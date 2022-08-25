from typing import Type, TypeVar

T = TypeVar("T")


class BaseRegistry:
    """Base Registry class

    Enables the use of a registry pattern to keep classes available in a global scope.
    Helpful for automating tests for classes.
    """

    @staticmethod
    def get_all() -> list[T]:
        raise NotImplementedError

    @staticmethod
    def add(model_cls: Type[T], *args, **kwargs):
        """Add a class to the registry

        Args:
            model_cls (Type[T]): class to be registered.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @staticmethod
    def validate(model_cls: Type[T], *args, **kwargs):
        """Validate a class before it is added to the registry.

        Args:
            model_cls (Type[T]): class to be registered.
        """
        pass

    @classmethod
    def register(cls, model_cls: Type[T]) -> Type[T]:
        """Decorator that registers classes.

        Args:
            model_cls (Type[T]): class to be registered.

        Returns:
            Type[T]: registered class.
        """

        def wrap(model_cls: T = model_cls):
            assert model_cls is not None, "Invalid usage, expect a class"
            cls.validate(model_cls)
            cls.add(model_cls)
            return model_cls

        if model_cls is None:
            return wrap

        return wrap()
