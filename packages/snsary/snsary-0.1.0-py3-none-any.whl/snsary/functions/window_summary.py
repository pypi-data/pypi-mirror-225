"""
Computes the mean, max, min and median (p50) of :mod:`Readings <snsary.models.reading>` over consecutive windows. The name of each computation is appended to the name of the :mod:`Reading <snsary.models.reading>` e.g. ``myreading--mean``.
"""

from statistics import mean, median

from .window import Window


class WindowSummary(Window):
    def aggregate(self, readings):
        def __dup_reading(name, value):
            base_reading = readings[-1]

            return base_reading.dup(
                name=base_reading.name + f"--{name}",
                value=value,
            )

        values = [r.value for r in readings]

        return [
            __dup_reading("mean", mean(values)),
            __dup_reading("max", max(values)),
            __dup_reading("min", min(values)),
            __dup_reading("p50", median(values)),
        ]
