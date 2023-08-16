from threading import Event

from snsary.models import Reading

from .polling_sensor import PollingSensor


class MockSensor(PollingSensor):
    def __init__(
        self,
        *,
        fail=False,
        hang=False,
        period_seconds=5,
        index=0,
    ):
        PollingSensor.__init__(
            self,
            period_seconds=period_seconds,
        )

        self.__hang = hang
        self.__fail = fail
        self.__failures = 0
        self.__index = index

    @property
    def name(self):
        return f"mocksensor-{self.__index}"

    def sample(
        self,
        now,  # unused here (implicit test for kwarg)
        start_time,  # unused (implicitly kwarg check)
        timestamp,
        elapsed_seconds,
    ):
        if self.__fail:
            self.__failures += 1
            raise RuntimeError(f"problem-{self.__failures}")

        if self.__hang:
            Event().wait()

        return [
            Reading(
                sensor_name=self.name,
                name="abc",
                timestamp=timestamp,
                value=elapsed_seconds,
            )
        ]
