from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.match.experiment_condition_matcher import AbTestConditionMatcher, \
    FeatureFlagConditionMatcher, \
    ExperimentConditionMatcher
from hackle.internal.model.entities import TargetCondition, TargetKey, TargetMatch
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request
from tests.internal.model.test_entities import create_experiment


class ExperimentConditionMatcherTest(TestCase):

    def setUp(self):
        self.ab_test_matcher = Mock(spec=AbTestConditionMatcher)
        self.feature_flag_matcher = Mock(spec=FeatureFlagConditionMatcher)
        self.sut = ExperimentConditionMatcher(self.ab_test_matcher, self.feature_flag_matcher)

    def test_ab_test(self):
        # given
        request = create_experiment_request(experiment=create_experiment(type='AB_TEST'))
        condition = TargetCondition(
            TargetKey('AB_TEST', '42'),
            TargetMatch('MATCH', 'IN', 'STRING', ['A'])
        )

        self.ab_test_matcher.matches.return_value = True

        # when
        actual = self.sut.matches(request, Evaluator.context(), condition)

        # then
        self.assertTrue(actual)
        self.ab_test_matcher.matches.assert_called_once()

    def test_feature_flag(self):
        # given
        request = create_experiment_request(experiment=create_experiment(type='FEATURE_FLAG'))
        condition = TargetCondition(
            TargetKey('FEATURE_FLAG', '42'),
            TargetMatch('MATCH', 'IN', 'BOOLEAN', [True])
        )

        self.ab_test_matcher.matches.return_value = True

        # when
        actual = self.sut.matches(request, Evaluator.context(), condition)

        # then
        self.assertTrue(actual)
        self.feature_flag_matcher.matches.assert_called_once()

    def test_unsupported(self):
        request = create_experiment_request(experiment=create_experiment())

        def verify(key_type):
            condition = TargetCondition(
                TargetKey(key_type, '42'),
                TargetMatch('MATCH', 'IN', 'STRING', ['A'])
            )
            with self.assertRaises(Exception):
                self.sut.matches(request, Evaluator.context(), condition)

        verify('USER_ID')
        verify('USER_PROPERTY')
        verify('HACKLE_PROPERTY')
        verify('SEGMENT')
