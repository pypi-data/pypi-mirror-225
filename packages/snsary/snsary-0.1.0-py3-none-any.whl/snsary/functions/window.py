"""
Base class for functions that aggregate :mod:`Readings <snsary.models.reading>` over fixed, consecutive periods, specified as the keyword arguments for a ``timedelta`` (seconds, minutes, etc.).

A subclass should define an ``aggregate`` method that is called each time the age of the window for a sensor / reading name pair reaches the specified period.

The windows are consecutive, not moving: after a window has been aggregated a new window is started using the :mod:`Reading <snsary.models.reading>` that triggered the previous window to close.

Windows also act as a :mod:`Service <snsary.system.service>` in order to persist and restore :mod:`Readings <snsary.models.reading>` when the program they are used in starts and stops. See the :mod:`storage <snsary.utils.storage>` module for more details.
"""


from datetime import timedelta

from snsary import system

from .function import Function


class Window(Function, system.Service):
    def __init__(self, **kwargs):
        system.Service.__init__(self)
        self.__period = timedelta(**kwargs).total_seconds()
        self.__windows = dict()

    def stop(self):
        for key, window in self.__windows.items():
            self.logger.debug(f"Storing window for {key}.")
            self.store[key] = window

    def __call__(self, reading):
        key = self.key(reading)

        if key not in self.__windows and key in self.store:
            self.logger.debug(f"Restoring window for {key}.")
            self.__windows[key] = self.store[key]

        if key not in self.__windows:
            self.logger.debug(f"Starting window for {key}.")
            self.__windows[key] = [reading]
            return []

        readings = self.__windows[key]
        start = readings[0].timestamp
        age = reading.timestamp - start

        if age >= self.__period:
            self.logger.debug(f"Closing window for {key}.")
            self.__windows[key] = [reading]
            return self.aggregate(readings)

        readings.append(reading)
        return []

    def aggregate(self, readings):
        raise NotImplementedError()

    def key(self, reading):
        return f"window-{int(self.__period)}-{reading.sensor_name}-{reading.name}"
