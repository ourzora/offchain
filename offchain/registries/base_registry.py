from typing import Type, TypeVar

T = TypeVar("T")


class BaseRegistry:
    @staticmethod
    def get_all() -> list[T]:
        raise NotImplementedError

    @staticmethod
    def add(model_cls: Type[T], *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def validate(model_cls: Type[T], *args, **kwargs):
        pass

    @classmethod
    def register(cls, model_cls=Type[T]) -> Type[T]:
        """Decorator that registers entities."""

        def wrap(model_cls: T = model_cls):
            assert model_cls is not None, "Invalid usage, expect a class"
            cls.validate(model_cls)
            cls.add(model_cls)
            return model_cls

        if model_cls is None:
            return wrap

        return wrap()
