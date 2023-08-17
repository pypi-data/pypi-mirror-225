from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.match.user_condition_matcher import UserValueResolver, UserConditionMatcher
from hackle.internal.evaluation.match.value_operator_matcher import ValueOperatorMatcher
from hackle.internal.model.entities import TargetCondition, TargetKey, TargetMatch


class UserConditionMatcherTest(TestCase):

    def setUp(self):
        self.user_value_resolver = Mock(spec=UserValueResolver)
        self.value_operator_matcher = Mock(spec=ValueOperatorMatcher)
        self.sut = UserConditionMatcher(self.user_value_resolver, self.value_operator_matcher)

    def test_Key에_해당하는_UserValue가_없으면_match_false(self):
        # given
        condition = TargetCondition(
            TargetKey('USER_PROPERTY', "age"),
            TargetMatch('MATCH', 'IN', 'NUMBER', [30])
        )
        self.user_value_resolver.resolve_or_none.return_value = None

        # when
        actual = self.sut.matches(Mock(), Mock(), condition)

        # then
        self.assertFalse(actual)

    def test_Key에_해당하는_UserValue로_매칭한다(self):
        # given
        condition = TargetCondition(
            TargetKey('USER_PROPERTY', "age"),
            TargetMatch('MATCH', 'IN', 'NUMBER', [30])
        )
        self.user_value_resolver.resolve_or_none.return_value = "test_user_value"
        self.value_operator_matcher.matches.return_value = True

        # when
        actual = self.sut.matches(Mock(), Mock(), condition)

        # then
        self.assertTrue(actual)

    def test_Key에_해당하는_UserValue로_매칭한다_2(self):
        # given
        condition = TargetCondition(
            TargetKey('USER_PROPERTY', "gender"),
            TargetMatch('MATCH', 'IN', 'NUMBER', [0])
        )
        self.user_value_resolver.resolve_or_none.return_value = 0
        self.value_operator_matcher.matches.return_value = True

        # when
        actual = self.sut.matches(Mock(), Mock(), condition)

        # then
        self.assertTrue(actual)

    def test_Key에_해당하는_UserValue로_매칭한다_3(self):
        # given
        condition = TargetCondition(
            TargetKey('USER_PROPERTY', "is_admin"),
            TargetMatch('MATCH', 'IN', 'BOOLEAN', [False])
        )
        self.user_value_resolver.resolve_or_none.return_value = False
        self.value_operator_matcher.matches.return_value = True

        # when
        actual = self.sut.matches(Mock(), Mock(), condition)

        # then
        self.assertTrue(actual)
