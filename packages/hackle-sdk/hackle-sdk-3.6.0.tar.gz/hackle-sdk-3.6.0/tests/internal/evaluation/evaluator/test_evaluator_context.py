from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluation import ExperimentEvaluation
from hackle.internal.evaluation.evaluator.remoteconfig.remote_config_evaluation import RemoteConfigEvaluation
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request
from tests.internal.model.test_entities import create_experiment


class EvaluatorContextTest(TestCase):
    def test_stack(self):
        context = Evaluator.context()
        self.assertEqual(0, len(context.stack))

        request_1 = create_experiment_request(experiment=create_experiment(id=1))
        context.add_request(request_1)
        stack_1 = context.stack
        self.assertEqual(1, len(stack_1))

        request_2 = create_experiment_request(experiment=create_experiment(id=2))
        context.add_request(request_2)
        stack_2 = context.stack
        self.assertEqual(2, len(stack_2))

        context.remove_request(request_2)
        self.assertEqual(1, len(context.stack))

        context.remove_request(request_1)
        self.assertEqual(0, len(context.stack))

        self.assertEqual(1, len(stack_1))
        self.assertEqual(2, len(stack_2))

    def test_target_evaluations(self):
        context = Evaluator.context()
        self.assertEqual(0, len(context.target_evaluations))

        experiment = create_experiment(id=1)

        evaluation_1 = Mock(spec=RemoteConfigEvaluation)
        context.add_evaluation(evaluation_1)
        target_evaluations_1 = context.target_evaluations
        self.assertEqual(1, len(target_evaluations_1))
        self.assertEqual(None, context.get_evaluation_or_none(experiment))

        evaluation_2 = Mock(spec=ExperimentEvaluation)
        evaluation_2.experiment = experiment
        context.add_evaluation(evaluation_2)
        target_evaluations_2 = context.target_evaluations
        self.assertEqual(1, len(target_evaluations_1))
        self.assertEqual(2, len(target_evaluations_2))
        self.assertEqual(evaluation_2, context.get_evaluation_or_none(experiment))
        self.assertEqual(None, context.get_evaluation_or_none(create_experiment(id=2)))
