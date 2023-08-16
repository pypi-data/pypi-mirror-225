from .source import Source


class Sensor(Source):
    def __init__(self):
        from snsary.streams import AsyncStream

        self.__stream = AsyncStream()

    @property
    def stream(self):
        return self.__stream

    def subscribe(self, output):
        self.stream.subscribe(output)
