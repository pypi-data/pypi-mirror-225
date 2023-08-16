"""
Sends batches of :mod:`Readings <snsary.models.reading>` as rows to Google BigQuery to be stored in a dataset / table called ``snsary.readings``, using `the Google BigQuery Storage API <https://github.com/googleapis/python-bigquery-storage>`_.

Create an instance with ``.from_env()``, which expects:

- GOOGLE_APPLICATION_CREDENTIALS - the path to `a JSON credentials file <https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating>`_
- GOOGLE_BIGQUERY_STREAM - of the form ``projects/<your_project_id>/datasets/snsary/tables/readings/streams/_default``

Setting up BigQuery
===================

You can use the BigQuery UI to do most of the setup.

1. Create a dataset called ``snsary``.

    - Do not enable table expiration (this is different to partition expiration).

2. Create a table called ``readings``.

    - Add columns ``timestamp``, ``host``, ``sensor``, ``metric`` and ``value``.
    - Use ``TIMESTAMP`` for ``timestamp``, ``FLOAT`` for ``value`` and otherwise ``STRING``.
    - Partition the table **by day** using values of the **timestamp** column.

3. Set up partition expiration e.g. ::

       ALTER TABLE snsary.readings
       SET OPTIONS (
        partition_expiration_days=425
       )

You will also need to create `a Google Cloud service account <https://cloud.google.com/iam/docs/service-accounts>`_ and corresponding API key. The service account should have the "BigQuery Data Editor" role or similar.

Querying the data
=================

Example query for data in the table: ::

    SELECT $__timeGroup(timestamp,$__interval), sensor, metric, avg(value)
    FROM `snsary.readings`
    where $__timeFilter(timestamp)
    group by $__timeGroup(timestamp,$__interval), sensor, metric
    order by 1 asc

Note that the ``$__`` functions are `defined by Grafana <https://grafana.com/grafana/plugins/grafana-bigquery-datasource/>`_. A service account reading the data will need to have "BigQuery Data Viewer" and "BigQuery Job User" roles.
"""
import os
import platform

import pytz
from google.api_core.retry import Retry
from google.cloud import bigquery_storage_v1
from google.cloud.bigquery_storage_v1 import types
from google.protobuf import descriptor_pb2

from snsary.outputs import BatchOutput

from . import reading_pb2


class BigQueryOutput(BatchOutput):
    RETRY_DEADLINE = 10

    def __init__(self, stream):
        BatchOutput.__init__(self)
        self.__stream = stream
        self.__client = bigquery_storage_v1.BigQueryWriteClient()

    @classmethod
    def from_env(cls):
        return cls(
            stream=os.environ["GOOGLE_BIGQUERY_STREAM"],
        )

    def publish_batch(self, readings):
        proto_readings = [self.__proto_row(reading) for reading in readings]
        self.__proto_send(proto_readings)

    def __proto_row(self, reading):
        """
        Copy a :mod:`Reading <snsary.models.reading>` into an intermediary protobuf model `generated from a schema <https://developers.google.com/protocol-buffers/docs/pythontutorial>`_.
        """
        return reading_pb2.Reading(
            # using UTC ensures test stability when run in different zones
            timestamp=reading.datetime.astimezone(pytz.utc).isoformat(),
            host=platform.node(),
            sensor=reading.sensor_name,
            metric=reading.name,
            value=reading.value,
        )

    def __proto_send(self, proto_readings):
        """
        Serialise and send a set of intermediary protobuf readings together with their schema, which is redundant after the first attempt but simpler to keep sending anyway. This method was written by following the `BigQuery Storage API reference <https://cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1#google.cloud.bigquery.storage.v1.AppendRowsRequest>`_ and `an example implementation <https://github.com/googleapis/python-bigquery-storage/blob/main/samples/snippets/append_rows_pending.py>`_.
        """
        proto_descriptor = descriptor_pb2.DescriptorProto()
        reading_pb2.Reading.DESCRIPTOR.CopyToProto(proto_descriptor)

        proto_schema = types.ProtoSchema()
        proto_schema.proto_descriptor = proto_descriptor

        proto_rows = types.ProtoRows()

        for proto_reading in proto_readings:
            proto_rows.serialized_rows.append(
                proto_reading.SerializeToString(),
            )

        proto_data = types.AppendRowsRequest.ProtoData()
        proto_data.rows = proto_rows
        proto_data.writer_schema = proto_schema

        request = types.AppendRowsRequest()
        request.write_stream = self.__stream
        request.proto_rows = proto_data

        self.__client.append_rows(
            requests=iter([request]),
            retry=Retry(deadline=self.RETRY_DEADLINE),
        )
