from unittest import TestCase

from hackle.internal.user.identifiers_builder import IdentifiersBuilder


class IdentifierBuilderTest(TestCase):

    def test_add_identifier_type이_None이면_추가하지_않는다(self):
        self.assertEqual({}, IdentifiersBuilder().add(None, 'id').build())

    def test_add_identifier_type이_str_타입이_아니면_추가하지_않는다(self):
        self.assertEqual({}, IdentifiersBuilder().add(42, 'id').build())

    def test_add_identifier_type이_128자보다_크면_추가하지_않는다(self):
        self.assertEqual({}, IdentifiersBuilder().add('a' * 129, 'id').build())

    def test_add_identifier_value가_None이면_추가하지_않는다(self):
        self.assertEqual({}, IdentifiersBuilder().add('my_id', None).build())

    def test_add_identifier_value가_512자보다_크면_추가하지_않는다(self):
        self.assertEqual({}, IdentifiersBuilder().add('my_id', 'a' * 513).build())

    def test_add(self):
        builder = IdentifiersBuilder()
        builder.add('id3', 'a')
        builder.add('id2', 'myId')
        builder.add('id1', 'hello')
        builder.add('a' * 128, 'a' * 512)
        builder.add('num1', 1)
        builder.add('invalid2', None)
        identifier = builder.build()

        self.assertEqual({
            'id1': 'hello',
            'id2': 'myId',
            'id3': 'a',
            'a' * 128: 'a' * 512,
            'num1': '1'
        }, identifier)

    def test_add_identifiers_None이면_추가하지_않는다(self):
        self.assertEqual({}, IdentifiersBuilder().add_identifiers(None).build())

    def test_add_identifiers_dict가_아니면_추가하지_않는다(self):
        self.assertEqual({}, IdentifiersBuilder().add_identifiers('must_be_dict').build())

    def test_add_identifiers(self):
        identifiers = {
            'id1': 'hello',
            'id2': 'myId',
            'id3': 'a',
            'a' * 128: 'a' * 512
        }

        builder = IdentifiersBuilder()
        builder.add_identifiers(identifiers)
        builder.add('bbb', 'ccc')
        actual = builder.build()

        self.assertEqual({
            'id1': 'hello',
            'id2': 'myId',
            'id3': 'a',
            'a' * 128: 'a' * 512,
            'bbb': 'ccc'
        }, actual)
