"""
Sends batches of :mod:`Readings <snsary.models.reading>` as "points" to a specified InfluxDB bucket at a specified endpoint e.g. `InfluxDB Cloud <https://www.influxdata.com/products/influxdb-cloud>`_. Each point is named after the Reading and tagged by **sensor** and **host**.

Create an instance with ``.from_env()``, which expects:

- INFLUXDB_URL
- INFLUXDB_TOKEN
- INFLUXDB_ORG
- INFLUXDB_BUCKET
"""

import os
import platform

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from snsary.outputs import BatchOutput


class InfluxDBOutput(BatchOutput):
    @classmethod
    def from_env(cls):
        return cls(
            url=os.environ["INFLUXDB_URL"],
            token=os.environ["INFLUXDB_TOKEN"],
            org=os.environ["INFLUXDB_ORG"],
            bucket=os.environ["INFLUXDB_BUCKET"],
        )

    def __init__(self, *, url, token, org, bucket):
        BatchOutput.__init__(self)
        client = InfluxDBClient(url=url, token=token, org=org)
        self.__bucket = bucket
        self.__write_api = client.write_api(write_options=SYNCHRONOUS)

    def publish_batch(self, readings):
        points = [
            Point(reading.name)
            .tag("sensor", reading.sensor_name)
            .tag("host", platform.node())
            .field("value", reading.value)
            .time(reading.timestamp, write_precision="s")
            for reading in readings
        ]

        lines = [point.to_line_protocol() for point in points]
        self.logger.debug("Sending " + str(lines))

        self.__write_api.write(bucket=self.__bucket, record=points)
