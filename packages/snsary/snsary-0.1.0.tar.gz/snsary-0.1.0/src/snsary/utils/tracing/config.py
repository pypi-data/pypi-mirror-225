"""
Path-based key / value store with optional defaults.

Basic key / value access looks like this: ::

    config = Config()
    config.set("some.unique.path.attribute", 1)
    config.get("some.unique.path.attribute")  # => 1

Defaults can be set for each key access: ::

    config.get("some.other.path.attribute", default=2)  # => 2

Attribute defaults can also be set globally: ::

    config.set("attribute", 3)
    config.get("some.other.path.attribute", default=2)  # => 3
"""


class Config:
    def __init__(self):
        self.reset()

    def get(self, path, default=None):
        if path in self.__backend:
            return self.__backend[path]

        prefix, _, attribute = path.rpartition(".")

        if attribute in self.__backend:
            return self.__backend[attribute]

        if default is not None:
            return default

        raise KeyError(f"No config defined for '{path}'")

    def set(self, path, value):
        self.__backend[path] = value

    def reset(self):
        self.__backend = {}
