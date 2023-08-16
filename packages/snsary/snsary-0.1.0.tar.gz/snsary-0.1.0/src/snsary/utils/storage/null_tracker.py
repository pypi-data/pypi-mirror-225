from .tracker import Tracker


class NullTracker(Tracker):
    def __init__(self):
        pass

    def update(self, readings):
        """
        Does nothing.
        """
        return

    @property
    def values(self):
        """
        Returns {}.
        """
        return {}
