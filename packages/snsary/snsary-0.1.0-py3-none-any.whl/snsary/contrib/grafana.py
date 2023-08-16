"""
A collection of tools to interact with a remote Grafana Cloud instance.

`GraphiteOutput` sends batches of :mod:`Readings <snsary.models.reading>` to Grafana Cloud, who provide `a custom ingest endpoint for Graphite metrics <https://grafana.com/docs/grafana-cloud/metrics-graphite/http-api/>`_. Metric names are of the form ``<prefix>.<sensor name>.<reading name>``. Using ``.from_env()`` to create an instance sets the ``<prefix>`` to the hostname of the machine. ``.from_env()`` expects ``GRAPHITE_URL`` to be set as an environment variable.
"""

import json
import os
import platform

from snsary.outputs import BatchOutput
from snsary.utils import request


class GraphiteOutput(BatchOutput):
    @classmethod
    def from_env(cls):
        return cls(
            url=os.environ["GRAPHITE_URL"],
            prefix=platform.node(),
        )

    def __init__(self, *, url, prefix):
        BatchOutput.__init__(self)
        self.__url = url
        self.__prefix = prefix

    def publish_batch(self, readings):
        data = self.__format(readings)
        self.logger.debug(f"Sending {data}")

        response = request.retrying_session().post(
            self.__url,
            data=data,
            headers={"Content-Type": "application/json"},
        )

        self.logger.debug(response.text)
        response.raise_for_status()

    def __format(self, readings):
        return json.dumps(
            [
                {
                    "name": f"{self.__prefix}.{reading.sensor_name}.{reading.name}",
                    "value": reading.value,
                    "time": reading.timestamp,
                    "interval": 1,
                }
                for reading in readings
            ]
        )
