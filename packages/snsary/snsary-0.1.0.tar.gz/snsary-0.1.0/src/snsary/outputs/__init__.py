"""
An Output has a ``publish`` method to receive :mod:`Readings <snsary.models.reading>`. Note that ``publish`` may be called concurrently if an Output is attached to multiple asynchronous :mod:`Sources <snsary.sources.source>`.
"""

from .batch_output import BatchOutput
from .mock_output import MockOutput
from .output import Output

__all__ = [
    "BatchOutput",
    "MockOutput",
    "Output",
]
