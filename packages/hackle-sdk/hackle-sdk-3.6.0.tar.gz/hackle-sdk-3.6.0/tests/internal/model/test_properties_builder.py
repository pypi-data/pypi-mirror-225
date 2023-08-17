from hackle.internal.model.properties_builder import PropertiesBuilder
from tests import base


class PropertiesBuilderTest(base.BaseTest):

    def test_raw_value_valid_build(self):
        self.assertEqual(PropertiesBuilder().add("key1", 1).build(), {"key1": 1})
        self.assertEqual(PropertiesBuilder().add("key1", "1").build(), {"key1": "1"})
        self.assertEqual(PropertiesBuilder().add("key1", True).build(), {"key1": True})
        self.assertEqual(PropertiesBuilder().add("key1", False).build(), {"key1": False})

    def test_raw_value_invalid(self):
        self.assertEqual(PropertiesBuilder().add("key1", {id: "a"}).build(), {})

    def test_array_value(self):
        self.assertEqual(PropertiesBuilder().add("key1", [1, 2, 3]).build(), {"key1": [1, 2, 3]})
        self.assertEqual(PropertiesBuilder().add("key1", ["1", "2", "3"]).build(), {"key1": ["1", "2", "3"]})
        self.assertEqual(PropertiesBuilder().add("key1", ["1", 2, "3"]).build(), {"key1": ["1", 2, "3"]})
        self.assertEqual(PropertiesBuilder().add("key1", [1, 2, 3, None, 4]).build(), {"key1": [1, 2, 3, 4]})
        self.assertEqual(PropertiesBuilder().add("key1", [True, False]).build(), {"key1": []})
        self.assertEqual(PropertiesBuilder().add("key1", ["a" * 1024]).build(), {"key1": ["a" * 1024]})
        self.assertEqual(PropertiesBuilder().add("key1", ["a" * 1025]).build(), {"key1": []})

    def test_max_property_size_is_128(self):
        builder = PropertiesBuilder()
        for i in range(128):
            builder.add(str(i), i)

        self.assertEqual(128, len(builder.build()))

        builder.add("key", 42)
        properties = builder.build()
        self.assertEqual(128, len(properties))
        self.assertIsNone(properties.get("key"))

    def test_max_key_length_is_128(self):
        builder = PropertiesBuilder()

        builder.add("a" * 128, 128)
        self.assertEqual(1, len(builder.build()))

        builder.add("a" * 129, 1289)
        self.assertEqual(1, len(builder.build()))

    def test_properties(self):
        properties = {
            "k1": "v1",
            "k2": 2,
            "k3": True,
            "k4": False,
            "k5": [1, 2, 3],
            "k6": ["1", "2", "3"],
            "k7": None
        }

        actual = PropertiesBuilder().add_properties(properties).build()

        self.assertEqual(6, len(actual))
        self.assertEqual({
            "k1": "v1",
            "k2": 2,
            "k3": True,
            "k4": False,
            "k5": [1, 2, 3],
            "k6": ["1", "2", "3"],
        }, actual)

        self.assertEqual({}, PropertiesBuilder().add_properties(None).build())
        self.assertEqual({}, PropertiesBuilder().add_properties("str").build())
