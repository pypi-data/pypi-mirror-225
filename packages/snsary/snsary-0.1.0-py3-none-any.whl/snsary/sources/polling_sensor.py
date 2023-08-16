from snsary.utils import tracing

from .poller import Poller
from .sensor import Sensor


class PollingSensor(Sensor, Poller):
    start = Poller.start

    def __init__(self, *, period_seconds):
        Sensor.__init__(self)
        Poller.__init__(self, period_seconds=period_seconds)

    @tracing.capture_exceptions("snsary.sources.polling_sensor")
    def tick(self, **kwargs):
        readings = list(self.sample(**kwargs))
        self.logger.info(f"Collected {len(readings)} readings.")

        for reading in readings:
            self.stream.publish(reading)

    def sample(self, **kwargs):
        raise NotImplementedError()
