from offchain.base.types import StringEnum


class IndexedStringEnum(StringEnum):
    @classmethod
    def from_index(cls, index: int):
        """
        Treat the enum like an array, and pull an element like an index
        Helpful when deserializing from a contract
        """
        return cls(cls.values()[index])
