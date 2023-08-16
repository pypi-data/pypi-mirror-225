"""
Manages the :mod:`Monitors <snsary.utils.tracing.monitors>` associated with an instrumented block of code. Calling ``get`` will return a list of instances of any :mod:`Monitors <snsary.utils.tracing.monitors>` set in :mod:`Config <snsary.utils.tracing.config>` for the specified ``trace_id``: ::

    config = Config()
    config.set("some.id.monitors", [Monitor.factory()])

    registry = Registry(config)
    registry.get("some.id")  # => [<Monitor>]

The same instances are returned across calls to ``get`` for the same ``trace_id``. Setting ``thread_aware`` in :mod:`Config <snsary.utils.tracing.config>` means the returned instances will also be unique across threads.
"""

from threading import current_thread


class Registry:
    def __init__(self, config):
        self.__backend = {}
        self.__config = config

    def reset(self):
        self.__backend = {}

    def get(self, trace_id):
        registry_id = self.__registry_id(trace_id)

        if registry_id not in self.__backend:
            monitors = self.__monitors(trace_id)
            self.__backend[registry_id] = monitors

        return self.__backend[registry_id]

    def __monitors(self, trace_id):
        return [
            monitor_class()
            for monitor_class in self.__config.get(
                f"{trace_id}.monitors",
                default=[],
            )
        ]

    def __registry_id(self, trace_id):
        registry_id = f"[trace_id={trace_id}]"

        thread_aware = self.__config.get(
            f"{trace_id}.thread_aware",
            default=False,
        )

        if thread_aware:
            thread_ident = current_thread().ident
            registry_id += f"[thread_ident={thread_ident}]"

        return registry_id
