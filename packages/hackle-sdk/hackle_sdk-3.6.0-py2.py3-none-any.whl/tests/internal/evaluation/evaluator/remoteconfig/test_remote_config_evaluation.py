from unittest import TestCase
from unittest.mock import Mock

from hackle.decision import DecisionReason
from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.evaluator.remoteconfig.remote_config_evaluation import RemoteConfigEvaluation
from hackle.internal.model.entities import RemoteConfigParameter
from hackle.internal.model.properties_builder import PropertiesBuilder
from tests.internal.evaluation.evaluator.remoteconfig.test_remote_config_request import create_remote_config_request


class RemoteConfigEvaluationTest(TestCase):

    def test_create(self):
        parameter = Mock(spec=RemoteConfigParameter)
        parameter.id = 1

        request = create_remote_config_request(parameter=parameter)
        context = Evaluator.context()
        context.add_evaluation(Mock(spec=Evaluator.Evaluation))

        evaluation = RemoteConfigEvaluation.of(request, context, 42, "go", DecisionReason.DEFAULT_RULE,
                                               PropertiesBuilder())

        self.assertEqual(DecisionReason.DEFAULT_RULE, evaluation.reason)
        self.assertEqual(1, len(evaluation.target_evaluations))
        self.assertEqual(parameter, evaluation.parameter)
        self.assertEqual("go", evaluation.properties.get("returnValue"))

    def test_create_by_default(self):
        parameter = Mock(spec=RemoteConfigParameter)
        parameter.id = 1

        request = create_remote_config_request(parameter=parameter, default_value="42")
        context = Evaluator.context()
        context.add_evaluation(Mock(spec=Evaluator.Evaluation))

        evaluation = RemoteConfigEvaluation.of_default(request, context, DecisionReason.DEFAULT_RULE,
                                                       PropertiesBuilder())

        self.assertEqual(DecisionReason.DEFAULT_RULE, evaluation.reason)
        self.assertEqual(1, len(evaluation.target_evaluations))
        self.assertEqual(parameter, evaluation.parameter)
        self.assertEqual("42", evaluation.properties.get("returnValue"))
