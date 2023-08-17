from unittest import TestCase

from hackle.internal.evaluation.match.user_condition_matcher import UserValueResolver
from hackle.internal.model.entities import TargetKey
from hackle.internal.user.internal_hackle_user import InternalHackleUser


class UserValueResolverTest(TestCase):

    def setUp(self):
        self.sut = UserValueResolver()

    def test_USER_ID(self):
        user = InternalHackleUser(
            identifiers={
                '$id': 'test_user_id',
                '$deviceId': 'test_device_id',
                'custom_id': 'test_custom_id'
            },
            properties={}
        )
        self.assertEqual('test_user_id', self.sut.resolve_or_none(user, TargetKey('USER_ID', '$id')))
        self.assertEqual('test_device_id', self.sut.resolve_or_none(user, TargetKey('USER_ID', '$deviceId')))
        self.assertEqual('test_custom_id', self.sut.resolve_or_none(user, TargetKey('USER_ID', 'custom_id')))

    def test_USER_PROPERTY(self):
        user = InternalHackleUser(identifiers={'$id': 'test_user_id'}, properties={'age': 42})
        actual = self.sut.resolve_or_none(user, TargetKey('USER_PROPERTY', 'age'))
        self.assertEqual(42, actual)

    def test_HACKLE_PROPERTY(self):
        user = InternalHackleUser(identifiers={'$id': 'test_user_id'}, properties={'age': 42})
        actual = self.sut.resolve_or_none(user, TargetKey('HACKLE_PROPERTY', 'platform'))
        self.assertIsNone(actual)

    def test_SEGMENT(self):
        user = InternalHackleUser(identifiers={'$id': 'test_user_id'}, properties={'age': 42})
        with self.assertRaises(Exception) as actual:
            self.sut.resolve_or_none(user, TargetKey('SEGMENT', 'SEGMENT'))
        self.assertEqual('Unsupported target_key.type [SEGMENT]', str(actual.exception))
