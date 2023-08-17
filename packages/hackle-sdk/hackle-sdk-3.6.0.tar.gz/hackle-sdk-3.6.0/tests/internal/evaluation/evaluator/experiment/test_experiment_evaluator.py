from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluation import ExperimentEvaluation
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluator import ExperimentEvaluator
from hackle.internal.evaluation.evaluator.experiment.experiment_request import ExperimentRequest
from hackle.internal.evaluation.evaluator.remoteconfig.remote_config_request import RemoteConfigRequest
from hackle.internal.evaluation.flow.evaluation_flow import EvaluationFlow
from hackle.internal.evaluation.flow.evaluation_flow_factory import EvaluationFlowFactory
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request


class ExperimentEvaluatorTest(TestCase):

    def setUp(self):
        self.evaluation_flow_factory = Mock(spec=EvaluationFlowFactory)
        self.sut = ExperimentEvaluator(self.evaluation_flow_factory)

    def test_supports(self):
        self.assertTrue(self.sut.supports(Mock(spec=ExperimentRequest)))
        self.assertFalse(self.sut.supports(Mock(spec=RemoteConfigRequest)))

    def test__evaluate__circular_call(self):
        request = create_experiment_request()
        context = Evaluator.context()
        context.add_request(request)

        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, context)

        self.assertIn('Circular evaluation has occurred', str(actual.exception))

    def test__evaluate__flow(self):
        evaluation = Mock(spec=ExperimentEvaluation)
        evaluation_flow = Mock(spec=EvaluationFlow)
        evaluation_flow.evaluate.return_value = evaluation

        self.evaluation_flow_factory.get_evaluation_flow.return_value = evaluation_flow

        request = create_experiment_request()
        context = Evaluator.context()

        actual = self.sut.evaluate(request, context)

        self.assertEqual(evaluation, actual)
        self.assertEqual(0, len(context.stack))
