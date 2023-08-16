from .stream import Stream


class SimpleStream(Stream):
    def __init__(self):
        self.__outputs = []

    def publish(self, reading):
        for output in self.__outputs:
            try:
                output.publish(reading)
            except Exception as e:
                output.logger.exception(e)

    def subscribe(self, output):
        self.__outputs += [output]
