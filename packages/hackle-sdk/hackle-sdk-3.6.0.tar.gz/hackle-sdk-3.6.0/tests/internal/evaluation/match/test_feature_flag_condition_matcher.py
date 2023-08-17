from unittest import TestCase
from unittest.mock import Mock

from hackle.decision import DecisionReason
from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluation import ExperimentEvaluation
from hackle.internal.evaluation.match.experiment_condition_matcher import FeatureFlagConditionMatcher
from hackle.internal.evaluation.match.value_operator_matcher import ValueOperatorMatcher
from hackle.internal.model.entities import TargetCondition, TargetKey, TargetMatch
from hackle.internal.workspace.workspace import Workspace
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request
from tests.internal.model.test_entities import create_experiment


class FeatureFlagConditionMatcherTest(TestCase):

    def setUp(self):
        self.evaluator = Mock(spec=Evaluator)
        self.value_operator_matcher = Mock(spec=ValueOperatorMatcher)
        self.sut = FeatureFlagConditionMatcher(self.evaluator, self.value_operator_matcher)
        self.context = Evaluator.context()

    def test_key_is_not_int(self):
        # given
        experiment = create_experiment(type='FEATURE_FLAG')
        request = create_experiment_request(experiment=experiment)
        condition = TargetCondition(
            TargetKey('FEATURE_FLAG', 'string'),
            TargetMatch('MATCH', 'IN', 'BOOLEAN', [True])
        )

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.matches(request, Evaluator.context(), condition)

        # then
        self.assertEqual('Invalid key [FEATURE_FLAG, string]', str(actual.exception))

    def test_experiment_not_found(self):
        # given
        experiment = create_experiment(type='FEATURE_FLAG')
        request = create_experiment_request(experiment=experiment)
        condition = TargetCondition(
            TargetKey('FEATURE_FLAG', '42'),
            TargetMatch('MATCH', 'IN', 'BOOLEAN', [True])
        )

        # when
        actual = self.sut.matches(request, Evaluator.context(), condition)

        # then
        self.assertFalse(actual)

    # noinspection PyMethodMayBeStatic
    def __request(self, experiment):
        workspace = Mock(spec=Workspace)
        workspace.get_feature_flag_or_none.return_value = experiment
        return create_experiment_request(workspace=workspace, experiment=experiment)

    def test_new_evaluation(self):
        # given
        experiment = create_experiment(type='FEATURE_FLAG')
        request = self.__request(experiment)
        condition = TargetCondition(
            TargetKey('FEATURE_FLAG', '42'),
            TargetMatch('MATCH', 'IN', 'BOOLEAN', [True])
        )

        evaluation = ExperimentEvaluation.of(request, self.context, request.experiment.variations[0],
                                             DecisionReason.DEFAULT_RULE)
        self.evaluator.evaluate.return_value = evaluation
        self.value_operator_matcher.matches.return_value = True

        # when
        actual = self.sut.matches(request, self.context, condition)

        # then
        self.assertEqual(True, actual)
        self.evaluator.evaluate.assert_called_once()
        self.assertEqual(evaluation, self.context.get_evaluation_or_none(experiment))

    def test_alreadt_evaluated(self):
        # given
        experiment = create_experiment(type='FEATURE_FLAG')
        request = self.__request(experiment)
        condition = TargetCondition(
            TargetKey('FEATURE_FLAG', '42'),
            TargetMatch('MATCH', 'IN', 'BOOLEAN', [True])
        )

        evaluation = ExperimentEvaluation.of(request, self.context, request.experiment.variations[0],
                                             DecisionReason.DEFAULT_RULE)
        self.context.add_evaluation(evaluation)
        self.value_operator_matcher.matches.return_value = True

        # when
        actual = self.sut.matches(request, self.context, condition)

        # then
        self.assertEqual(True, actual)
        self.evaluator.evaluate.assert_not_called()
        self.assertEqual(evaluation, self.context.get_evaluation_or_none(experiment))
