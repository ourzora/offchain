from offchain.metadata.registries.base_registry import BaseRegistry


class TestBaseRegistry:
    def test_base_registry(self):  # type: ignore[no-untyped-def]
        class Registry(BaseRegistry):
            __registry = {}  # type: ignore[var-annotated]

            @staticmethod
            def get_all():  # type: ignore[no-untyped-def]
                return list(Registry.__registry.values())

            @staticmethod
            def add(cls):  # type: ignore[no-untyped-def]
                Registry.__registry[cls.__name__] = cls

        @Registry.register
        class Foo:
            pass

        assert Registry.get_all() == [Foo]  # type: ignore[no-untyped-call]
