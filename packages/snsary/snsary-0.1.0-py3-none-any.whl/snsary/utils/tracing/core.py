import functools

from ..logging import get_logger
from .config import Config
from .registry import Registry
from .sample import Sample

_config = Config()
_registry = Registry(_config)


def reset():
    _config.reset()
    _registry.reset()


def configure(settings):
    for path, value in settings.items():
        _config.set(path, value)


def capture_exceptions(trace_id):
    def _factory(fn):
        @functools.wraps(fn)
        def _wrapper(*args, **kwargs):
            enabled = _config.get(f"{trace_id}.enabled", default=False)
            monitors = _registry.get(trace_id)

            if not enabled:
                return fn(*args, **kwargs)

            try:
                result = fn(*args, **kwargs)

                for monitor in monitors:
                    monitor.analyse(Sample.SUCCESS)

                return result
            except Exception as e:
                for monitor in monitors:
                    monitor.analyse(Sample.FAILURE)

                get_logger().warning(e)

        return _wrapper

    return _factory
