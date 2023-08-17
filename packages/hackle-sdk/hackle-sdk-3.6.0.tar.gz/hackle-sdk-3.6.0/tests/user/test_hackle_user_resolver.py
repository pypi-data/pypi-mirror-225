from hackle.internal.user.hackle_user_resolver import HackleUserResolver
from hackle.internal.user.internal_hackle_user import InternalHackleUser
from hackle.model import User, HackleUser
from tests import base


class HackleUserResolverTest(base.BaseTest):

    def setUp(self):
        self.sut = HackleUserResolver()

    def test_user가_None이면_None리턴(self):
        # given
        user = None

        # when
        actual = self.sut.resolve_or_none(user)

        # then
        self.assertIsNone(actual)

    def test_user가_User_or_HackleUser_타입이_아니면_None_리턴(self):
        # given
        user = 'string user'

        # when
        actual = self.sut.resolve_or_none(user)

        # then
        self.assertIsNone(actual)

    def test_user가_User_타입이면_HackleUser로_변환하여_처리한다(self):
        # given
        user = User(id='test_id', properties={'age': 30, 'grade': 'GOLD'})

        # when
        actual = self.sut.resolve_or_none(user)

        # then
        self.assertEqual(
            InternalHackleUser(identifiers={'$id': 'test_id'}, properties={'age': 30, 'grade': 'GOLD'}),
            actual
        )

    def test_user가_HackleUser_타입이면_그대로_처리한다(self):
        # given
        user = HackleUser(
            id='test_id',
            user_id='test_user_id',
            device_id='test_device_id',
            identifiers={
                'custom_id': 'test_custom_id'
            },
            properties={
                'grade': 'GOLD',
                'age': 30
            }
        )

        # when
        actual = self.sut.resolve_or_none(user)

        # then
        self.assertEqual(
            InternalHackleUser(
                identifiers={
                    '$id': 'test_id',
                    '$userId': 'test_user_id',
                    '$deviceId': 'test_device_id',
                    'custom_id': 'test_custom_id'
                },
                properties={
                    'age': 30,
                    'grade': 'GOLD'
                }
            ),
            actual
        )

    def test_유효하지않은_properties는_필터링한다(self):
        # given
        user = HackleUser(
            id='test_id',
            user_id='test_user_id',
            device_id='test_device_id',
            identifiers={
                'custom_id': 'test_custom_id'
            },
            properties={
                'grade': 'GOLD',
                'age': 30,
                'a' * 129: 'too long key',
                'object_value_is_invalid': {1: 1}
            }
        )

        # when
        actual = self.sut.resolve_or_none(user)

        # then
        self.assertEqual(
            InternalHackleUser(
                identifiers={
                    '$id': 'test_id',
                    '$userId': 'test_user_id',
                    '$deviceId': 'test_device_id',
                    'custom_id': 'test_custom_id'
                },
                properties={
                    'age': 30,
                    'grade': 'GOLD'
                }
            ),
            actual
        )

    def test_id가_없는_경우(self):
        # given
        user = HackleUser(
            user_id='test_user_id',
            device_id='test_device_id',
            identifiers={
                'custom_id': 'test_custom_id'
            },
            properties={
                'grade': 'GOLD',
                'age': 30
            }
        )

        # when
        actual = self.sut.resolve_or_none(user)

        # then
        self.assertEqual(
            InternalHackleUser(
                identifiers={
                    '$userId': 'test_user_id',
                    '$deviceId': 'test_device_id',
                    'custom_id': 'test_custom_id'
                },
                properties={
                    'age': 30,
                    'grade': 'GOLD'
                }
            ),
            actual
        )

    def test_user_id가_없는_경우(self):
        # given
        user = HackleUser(
            id='test_id',
            device_id='test_device_id',
            identifiers={
                'custom_id': 'test_custom_id'
            },
            properties={
                'grade': 'GOLD',
                'age': 30
            }
        )

        # when
        actual = self.sut.resolve_or_none(user)

        # then
        self.assertEqual(
            InternalHackleUser(
                identifiers={
                    '$id': 'test_id',
                    '$deviceId': 'test_device_id',
                    'custom_id': 'test_custom_id'
                },
                properties={
                    'age': 30,
                    'grade': 'GOLD'
                }
            ),
            actual
        )

    def test_device_id가_없는_경우(self):
        # given
        user = HackleUser(
            id='test_id',
            user_id='test_user_id',
            identifiers={
                'custom_id': 'test_custom_id'
            },
            properties={
                'grade': 'GOLD',
                'age': 30
            }
        )

        # when
        actual = self.sut.resolve_or_none(user)

        # then
        self.assertEqual(
            InternalHackleUser(
                identifiers={
                    '$id': 'test_id',
                    '$userId': 'test_user_id',
                    'custom_id': 'test_custom_id'
                },
                properties={
                    'age': 30,
                    'grade': 'GOLD'
                }
            ),
            actual
        )

    def test_식별자가_하나도_없는경우_None_리턴(self):
        # given
        user = HackleUser(
            properties={
                'grade': 'GOLD',
                'age': 30
            }
        )

        # when
        actual = self.sut.resolve_or_none(user)

        # then
        self.assertIsNone(actual)

    def test_propertis가_None인_경우(self):
        # given
        user = HackleUser(
            id='test_id',
            user_id='test_user_id',
            identifiers={
                'custom_id': 'test_custom_id'
            }
        )

        # when
        actual = self.sut.resolve_or_none(user)

        # then
        self.assertEqual(
            InternalHackleUser(
                identifiers={
                    '$id': 'test_id',
                    '$userId': 'test_user_id',
                    'custom_id': 'test_custom_id'
                },
                properties={}
            ),
            actual
        )
