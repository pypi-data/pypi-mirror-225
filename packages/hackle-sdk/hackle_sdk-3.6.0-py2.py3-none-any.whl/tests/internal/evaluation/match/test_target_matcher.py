from unittest.mock import Mock

from hackle.internal.evaluation.match.condition_matcher import ConditionMatcher
from hackle.internal.evaluation.match.condition_matcher_factory import ConditionMatcherFactory
from hackle.internal.evaluation.match.target_matcher import TargetMatcher
from hackle.internal.model.entities import Target, TargetCondition, TargetKey
from tests import base


class TargetMatcherTest(base.BaseTest):

    def setUp(self):
        self.match_values = []
        self.condition_matcher = Mock(spec=ConditionMatcher)
        self.condition_matcher.matches = Mock(side_effect=self.match_values)

        self.condition_matcher_factory = Mock(spec=ConditionMatcherFactory)
        self.condition_matcher_factory.get_condition_matcher_or_none.return_value = self.condition_matcher

        self.sut = TargetMatcher(self.condition_matcher_factory)

    def test_모든_조건이_일치하면_true(self):
        # given
        target = Target([
            self._condition(True),
            self._condition(True),
            self._condition(True),
            self._condition(True),
            self._condition(True),
            self._condition(True),
        ])

        # when
        actual = self.sut.matches(Mock(), Mock(), target)

        # then
        self.assertTrue(actual)
        self.assertEqual(6, self.condition_matcher.matches.call_count)

    def test_타겟의_조건중_하나라도_일치하지_않으면_false(self):
        # given
        target = Target([
            self._condition(True),
            self._condition(True),
            self._condition(True),
            self._condition(False),
            self._condition(True),
            self._condition(True),
        ])

        # when
        actual = self.sut.matches(Mock(), Mock(), target)

        # then
        self.assertFalse(actual)
        self.assertEqual(4, self.condition_matcher.matches.call_count)

    def _condition(self, is_match):
        self.match_values.append(is_match)
        return TargetCondition(key=TargetKey(type='USER_PROPERTY', name='age'), match=Mock())
