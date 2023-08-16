"""
A store has a dict-like interface to get and set data that a consumer wants to persist between program restarts e.g. the current :mod:`Readings <snsary.models.reading>` in a :mod:`Window <snsary.functions.window>`. This module provides a ``get_storage`` function and a ``HasStore`` trait to make it easy access to persistent storage.

By default persistent storage is disabled to avoid creating files without warning - the data stored is only held in memory and not written to disk. Set the ``STORAGE_PATH`` environment variable to enable persistent storage to a file e.g. ``export STORAGE_PATH=snsary.db``.

Storage trackers
================

Trackers can be used to keep track of values of series of :mod:`Readings <snsary.models.reading>` with specified names using persistent storage. New values for each series are individually compared with old values using the specified function for the series e.g. ::

    Tracker('id-for-persistent-storage', myreading=max, othername=min)

Call ``update`` when new readings are available for any of the series. ``on_change`` is then called with :mod:`Reading <snsary.models.reading>` kwargs ``old`` and ``new`` when each of the tracked series changes - set to a different function to subscribe to changes.

Storage internals
=================

Persistent storage uses the `pickle <https://docs.python.org/3/library/pickle.html>`_ module internally. Data to be stored is only written to disk when a program exits, to prevent any issues from concurrent writes. If the specified file doesn't exist when a program starts, it will be created when data is first written.

Even persistent storage will expire, to prevent a build up of dead data over time as a program evolves with different consumers of storage and different data to store. Set the ``STORAGE_TTL`` environment variable to override the default TTL of 1 day.

The storage format is not versioned and may break without warning after an upgrade. You will need to manually remove the file at ``STORAGE_PATH`` if this happens.
"""

from .backend import HasStore, get_storage
from .max_tracker import MaxTracker
from .null_tracker import NullTracker
from .tracker import Tracker

__all__ = [
    "HasStore",
    "get_storage",
    "MaxTracker",
    "NullTracker",
    "Tracker",
]
