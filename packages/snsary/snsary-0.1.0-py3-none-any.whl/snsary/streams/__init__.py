"""
A :mod:`Stream <snsary.streams.stream>` is an :mod:`Output <snsary.outputs.output>` and a :mod:`Source <snsary.sources.source>` that provides some kind of additional functionality over connecting :mod:`Sources <snsary.sources.source>` to :mod:`Outputs <snsary.outputs.output>` directly. All :mod:`Sensors <snsary.sources.sensor>` expose a ``stream`` of their :mod:`Readings <snsary.models.reading>` e.g. ``MockSensor().stream`` returns an :mod:`AsyncStream <snsary.streams.async_stream>` to cope with flakey :mod:`Outputs <snsary.outputs.output>`.

Streams make it easy to subscribe multiple :mod:`Outputs <snsary.outputs.output>` with ``into``: ::

    # same as calling "subscribe" for each
    stream.into(MockOutput(), MockOutput())

Any :mod:`Stream <snsary.streams.stream>` can also be wrapped in a :mod:`Filter <snsary.functions.filter>` function e.g. ::

    # only output readings for sensor "foo"
    stream.apply(Filter.sensor_name('foo')).into(MockOutput())

    # only output readings called "a", etc.
    # convenience shortcut method for "apply"
    stream.filter_names('a', 'b', 'c').subscribe(MockOutput())

A stream can actually be used to ``apply`` any one-to-many :mod:`function <snsary.functions>` to the readings that pass through it. For example, to average the distinct readings received in a window: ::

    # outputs an average value every 3 seconds
    # for each distinct sensor / reading name;
    # convenience shortcut method for "apply"
    stream.average(seconds=3).into(MockOutput())
"""


from .async_stream import AsyncStream
from .simple_stream import SimpleStream
from .stream import Stream

__all__ = [
    "SimpleStream",
    "AsyncStream",
    "Stream",
]
