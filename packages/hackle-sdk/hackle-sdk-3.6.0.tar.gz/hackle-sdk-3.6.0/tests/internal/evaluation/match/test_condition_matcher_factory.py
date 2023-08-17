from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.match.condition_matcher_factory import ConditionMatcherFactory
from hackle.internal.evaluation.match.experiment_condition_matcher import ExperimentConditionMatcher
from hackle.internal.evaluation.match.segment_condition_matcher import SegmentConditionMatcher
from hackle.internal.evaluation.match.user_condition_matcher import UserConditionMatcher


class ConditionMatcherFactoryTest(TestCase):

    def test_get_matcher(self):
        sut = ConditionMatcherFactory(Mock())
        self.assertIsInstance(sut.get_condition_matcher_or_none('USER_ID'), UserConditionMatcher)
        self.assertIsInstance(sut.get_condition_matcher_or_none('USER_PROPERTY'), UserConditionMatcher)
        self.assertIsInstance(sut.get_condition_matcher_or_none('HACKLE_PROPERTY'), UserConditionMatcher)
        self.assertIsInstance(sut.get_condition_matcher_or_none('SEGMENT'), SegmentConditionMatcher)
        self.assertIsInstance(sut.get_condition_matcher_or_none('AB_TEST'), ExperimentConditionMatcher)
        self.assertIsInstance(sut.get_condition_matcher_or_none('FEATURE_FLAG'), ExperimentConditionMatcher)
        self.assertIsNone(sut.get_condition_matcher_or_none('INVALID'))
