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
    def add(model_cls: Type[T], *args, **kwargs):  # type: ignore[no-untyped-def]
        """Add a class to the registry

        Args:
            model_cls (Type[T]): class to be registered.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    @staticmethod
    def validate(model_cls: Type[T], *args, **kwargs):  # type: ignore[no-untyped-def]
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

        def wrap(model_cls: T = model_cls):  # type: ignore[assignment, no-untyped-def]
            assert model_cls is not None, "Invalid usage, expect a class"
            cls.validate(model_cls)  # type: ignore[arg-type]
            cls.add(model_cls)  # type: ignore[arg-type]
            return model_cls

        if model_cls is None:
            return wrap

        return wrap()  # type: ignore[no-any-return]
