from threading import Event

from .output import Output


class MockOutput(Output):
    def __init__(
        self,
        *,
        fail=False,
        hang=False,
        index=0,
    ):
        self.__fail = fail
        self.__hang = hang
        self.__failures = 0
        self.__index = index

    @property
    def name(self):
        return f"mockoutput-{self.__index}"

    def publish(self, reading):
        if self.__hang:
            Event().wait()

        if self.__fail:
            self.__failures += 1
            raise RuntimeError(f"problem-{self.__failures}")

        self.logger.info(f"Reading: {reading}")
