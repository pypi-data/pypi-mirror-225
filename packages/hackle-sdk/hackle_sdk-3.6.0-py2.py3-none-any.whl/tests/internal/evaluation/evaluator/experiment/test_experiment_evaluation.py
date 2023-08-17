from unittest import TestCase
from unittest.mock import Mock

from hackle.decision import DecisionReason
from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluation import ExperimentEvaluation
from hackle.internal.evaluation.evaluator.experiment.experiment_request import ExperimentRequest
from hackle.internal.model.entities import ParameterConfiguration
from hackle.internal.user.internal_hackle_user import InternalHackleUser
from hackle.internal.workspace.workspace import Workspace
from tests.internal.model.test_entities import create_experiment, create_variation


class ExperimentEvaluationTest(TestCase):

    def test_create_by_variation(self):
        experiment = create_experiment(
            id=42,
            key=50,
            variations=[
                create_variation(id=320, key='A', config_id=99),
                create_variation(id=321, key='B', config_id=100),
            ]
        )

        variation = experiment.get_variation_by_id_or_none(321)

        config = Mock(sepc=ParameterConfiguration)
        workspace = Mock(spec=Workspace)
        workspace.get_parameter_configuration_or_none.return_value = config

        user = InternalHackleUser.builder().build()
        request = ExperimentRequest.of(workspace, user, experiment, 'H')

        context = Evaluator.context()
        context.add_evaluation(Mock(spec=Evaluator.Evaluation))

        evaluation = ExperimentEvaluation.of(request, context, variation, DecisionReason.TRAFFIC_ALLOCATED)

        self.assertEqual(DecisionReason.TRAFFIC_ALLOCATED, evaluation.reason)
        self.assertEqual(1, len(evaluation.target_evaluations))
        self.assertEqual(experiment, evaluation.experiment)
        self.assertEqual(321, evaluation.variation_id)
        self.assertEqual('B', evaluation.variation_key)
        self.assertEqual(config, evaluation.config)

    def test_create_by_variation_config_none(self):
        experiment = create_experiment(
            id=42,
            key=50,
            variations=[
                create_variation(id=320, key='A'),
                create_variation(id=321, key='B'),
            ]
        )

        variation = experiment.get_variation_by_id_or_none(321)

        workspace = Mock(spec=Workspace)

        user = InternalHackleUser.builder().build()
        request = ExperimentRequest.of(workspace, user, experiment, 'H')

        context = Evaluator.context()
        context.add_evaluation(Mock(spec=Evaluator.Evaluation))

        evaluation = ExperimentEvaluation.of(request, context, variation, DecisionReason.TRAFFIC_ALLOCATED)

        self.assertEqual(DecisionReason.TRAFFIC_ALLOCATED, evaluation.reason)
        self.assertEqual(1, len(evaluation.target_evaluations))
        self.assertEqual(experiment, evaluation.experiment)
        self.assertEqual(321, evaluation.variation_id)
        self.assertEqual('B', evaluation.variation_key)
        self.assertIsNone(evaluation.config)

    def test_create_by_default(self):
        experiment = create_experiment(
            id=42,
            key=50,
            variations=[
                create_variation(id=320, key='A'),
                create_variation(id=321, key='B'),
            ]
        )

        workspace = Mock(spec=Workspace)

        user = InternalHackleUser.builder().build()
        request = ExperimentRequest.of(workspace, user, experiment, 'A')

        evaluation = ExperimentEvaluation.of_default(request, Evaluator.context(), DecisionReason.TRAFFIC_NOT_ALLOCATED)

        self.assertEqual(DecisionReason.TRAFFIC_NOT_ALLOCATED, evaluation.reason)
        self.assertEqual(0, len(evaluation.target_evaluations))
        self.assertEqual(experiment, evaluation.experiment)
        self.assertEqual(320, evaluation.variation_id)
        self.assertEqual('A', evaluation.variation_key)
        self.assertIsNone(evaluation.config)

    def test_create_by_default_null(self):
        experiment = create_experiment(
            id=42,
            key=50,
            variations=[
                create_variation(id=320, key='A'),
                create_variation(id=321, key='B'),
            ]
        )

        workspace = Mock(spec=Workspace)

        user = InternalHackleUser.builder().build()
        request = ExperimentRequest.of(workspace, user, experiment, 'C')

        evaluation = ExperimentEvaluation.of_default(request, Evaluator.context(), DecisionReason.TRAFFIC_NOT_ALLOCATED)

        self.assertEqual(DecisionReason.TRAFFIC_NOT_ALLOCATED, evaluation.reason)
        self.assertEqual(0, len(evaluation.target_evaluations))
        self.assertEqual(experiment, evaluation.experiment)
        self.assertEqual(None, evaluation.variation_id)
        self.assertEqual('C', evaluation.variation_key)
        self.assertIsNone(evaluation.config)

    def test_copy_with(self):
        evaluation = ExperimentEvaluation(DecisionReason.TRAFFIC_ALLOCATED, Mock(), Mock(), 42, 'A', Mock())

        actual = evaluation.copy_with(DecisionReason.TRAFFIC_ALLOCATED_BY_TARGETING)

        self.assertEqual(DecisionReason.TRAFFIC_ALLOCATED_BY_TARGETING, actual.reason)
        self.assertEqual(evaluation.target_evaluations, actual.target_evaluations)
        self.assertEqual(evaluation.experiment, actual.experiment)
        self.assertEqual(evaluation.variation_id, actual.variation_id)
        self.assertEqual(evaluation.variation_key, actual.variation_key)
        self.assertEqual(evaluation.config, actual.config)
