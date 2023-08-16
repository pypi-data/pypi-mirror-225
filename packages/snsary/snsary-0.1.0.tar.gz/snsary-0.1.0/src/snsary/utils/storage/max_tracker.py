from .tracker import Tracker


class MaxTracker(Tracker):
    def __init__(self, id, *, names, on_change):
        self.on_change = on_change
        Tracker.__init__(self, id, **{name: max for name in names})
