"""
Publishes zero or more :mod:`Readings <snsary.models.Reading>` depending on what the specified :mod:`function <snsary.functions>` returns for a given :mod:`Reading <snsary.models.reading>`. This could be nothing, the same reading, or multiple, different readings.
"""
from wrapt import synchronized

from .simple_stream import SimpleStream


class FuncStream(SimpleStream):
    def __init__(
        self,
        stream,
        function=lambda reading: [reading],
    ):
        SimpleStream.__init__(self)
        stream.subscribe(self)
        self.__function = function

    @synchronized
    def publish(self, reading):
        output_readings = self.__function(reading)

        for output_reading in output_readings:
            SimpleStream.publish(self, output_reading)
