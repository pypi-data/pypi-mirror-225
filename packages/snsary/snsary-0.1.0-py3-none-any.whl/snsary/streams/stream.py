from snsary.functions import Filter, Rename, WindowAverage, WindowSummary
from snsary.outputs import Output
from snsary.sources import Source


class Stream(Source, Output):
    def into(self, *outputs):
        for output in outputs:
            self.subscribe(output)

    def tee(self, output):
        """
        Subscribes the specified :mod:`Output <snsary.outputs.output>` to the stream using ``into``, but unlike ``into`` also returns the stream for further use, similar to the Unix ``tee`` command.
        """
        self.into(output)
        return self

    def apply(self, function):
        from .func_stream import FuncStream

        return FuncStream(self, function)

    def filter_names(self, *names):
        return self.apply(Filter.names(*names))

    def average(self, **kwargs):
        """
        Returns a new stream that applies a :mod:`WindowAverage <snsary.functions.window_average>` to all :mod:`Readings <snsary.models.reading>` over a period, specified as the keyword arguments for a ``timedelta``.
        """
        return self.apply(WindowAverage(**kwargs))

    def summarize(self, **kwargs):
        """
        Returns a new stream that applies a :mod:`WindowSummary <snsary.functions.window_summary>` to all :mod:`Readings <snsary.models.reading>` over a period, specified as the keyword arguments for a ``timedelta``.
        """
        return self.apply(WindowSummary(**kwargs))

    def rename(self, **kwargs):
        """
        Returns a new stream that applies a :mod:`Rename <snsary.functions.rename>` to all :mod:`Readings <snsary.models.reading>`. For example, ``rename(append="foo")`` will append "foo" to all reading names.
        """
        return self.apply(Rename(**kwargs))
