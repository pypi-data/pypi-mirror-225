import logging
import sys
from threading import current_thread, main_thread

rootLogger = logging.getLogger("snsary")
loggers = dict()


class HasLogger:
    @property
    def name(self):
        return type(self).__name__

    @property
    def logger(self):
        return get_logger(self.name.lower())


def get_logger(name=None):
    thread_id = current_thread().ident

    if name:
        sublogger = logging.getLogger(f"snsary.{name}")
        loggers[thread_id] = sublogger
        return sublogger

    if main_thread().ident == thread_id:
        return rootLogger

    if thread_id in loggers:
        return loggers[thread_id]

    return logging.getLogger(f"snsary.anon-{thread_id}")


def configure_logging(level=logging.INFO):
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format="%(levelname)s - [%(name)s] %(message)s",
    )
