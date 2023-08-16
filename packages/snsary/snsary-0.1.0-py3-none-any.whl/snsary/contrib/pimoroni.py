"""
Factory to wrap Pimoroni sensor objects, many of which have different ways to read data and structure the results. Because this is just a wrapper class, you will need to separately install the Pimoroni library for each sensor you want to poll.

Example for `the MICS6814 3-in-1 Gas Sensor <https://thepihut.com/products/mics6814-3-in-1-gas-sensor-breakout-co-no2-nh3>`_: ::

   # install the sensor library
   pip3 install pimoroni-mics6814

   # create the sensor to poll
   GenericSensor.mics6814_i2c()

Warning: sensors like ``mics6814_i2c`` rely on `the Pimoroni IO Expander library <https://github.com/pimoroni/ioe-python>`_, which uses `smbus2 <https://github.com/kplindegaard/smbus2>`_ internally and doesn't implement any kind of locking. This means it's possible for multiple sensors to conflict if they poll for data around the exact same time.
"""

from snsary.models import Reading
from snsary.sources import PollingSensor
from snsary.utils import scraper


class GenericSensor(PollingSensor):
    @classmethod
    def mics6814_i2c(cls):
        """
        Returns a sensor configured to scrape ``oxidising``, ``reducing`` and ``nh3`` values in Ohms. Calling this function also switches off the LED of the MICS 6814, which is on by default.

        Requires `the mics6814-python library <https://github.com/pimoroni/mics6814-python>`_. Note that, while Pimoroni do provide `a library for CircuitPython <https://github.com/pimoroni/Pimoroni_CircuitPython_MICS6814>`_ (similarly to many Adafruit sensors), this only supports pin-based wiring.
        """

        # data is stored as slots in reading
        from mics6814 import Mics6814Reading

        class_scraper = scraper.for_class(Mics6814Reading)

        # create once to avoid descriptor leak
        from mics6814 import MICS6814

        instance = MICS6814()

        # turn off bright LED (on by default)
        instance.set_led(0, 0, 0)

        def read_fn():
            scraps = class_scraper(instance.read_all())
            # filter out internal "adc" resistance values
            return filter(lambda scrap: scrap[0] != "adc", scraps)

        return cls(name="MICS6814", read_fn=read_fn)

    def __init__(self, *, name, read_fn):
        PollingSensor.__init__(self, period_seconds=10)
        self.__name = name
        self.__read_fn = read_fn

    @property
    def name(self):
        return self.__name

    def sample(self, timestamp, **kwargs):
        return [
            Reading(
                sensor_name=self.name,
                name=name,
                value=value,
                timestamp=timestamp,
            )
            for name, value in self.__read_fn()
        ]
