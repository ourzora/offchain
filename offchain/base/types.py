from enum import Enum


class StringEnum(str, Enum):
    """Allows for string comparison of enum values"""

    def __repr__(self) -> str:
        return str(self.value)

    def __str__(self):  # type: ignore[no-untyped-def]
        return str(self.value)

    @classmethod
    def contains_value(cls, value: str) -> bool:
        return value in set(str(item.value) for item in cls)

    @classmethod
    def values(cls) -> list[str]:
        return [str(item.value) for item in cls]
