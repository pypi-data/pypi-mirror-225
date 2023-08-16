"""
Represents a FIFO list of :mod:`Samples <snsary.utils.tracing.sample>`. :mod:`Samples <snsary.utils.tracing.sample>` are added to the list with ``add``. The oldest :mod:`Sample <snsary.utils.tracing.sample>` is ejected when the list reaches the specified ``max_length``.
"""


class History:
    def __init__(self, *, max_length):
        self.__max_length = max_length
        self.__backend = []

    @property
    def max_length(self):
        return self.__max_length

    def add(self, sample):
        self.__backend.append(sample)

        if len(self) > self.max_length:
            self.__backend.pop(0)

    def reset(self):
        self.__backend.clear()

    def __len__(self):
        return len(self.__backend)

    def __iter__(self):
        return iter(self.__backend)
