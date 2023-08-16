from snsary.utils import logging


class Source(logging.HasLogger):
    def subscribe(self, output):
        raise NotImplementedError()
