from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.match.segment_condition_matcher import SegmentMatcher
from hackle.internal.evaluation.match.user_condition_matcher import UserConditionMatcher
from hackle.internal.model.entities import *


class SegmentMatcherTest(TestCase):

    def setUp(self):
        self.condition_matches = []
        self.user_condition_matcher = Mock(spec=UserConditionMatcher)
        self.user_condition_matcher.matches = Mock(side_effect=self.condition_matches)
        self.sut = SegmentMatcher(self.user_condition_matcher)

    def test_Target이_비어있으면_match_false(self):
        # given
        segment = Segment(1, "seg_01", 'USER_PROPERTY', [])

        # when
        actual = self.sut.matches(Mock(), Mock(), segment)

        # then
        self.assertFalse(actual)

    def test_하나라도_매칭되는_Target이_있으면_true(self):
        # given
        segment = self._segment(
            [True, True, True, False],  # False
            [False],  # False
            [True, True]  # True
        )

        # when
        actual = self.sut.matches(Mock(), Mock(), segment)

        # then
        self.assertTrue(actual)

    def test_하나라도_매칭되는_Target이_없으면_true(self):
        # given
        segment = self._segment(
            [True, True, True, False],  # False
            [False],  # False
            [False, True]  # False
        )

        # when
        actual = self.sut.matches(Mock(), Mock(), segment)

        # then
        self.assertFalse(actual)

    def _segment(self, *target_conditions):
        targets = []
        for target_matches in target_conditions:
            conditions = []
            for conditionMatch in target_matches:
                condition = Mock(spec=TargetCondition)
                conditions.append(condition)
                self.condition_matches.append(conditionMatch)
            targets.append(Target(conditions))

        return Segment(42, "seg_01", "USER_PROPERTY", targets)
