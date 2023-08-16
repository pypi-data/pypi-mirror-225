from types import MemberDescriptorType as member_descriptor

from .logging import get_logger


def extract_from(value, *, prefix):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from extract_from(item, prefix=f"{prefix}-{key}")

    elif hasattr(value, "_asdict"):
        yield from extract_from(value._asdict(), prefix=prefix)

    elif isinstance(value, (tuple, list)):
        for index, item in enumerate(value):
            yield from extract_from(item, prefix=f"{prefix}-{index}")

    elif isinstance(value, int):
        yield (prefix, int(value))

    elif isinstance(value, float):
        yield (prefix, value)

    else:
        get_logger().debug(f"Ignoring {value} as not a number.")


class for_class:
    def __init__(self, klass):
        self.__props = [
            name
            for name, value in vars(klass).items()
            if isinstance(value, (property, member_descriptor))
            and not name.startswith("_")
        ]

    def __call__(self, instance):
        for prop in self.__props:
            value = getattr(instance, prop)
            yield from extract_from(value, prefix=prop)
