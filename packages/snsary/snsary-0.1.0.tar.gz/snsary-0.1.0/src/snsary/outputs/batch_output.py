"""
Depending on the output, it may be more efficient to dispatch multiple :mod:`Readings<snsary.models.reading>` together. This can be done by inheriting from BatchOutput, which requires a ``publish_batch`` method.

BatchOutput protects against concurrent execution of its ``publish`` method. BatchOutput is also a :mod:`Service <snsary.system.service>` and will try to publish any remaining Readings when told to ``stop()``.
"""

from datetime import datetime

from wrapt import synchronized

from snsary import system
from snsary.utils import tracing

from .output import Output


class BatchOutput(Output, system.Service):
    def __init__(self, *, max_size=100, max_wait_seconds=10):
        Output.__init__(self)
        self.__max_size = max_size
        self.__readings = []
        self.__max_wait_seconds = max_wait_seconds
        self.__last_publish = datetime.utcnow().timestamp()

    @tracing.capture_exceptions("snsary.outputs.batch_output")
    def flush(self):
        # in case of multiple consecutive batch/age flushes
        if not self.__readings:
            return

        self.logger.info(f"Sending {len(self.__readings)} readings.")
        self.publish_batch(self.__readings)
        self.__readings = []

    def stop(self):
        if self.__readings:
            self.flush()

    @synchronized
    def publish(self, reading):
        self.__readings += [reading]
        self.__try_publish_large_batch()
        self.__try_publish_old_batch()

    def publish_batch(self, readings):
        raise NotImplementedError()

    def __try_publish_large_batch(self):
        if len(self.__readings) < self.__max_size:
            return

        self.flush()

    def __try_publish_old_batch(self):
        now = datetime.utcnow().timestamp()
        delay = now - self.__last_publish

        if delay > self.__max_wait_seconds:
            self.flush()
            self.__last_publish = now
