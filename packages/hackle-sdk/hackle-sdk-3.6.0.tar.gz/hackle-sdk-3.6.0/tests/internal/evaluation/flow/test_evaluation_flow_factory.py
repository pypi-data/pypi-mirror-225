from unittest.mock import Mock

from hackle.internal.evaluation.flow.evaluation_flow_factory import EvaluationFlowFactory
from hackle.internal.evaluation.flow.flow_evaluator import *
from tests import base


class EvaluationFlowFactoryTest(base.BaseTest):

    def setUp(self):
        self.sut = EvaluationFlowFactory(Mock())

    def test_AB_TEST(self):
        flow = self.sut.get_evaluation_flow('AB_TEST')

        flow = self.is_decision_with(flow, OverrideEvaluator)
        flow = self.is_decision_with(flow, IdentifierEvaluator)
        flow = self.is_decision_with(flow, ContainerEvaluator)
        flow = self.is_decision_with(flow, ExperimentTargetEvaluator)
        flow = self.is_decision_with(flow, DraftEvaluator)
        flow = self.is_decision_with(flow, PausedEvaluator)
        flow = self.is_decision_with(flow, CompletedEvaluator)
        flow = self.is_decision_with(flow, TrafficAllocateEvaluator)
        self.assertTrue(flow.is_end)

    def test_FEATURE_FLAG(self):
        flow = self.sut.get_evaluation_flow('FEATURE_FLAG')

        flow = self.is_decision_with(flow, DraftEvaluator)
        flow = self.is_decision_with(flow, PausedEvaluator)
        flow = self.is_decision_with(flow, CompletedEvaluator)
        flow = self.is_decision_with(flow, OverrideEvaluator)
        flow = self.is_decision_with(flow, IdentifierEvaluator)
        flow = self.is_decision_with(flow, TargetRuleEvaluator)
        flow = self.is_decision_with(flow, DefaultRuleEvaluator)
        self.assertTrue(flow.is_end)

    def is_decision_with(self, evaluation_flow, cls):
        self.assertFalse(evaluation_flow.is_end)
        self.assertIsInstance(evaluation_flow.flow_evaluator, cls)
        return evaluation_flow.next_flow
