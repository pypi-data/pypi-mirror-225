from ..logging import get_logger
from .history import History
from .sample import Sample


class Monitor:
    """
    Analyses :mod:`Samples <snsary.utils.tracing.sample>` of the execution of some code.
    """

    def analyse(self, sample):
        raise NotImplementedError()

    @classmethod
    def factory(cls, **kwargs):
        return lambda: cls(**kwargs)


class TimeSeriesAlert(Monitor):
    """
    Provides a :mod:`History <snsary.utils.tracing.history>` of :mod:`Samples <snsary.utils.tracing.sample>` over time to support time series alerting. Each subclass is responsible for managing the history.
    """

    MAX_HISTORY = 300

    def __init__(self, *, history=None):
        self._history = (
            history
            if history is not None
            else History(
                max_length=self.MAX_HISTORY,
            )
        )


class LivenessAlert(TimeSeriesAlert):
    """
    Logs an error when a complete history of samples is nothing but failures.

    The history is reset every time the monitor logs an error.
    """

    def analyse(self, sample):
        self._history.add(sample)

        if len(self._history) < self._history.max_length:
            return

        for sample in self._history:
            if sample == Sample.SUCCESS:
                return

        get_logger().error(
            f"Alert: {self._history.max_length} failures in sample window"
        )
        self._history.reset()


class GapAlert(TimeSeriesAlert):
    """
    Logs an error when there are too many gaps in ``SUCCESS`` samples. A gap
    is one or more ``FAILURE`` samples followed by a ``SUCCESS`` sample.

    The history is reset every time the monitor logs an error.
    """

    MAX_GAPS = 30

    def __init__(self, *, max_gaps=MAX_GAPS, **kwargs):
        TimeSeriesAlert.__init__(self, **kwargs)
        self.__max_gaps = max_gaps

    def analyse(self, sample):
        self._history.add(sample)

        if self.__count_gaps() <= self.__max_gaps:
            return

        get_logger().error(f"Alert: {self.__max_gaps + 1} gaps in last sample window")
        self._history.reset()

    def __count_gaps(self):
        gaps = 0
        previous = None

        for sample in self._history:
            if previous == Sample.FAILURE and sample == Sample.SUCCESS:
                gaps += 1

            previous = sample

        return gaps
