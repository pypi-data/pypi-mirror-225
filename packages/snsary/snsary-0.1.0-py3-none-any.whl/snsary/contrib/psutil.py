import psutil

from snsary.models import Reading
from snsary.sources import PollingSensor
from snsary.utils import scraper


class PSUtilSensor(PollingSensor):
    FUNCTIONS = {
        "cpu_times": {},
        "cpu_percent": {"interval": 1},
        "cpu_count": {},
        "cpu_stats": {},
        "getloadavg": {},
        "virtual_memory": {},
        "swap_memory": {},
        "disk_usage": {"path": "/"},
        "disk_io_counter": {},
        "net_io_counters": {},
        "sensors_temperatures": {},
        "sensors_fans": {},
        "sensors_battery": {},
    }

    def __init__(self, functions=FUNCTIONS):
        self.__functions = functions
        PollingSensor.__init__(self, period_seconds=10)

    @property
    def name(self):
        return "psutil"

    def sample(self, timestamp, **kwargs):
        for fname in self.__functions:
            yield from self.__readings_from_function(
                timestamp,
                fname,
            )

    def __readings_from_function(self, timestamp, fname):
        for name, value in self.__sample_fn(fname):
            yield Reading(
                sensor_name=self.name,
                name=name,
                value=value,
                timestamp=timestamp,
            )

    def __sample_fn(self, fname):
        if not hasattr(psutil, fname):
            self.logger.debug(f"Skipping {fname} as not available.")
            return []

        kwargs = self.__functions[fname]
        value = getattr(psutil, fname)(**kwargs)

        self.logger.debug(f"Scraping {fname} => {value}")
        return scraper.extract_from(value, prefix=fname)
