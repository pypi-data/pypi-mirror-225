"""
Sends batches of :mod:`Readings <snsary.models.reading>` as "mutations" to a specified `DataStax Astra DB <https://docs.datastax.com/en/astra/docs/index.html>`_ GraphQL endpoint using the `Python GQL client <https://github.com/graphql-python/gql>`_, as a means of inserting into a Cassandra table.

GraphQL replaces normal REST with a server-defined language / API in nested {} format. `DataStax generates the API automatically based on the keyspaces and tables that exist <https://docs.datastax.com/en/astra/docs/using-the-astra-graphql-api.html>`_.

GraphQL isn't well suited to timeseries data: every insertion ("mutation") must have a unique alias. The output compensates for this by using throwaway "r0", "r1" aliases for each reading mutation. See the tests for an example. In order to simplify building each request, the output makes an initial request to get the schema for the keyspace in order to utilise the DSL feature.

Create an instance with ``.from_env()``, which expects:

- DATASTAX_URL
- DATASTAX_TOKEN (needs API write permission)

Setting up Astra DB
===================

Create a DB table in Astra as follows: ::

    CREATE TABLE reading (
        host text,
        sensor text,
        metric text,
        timestamp timestamp,
        value double,
        PRIMARY KEY ((host,sensor,metric), timestamp)
    )
    WITH CLUSTERING ORDER BY (timestamp DESC)
    AND default_time_to_live = 33696000;

The output specifies a TTL for each insertion, which may be configurable in future. Having a default TTL for the table is optional but reduces the risk of data remaining indefinitely. Note that it's current not possible to specify other options like the compaction strategy. However, `the DataStax docs say the default strategy is suitable for time series data <https://docs.datastax.com/en/astra/docs/datastax-astra-database-limits.html>`_.

Querying the data
=================

Example GraphQL query for data in the table: ::

    query readings {
      data:reading (
        options: {
          pageSize: 10000, limit: 10000
        },
        filter: {
          host: { eq: "raspberrypi" },
          sensor: { eq: "PMSx003" },
          metric: { eq: "pm25--max/minute" },
          timestamp: { gt: "${__from:date:iso}", lt: "${__to:date:iso}" }
        }
      ) {
        values {
          host, sensor, metric, timestamp, value
        }
      }
    }

Note that the "$" variables are `Grafana global variables <https://grafana.com/docs/grafana/latest/variables/variable-types/global-variables/>`_.
"""

import logging
import os
import platform

import pytz
from gql import Client
from gql.dsl import DSLMutation, DSLSchema, dsl_gql
from gql.transport.requests import RequestsHTTPTransport
from graphql import print_ast

from snsary.outputs import BatchOutput


class GraphQLOutput(BatchOutput):
    TTL = 33696000  # 13 months

    def __init__(self, url, token):
        self.__client = Client(
            transport=RequestsHTTPTransport(
                url=url,
                headers={"X-Cassandra-Token": token},
            ),
        )

        # logs per request otherwise
        logging.getLogger("gql").setLevel(logging.WARNING)

        BatchOutput.__init__(self)
        self.__init_schema()

    @classmethod
    def from_env(cls):
        return cls(
            url=os.environ["DATASTAX_URL"],
            token=os.environ["DATASTAX_TOKEN"],
        )

    def publish_batch(self, readings):
        mutations = list(
            self.__mutation(reading).alias(f"r{i}")
            for i, reading in enumerate(readings)
        )

        query = dsl_gql(DSLMutation(*mutations))
        self.logger.debug(f"Sending {print_ast(query)}")
        self.__client.execute(query)

    def __mutation(self, reading):
        value = {
            # using UTC ensures test stability when run in different zones
            "timestamp": reading.datetime.astimezone(pytz.utc).isoformat(),
            "sensor": reading.sensor_name,
            "host": platform.node(),
            "metric": reading.name,
            "value": float(reading.value),
        }

        throwaway_result = self.__dsl.readingMutationResult.value.select(
            self.__dsl.reading.metric
        )

        return self.__dsl.Mutation.insertreading.args(
            options={"ttl": self.TTL}, value=value
        ).select(throwaway_result)

    def __init_schema(self):
        with self.__client as session:
            session.fetch_schema()

        self.logger.debug("Initialised schema.")
        self.__dsl = DSLSchema(self.__client.schema)
