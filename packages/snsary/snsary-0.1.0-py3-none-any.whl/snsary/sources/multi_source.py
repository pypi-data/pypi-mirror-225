"""
Manually subscribing each :mod:`Source <snsary.sources.source>` to each :mod:`Output <snsary.outputs.output>` is repetitive, especially when there are multiple Outputs. MultiSource combines multiple Sources as one. Just like a :mod:`Sensor <snsary.sources.sensor>`, a MultiSource also exposes a stream to make it easier to work with: ::

    MultiSource(MockSensor(), MockSensor()).stream.into(MockOutput())
"""

from .source import Source


class MultiSource(Source):
    def __init__(self, *sources):
        from snsary.streams import AsyncStream

        self.__stream = AsyncStream()

        for source in sources:
            source.subscribe(self.__stream)

    def subscribe(self, output):
        self.stream.subscribe(output)

    @property
    def stream(self):
        return self.__stream
