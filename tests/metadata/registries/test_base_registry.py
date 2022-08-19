from offchain.metadata.registries.base_registry import BaseRegistry


class TestBaseRegistry:
    def test_base_registry(self):
        class Registry(BaseRegistry):
            __registry = {}

            @staticmethod
            def get_all():
                return list(Registry.__registry.values())

            @staticmethod
            def add(cls):
                Registry.__registry[cls.__name__] = cls

        @Registry.register
        class Foo:
            pass

        assert Registry.get_all() == [Foo]
