from snsary.utils import logging


class Function(logging.HasLogger):
    def __call__(reading):
        raise NotImplementedError()
