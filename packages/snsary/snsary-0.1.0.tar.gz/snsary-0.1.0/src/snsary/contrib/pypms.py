"""
An adapter for `the PyPMS library <https://github.com/avaldebe/PyPMS>`_.

Example of creating an instance::

    PyPMSSensor(sensor_name='PMSx003')
"""
import dataclasses

from pms.core.reader import SensorReader

from snsary.models import Reading
from snsary.sources import PollingSensor


class PyPMSSensor(PollingSensor):
    """
    ``warm_up_seconds`` is necessary for some sensors e.g. for the PMSA003 the first two samples always `raise an InconsistentObservation exception <https://github.com/avaldebe/PyPMS/blob/04ff8edede7d780018cd00a7fcf78ffed43c0de4/src/pms/sensors/plantower/pmsx003.py#L63>`_.
    """

    class SnsaryReader(SensorReader):
        """
        PyPMS SensorReader customisations.
        """

        def _pre_heat(self):
            """
            Disable pre-heat to avoid blocking samples.

            Sensors will raise an exception if they are not ready.
            """
            pass

    def __init__(
        self,
        *,
        sensor_name,
        port="/dev/ttyS0",
        timeout=5,
    ):
        self.__reader = self.SnsaryReader(
            sensor=sensor_name,
            port=port,
            samples=1,
            max_retries=0,
            timeout=timeout,
        )

        PollingSensor.__init__(
            self,
            period_seconds=10,
        )

    @property
    def name(self):
        return self.__reader.sensor.name

    def start(self):
        self.__reader.open()
        PollingSensor.start(self)

    def stop(self):
        PollingSensor.stop(self)

        try:
            self.__reader.close()
        except Exception as e:
            self.logger.exception(e)

    def sample(self, timestamp, elapsed_seconds, **kwargs):
        if elapsed_seconds < self.__reader.pre_heat:
            self.logger.info("Still warming up, no data yet.")
            return []

        obs = next(self.__reader())

        return [
            Reading(
                sensor_name=self.name,
                name=key,
                value=value,
                timestamp=timestamp,
            )
            for key, value in dataclasses.asdict(obs).items()
            if key not in ("time")
        ]
