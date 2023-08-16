"""
Outputs KWh (electricity) or cubic meter (gas) consumption from a specified Smart Meter in `half hour intervals <https://developer.octopus.energy/docs/api/#consumption>`_. At the time of writing, data is only available for the previous day sometime on the following day (not sure exactly when). Create instances with ``.<fuel_type>_from_env()``.

- ``.electricity_from_env()`` expects:
    - OCTOPUS_ELECTRICITY_MPAN
    - OCTOPUS_ELECTRICITY_SERIAL
    - OCTOPUS_TOKEN

- ``.gas_from_env()`` expects:
    - OCTOPUS_GAS_MPRN
    - OCTOPUS_GAS_SERIAL
    - OCTOPUS_TOKEN

"""

import os
from datetime import timedelta

import pyrfc3339

from snsary.models import Reading
from snsary.sources import PollingSensor
from snsary.utils import request


class OctopusSensor(PollingSensor):
    CONSUMPTION_URL = "https://api.octopus.energy/v1/{fuel_type}-meter-points/{mpxn}/meters/{serial_number}/consumption/?period_from={period_from}&order_by=period"

    @classmethod
    def electricity_from_env(cls):
        return cls(
            mpxn=os.environ["OCTOPUS_ELECTRICITY_MPAN"],
            serial_number=os.environ["OCTOPUS_ELECTRICITY_SERIAL"],
            token=os.environ["OCTOPUS_TOKEN"],
            fuel_type="electricity",
        )

    @classmethod
    def gas_from_env(cls):
        return cls(
            mpxn=os.environ["OCTOPUS_GAS_MPRN"],
            serial_number=os.environ["OCTOPUS_GAS_SERIAL"],
            token=os.environ["OCTOPUS_TOKEN"],
            fuel_type="gas",
        )

    def __init__(self, *, mpxn, serial_number, token, fuel_type):
        PollingSensor.__init__(
            self,
            period_seconds=30 * 60,  # 30 mins
        )

        self.__token = token
        self.__mpxn = mpxn
        self.__serial_number = serial_number
        self.__fuel_type = fuel_type

    @property
    def name(self):
        return f"octopus.{self.__fuel_type}"

    def sample(self, now, **kwargs):
        start = now - timedelta(days=1)
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)

        url = self.CONSUMPTION_URL.format(
            mpxn=self.__mpxn,
            serial_number=self.__serial_number,
            period_from=pyrfc3339.generate(start),
            fuel_type=self.__fuel_type,
        )

        self.logger.debug(f"Request {url}")
        response = request.retrying_session().get(
            url,
            auth=(self.__token, ""),
        )
        response.raise_for_status()

        samples = response.json()["results"]
        self.logger.debug(f"Response {samples}")

        for sample in samples:
            yield self.__reading_from_sample(sample)

    def __reading_from_sample(self, sample):
        sample_datetime = pyrfc3339.parse(sample["interval_end"])
        sample_timestamp = int(sample_datetime.timestamp())

        return Reading(
            sensor_name=self.name,
            name="consumption",
            timestamp=sample_timestamp,
            value=sample["consumption"],
        )
