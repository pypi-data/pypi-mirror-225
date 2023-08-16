"""
Creates a thread for each :mod:`Output <snsary.outputs.output>` that subscribes to. Any :mod:`Readings <snsary.models.reading>` are published to a separate queue for each :mod:`Output <snsary.outputs.output>`, with the thread logging any errors from relaying to it. Using AsyncStream helps avoid issues due to flakey or time-consuming :mod:`Outputs <snsary.outputs.output>`.
"""

from queue import Queue
from threading import Thread

from .stream import Stream


class AsyncStream(Stream):
    def __init__(self):
        self.__relays = {}

    def publish(self, reading):
        for queue in self.__relays.values():
            queue.put(reading)

    def subscribe(self, output):
        queue = Queue()
        self.__relays[output] = queue

        def _relay():
            while True:
                try:
                    output.publish(queue.get())
                except Exception as e:
                    output.logger.exception(e)

        Thread(target=_relay, daemon=True).start()
