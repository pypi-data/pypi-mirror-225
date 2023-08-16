"""
Tracing utility with a ``capture_exceptions`` decorator that instruments a given function to monitor success and failure (exceptions) over time; exceptions are captured and logged as warnings. Basic usage of the tracing utility looks like this (with global configuration): ::

    @tracing.capture_exceptions("some.unique.path")
    def noisy_error_function():
        ...

    tracing.configure({
        # tracing is disabled by default
        "enabled": True,

        # specify how to look for errors
        "monitors": [
            tracing.GapsAlert.factory(),
            tracing.LivenessAlert.factory(),
        ],

        # monitor each thread separately
        "thread_aware": True,
    })

With this config, the tracing system will create a new instance of each :mod:`Monitor <snsary.utils.tracing.monitors>` for each function being traced and each thread that calls the function. You can change this behaviour on a per-function basis. For example, customising ``some.unique.path`` looks like this: ::

    tracing.configure({
        "some.unique.path.monitors": [
            tracing.GapsMonitor.factory(
                max_gaps=5,
                history=SimpleHistory(max_length=10),
            )
        ]
    })


See the :mod:`Config <snsary.utils.tracing.config>` module for more details.
"""

from .config import Config
from .core import capture_exceptions, configure, reset
from .history import History
from .monitors import GapAlert, LivenessAlert, Monitor
from .registry import Registry
from .sample import Sample

__all__ = [
    "capture_exceptions",
    "configure",
    "GapAlert",
    "LivenessAlert",
    "Sample",
    "Monitor",
    "reset",
    "History",
    "Config",
    "Registry",
]
