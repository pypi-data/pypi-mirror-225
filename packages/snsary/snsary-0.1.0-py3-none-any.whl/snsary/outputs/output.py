from snsary.utils import logging


class Output(logging.HasLogger):
    def publish(self, reading):
        raise NotImplementedError()
