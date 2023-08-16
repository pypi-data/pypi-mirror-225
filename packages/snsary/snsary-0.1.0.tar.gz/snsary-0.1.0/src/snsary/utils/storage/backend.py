import atexit
import os
import pickle

from cachetools import TTLCache, cached

from ..logging import get_logger


class HasStore:
    @property
    def store(self):
        """
        Shortcut to calling ``get_storage()`` directly.
        """
        return get_storage()


@cached({})
def get_storage():
    """
    Returns a memoised dict-like store.
    """
    return _get_storage_backend()


def _get_storage_backend():
    path = os.environ.get("STORAGE_PATH", "")

    if not path:
        get_logger().debug("Using memory store.")
        return dict()

    get_logger().debug(f"Using store {path}.")
    ttl = os.environ.get("STORAGE_TTL", 86400)

    get_logger().debug(f"Store TTL set to {ttl}.")
    return _get_file_backend(path, int(ttl))


def _get_file_backend(path, ttl):
    try:
        cache = pickle.load(open(path, "rb"))
    except Exception:
        get_logger().debug(f"{path} not found.")
        get_logger().debug("Creating new store.")
        cache = TTLCache(float("inf"), ttl)

    def atexit_handler():
        get_logger().debug(f"Writing store {path}.")
        pickle.dump(cache, open(path, "wb"))

    atexit.register(atexit_handler)
    return cache
