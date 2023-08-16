"""
Wrapper for the Adafruit SGP30 sensor, inheriting from :mod:`GenericSensor <snsary.contrib.adafruit.generic>`:

    - Waits 15 seconds for the device to warm up (as per the `datasheet <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9_Gas_Sensors/Datasheets/Sensirion_Gas_Sensors_Datasheet_SGP30.pdf>`_).
    - Standardises the name used for logs and readings to "SGP30".

The installation and configuration is the same as the generic wrapper: ::

    # install the sensor library
    pip3 install adafruit-circuitpython-sgp30

    # create the sensor object
    import board
    i2c = board.I2C()
    sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

    # prepare to poll / scrape
    SGP30Sensor(sgp30)

``SGP30Sensor`` polls at the default period of :mod:`GenericSensor <snsary.contrib.adafruit.generic>`. The `datasheet <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9_Gas_Sensors/Datasheets/Sensirion_Gas_Sensors_Datasheet_SGP30.pdf>`_ says it should be 1s, but this doesn't work in practice, especially when the I2C bus is busy.

Humidity compensation
=====================

``SGP30Sensor`` is also an :mod:`Output <snsary.outputs.output>`. The TVOC and eCO2 readings from the SGP30 sensor need to be adjusted based on the absolute humidity of the surrounding air, which `can be calculated <https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9_Gas_Sensors/Datasheets/Sensirion_Gas_Sensors_Datasheet_SGP30.pdf>`_ from the "temperature" and "relative_humidity" in a batch of :mod:`Readings <snsary.models.reading>`: ::

    # SCD30 outputs the required readings
    GenericSensor(scd30).stream.tee(sgp30)

The required names - "tempeature" and "relative_humidity" - may not match some sensors. One way to work around this is to rename each :mod:`Reading <snsary.models.reading>` on the fly: ::

    OtherSensor.stream.filter_names('temp').rename(to='temperature').into(sgp30)
    OtherSensor.stream.filter_names('humid').rename(to='relative_humidity').into(sgp30)

Persistent IAQ baselines
========================

``SGP30Sensor`` emits ``baseline_TVOC`` and ``baseline_eCO2`` values, which are a moving average of the best environmental conditions the sensor has encountered. Higher values are better (from manual observation). `Adafruit recommend exposing the sensor to fresh air for at least 10 minutes <https://learn.adafruit.com/adafruit-sgp30-gas-tvoc-eco2-mox-sensor/circuitpython-wiring-test>`_ as part of configuring the IAQ baseline.

Every time the SGP30 sensor is sampled, the values of both baseline :mod:`Readings <snsary.models.reading>` are checked. Higher values are set as the new baseline for future readings; use ``persistent_baselines=False`` in the constructor to disable this. The baseline values are kept in persistent :mod:`storage <snsary.utils.storage>` so they survive restarts. See the :mod:`storage <snsary.utils.storage>` module for more details.

"""

from snsary.outputs import BatchOutput
from snsary.utils import storage

from .generic import GenericSensor


class SGP30Sensor(GenericSensor, BatchOutput):
    def __init__(self, device, persistent_baselines=True):
        BatchOutput.__init__(self)
        GenericSensor.__init__(self, device)

        if persistent_baselines:
            self.tracker = storage.MaxTracker(
                self.name,
                names=["baseline_TVOC", "baseline_eCO2"],
                on_change=self.baselines_changed,
            )
        else:
            self.tracker = storage.NullTracker()
            self.logger.debug("Persistent baselines disabled, ignoring.")

    @property
    def name(self):
        return "SGP30"

    def start(self):
        if self.tracker.values:
            self.baselines_changed(old={}, new=self.tracker.values)
        else:
            self.logger.debug("No baselines to restore, using defaults.")

        GenericSensor.start(self)

    def ready(self, elapsed_seconds, **kwargs):
        return elapsed_seconds > 15

    def sample(self, **kwargs):
        readings = GenericSensor.sample(self, **kwargs)
        self.tracker.update(readings)
        return readings

    def baselines_changed(self, old, new):
        self.logger.debug(f"Setting baselines: {new}")

        self.device.set_iaq_baseline(
            eCO2=new["baseline_eCO2"], TVOC=new["baseline_TVOC"]
        )

    def publish_batch(self, readings):
        temperatures = self.__filter(readings, "temperature")
        relative_humidities = self.__filter(readings, "relative_humidity")

        if not temperatures or not relative_humidities:
            self.logger.warning("Incomplete data for self-calibration.")
            return

        self.device.set_iaq_relative_humidity(
            celsius=temperatures[-1].value,
            relative_humidity=relative_humidities[-1].value,
        )

    def __filter(self, readings, name):
        return [reading for reading in readings if reading.name == name]
