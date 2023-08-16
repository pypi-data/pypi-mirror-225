"""
Computes a mean average of :mod:`Readings <snsary.models.reading>` over fixed, consecutive windows.
"""

from statistics import mean

from .window import Window


class WindowAverage(Window):
    def aggregate(self, readings):
        aggregate_value = mean(r.value for r in readings)
        return [readings[-1].dup(value=aggregate_value)]
