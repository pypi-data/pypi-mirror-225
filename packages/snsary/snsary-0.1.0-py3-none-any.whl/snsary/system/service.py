"""
Base class for anything that needs to perform an action during the ``start`` or ``stop`` phases of a program. This could be something like spawning a thread, or storing data to disk. Each instance of a service is recorded in a global registry so it can be managed by the :mod:`system <snsary.system>` module.
"""

from snsary.utils import logging, storage

_instances = []


class Service(logging.HasLogger, storage.HasStore):
    def __init__(self):
        global _instances
        _instances += [self]

    def start(self):
        """
        Called synchronously by the :mod:`system <snsary.system>` module as part of program startup.
        """
        pass

    def stop(self):
        """
        Called asynchronously by the :mod:`system <snsary.system>` module when a program is stopping. The execution will eventually time out to ensure the overall program stops in good time.
        """
        pass


def clear_services():
    """
    Clear the global list of service instances. For testing use only.
    """
    global _instances
    _instances = []


def get_services():
    """
    Return a list of all service instances.
    """
    return _instances
