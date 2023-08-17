from unittest import TestCase
from unittest.mock import Mock

from hackle.decision import DecisionReason
from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluation import ExperimentEvaluation
from hackle.internal.evaluation.evaluator.remoteconfig.remote_config_evaluation import RemoteConfigEvaluation
from hackle.internal.evaluation.match.experiment_condition_matcher import AbTestConditionMatcher
from hackle.internal.evaluation.match.value_operator_matcher import ValueOperatorMatcher
from hackle.internal.model.entities import TargetCondition, TargetKey, TargetMatch
from hackle.internal.workspace.workspace import Workspace
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request
from tests.internal.model.test_entities import create_experiment


class AbTestConditionMatcherTest(TestCase):

    def setUp(self):
        self.evaluator = Mock(spec=Evaluator)
        self.value_operator_matcher = Mock(spec=ValueOperatorMatcher)
        self.sut = AbTestConditionMatcher(self.evaluator, self.value_operator_matcher)
        self.context = Evaluator.context()

    def test_key_is_not_int(self):
        # given
        experiment = create_experiment(type='AB_TEST')
        request = create_experiment_request(experiment=experiment)
        condition = TargetCondition(
            TargetKey('AB_TEST', 'string'),
            TargetMatch('MATCH', 'IN', 'STRING', ['A'])
        )

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.matches(request, Evaluator.context(), condition)

        # then
        self.assertEqual('Invalid key [AB_TEST, string]', str(actual.exception))

    def test_experiment_not_found(self):
        # given
        experiment = create_experiment(type='AB_TEST')
        request = create_experiment_request(experiment=experiment)
        condition = TargetCondition(
            TargetKey('AB_TEST', '42'),
            TargetMatch('MATCH', 'IN', 'STRING', ['A'])
        )

        # when
        actual = self.sut.matches(request, Evaluator.context(), condition)

        # then
        self.assertFalse(actual)

    # noinspection PyMethodMayBeStatic
    def __request(self, experiment):
        workspace = Mock(spec=Workspace)
        workspace.get_experiment_or_none.return_value = experiment
        return create_experiment_request(workspace=workspace, experiment=experiment)

    def test_not_matched_reason(self):
        def check(reason):
            # given
            experiment = create_experiment(type='AB_TEST')
            request = self.__request(experiment=experiment)
            condition = TargetCondition(
                TargetKey('AB_TEST', '42'),
                TargetMatch('MATCH', 'IN', 'STRING', ['A'])
            )

            evaluation = ExperimentEvaluation.of(request, self.context, request.experiment.variations[0], reason)
            self.evaluator.evaluate.return_value = evaluation

            # when
            actual = self.sut.matches(request, Evaluator.context(), condition)

            # then
            self.assertFalse(actual)

        check(DecisionReason.EXPERIMENT_DRAFT)
        check(DecisionReason.EXPERIMENT_PAUSED)
        check(DecisionReason.NOT_IN_MUTUAL_EXCLUSION_EXPERIMENT)
        check(DecisionReason.VARIATION_DROPPED)
        check(DecisionReason.NOT_IN_EXPERIMENT_TARGET)
        self.value_operator_matcher.matches.assert_not_called()

    def test_matched_reason(self):
        def check(reason):
            # given
            experiment = create_experiment(type='AB_TEST')
            request = self.__request(experiment=experiment)
            condition = TargetCondition(
                TargetKey('AB_TEST', '42'),
                TargetMatch('MATCH', 'IN', 'STRING', ['A'])
            )

            evaluation = ExperimentEvaluation.of(request, self.context, request.experiment.variations[0], reason)
            self.evaluator.evaluate.return_value = evaluation
            self.value_operator_matcher.matches.return_value = True

            # when
            actual = self.sut.matches(request, Evaluator.context(), condition)

            # then
            self.assertTrue(actual)

        check(DecisionReason.OVERRIDDEN)
        check(DecisionReason.TRAFFIC_ALLOCATED)
        check(DecisionReason.TRAFFIC_ALLOCATED_BY_TARGETING)
        check(DecisionReason.EXPERIMENT_COMPLETED)

    def test_already_evaluated_experiment(self):
        # given
        experiment = create_experiment(type='AB_TEST')
        request = self.__request(experiment=experiment)
        condition = TargetCondition(
            TargetKey('AB_TEST', '42'),
            TargetMatch('MATCH', 'IN', 'STRING', ['A'])
        )
        evaluation = ExperimentEvaluation.of(request, self.context, request.experiment.variations[0],
                                             DecisionReason.TRAFFIC_ALLOCATED)
        self.evaluator.evaluate.return_value = evaluation
        self.value_operator_matcher.matches.return_value = True

        self.context.add_evaluation(evaluation)

        # when
        actual = self.sut.matches(request, self.context, condition)

        # then
        self.assertTrue(actual)
        self.evaluator.evaluate.assert_not_called()
        self.assertEqual(1, len(self.context.target_evaluations))

    def test_replace_reason(self):
        # given
        experiment = create_experiment(type='AB_TEST')
        request = self.__request(experiment=experiment)
        condition = TargetCondition(
            TargetKey('AB_TEST', '42'),
            TargetMatch('MATCH', 'IN', 'STRING', ['A'])
        )
        evaluation = ExperimentEvaluation.of(request, self.context, request.experiment.variations[0],
                                             DecisionReason.TRAFFIC_ALLOCATED)
        self.evaluator.evaluate.return_value = evaluation
        self.value_operator_matcher.matches.return_value = True

        # when
        actual = self.sut.matches(request, self.context, condition)

        # then
        self.assertTrue(actual)
        self.assertEqual(DecisionReason.TRAFFIC_ALLOCATED_BY_TARGETING,
                         self.context.get_evaluation_or_none(experiment).reason)

    def test_use_evaluation_directly(self):
        # given
        experiment = create_experiment(type='AB_TEST')
        request = self.__request(experiment=experiment)
        condition = TargetCondition(
            TargetKey('AB_TEST', '42'),
            TargetMatch('MATCH', 'IN', 'STRING', ['A'])
        )
        evaluation = ExperimentEvaluation.of(request, self.context, request.experiment.variations[0],
                                             DecisionReason.OVERRIDDEN)
        self.evaluator.evaluate.return_value = evaluation
        self.value_operator_matcher.matches.return_value = True

        # when
        actual = self.sut.matches(request, self.context, condition)

        # then
        self.assertTrue(actual)
        self.assertEqual(evaluation, self.context.get_evaluation_or_none(experiment))

    def test_unexpected_evaluation(self):
        # given
        experiment = create_experiment(type='AB_TEST')
        request = self.__request(experiment=experiment)
        condition = TargetCondition(
            TargetKey('AB_TEST', '42'),
            TargetMatch('MATCH', 'IN', 'STRING', ['A'])
        )
        evaluation = Mock(spec=RemoteConfigEvaluation)
        self.evaluator.evaluate.return_value = evaluation
        self.value_operator_matcher.matches.return_value = True

        # when
        with self.assertRaises(Exception):
            self.sut.matches(request, self.context, condition)
