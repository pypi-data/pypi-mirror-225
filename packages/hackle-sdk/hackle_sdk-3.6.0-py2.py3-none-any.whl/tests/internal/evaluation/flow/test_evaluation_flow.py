from unittest import TestCase
from unittest.mock import Mock

from hackle.decision import DecisionReason
from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluation import ExperimentEvaluation
from hackle.internal.evaluation.flow.evaluation_flow import EvaluationFlow
from hackle.internal.evaluation.flow.flow_evaluator import FlowEvaluator
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request


class EvaluationFlowTest(TestCase):

    def test__evaluate__end(self):
        request = create_experiment_request()
        evaluation = EvaluationFlow().evaluate(request, Evaluator.context())
        self.assertEqual(DecisionReason.TRAFFIC_NOT_ALLOCATED, evaluation.reason)
        self.assertEqual('A', evaluation.variation_key)

    def test__evaluate__flow(self):
        evaluation = Mock(spec=ExperimentEvaluation)
        next_flow = Mock(spec=EvaluationFlow)
        flow_evaluator = Mock(spec=FlowEvaluator)
        flow_evaluator.evaluate.return_value = evaluation

        request = create_experiment_request()

        sut = EvaluationFlow(flow_evaluator, next_flow)

        actual = sut.evaluate(request, Evaluator.context())

        self.assertEqual(evaluation, actual)
        flow_evaluator.evaluate.assert_called_once()

    def test_of(self):
        fe1 = Mock(spec=FlowEvaluator)
        fe2 = Mock(spec=FlowEvaluator)
        fe3 = Mock(spec=FlowEvaluator)

        flow = EvaluationFlow.of(fe1, fe2, fe3)

        self.assertFalse(flow.is_end)
        self.assertEqual(fe1, flow.flow_evaluator)

        flow = flow.next_flow
        self.assertFalse(flow.is_end)
        self.assertEqual(fe2, flow.flow_evaluator)

        flow = flow.next_flow
        self.assertFalse(flow.is_end)
        self.assertEqual(fe3, flow.flow_evaluator)

        flow = flow.next_flow
        self.assertTrue(flow.is_end)
