from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.evaluator.delegating_evaluator import DelegatingEvaluator
from hackle.internal.evaluation.evaluator.evaluator import Evaluator, ContextualEvaluator


class DelegatingEvaluatorTest(TestCase):

    def test_evaluate(self):
        sut = DelegatingEvaluator()

        r1 = Mock(spec=Evaluator.Request)
        e1 = Mock(spec=Evaluator.Evaluation)
        evaluator1 = MockEvaluator(r1, e1)

        sut.add(evaluator1)
        with self.assertRaises(Exception):
            sut.evaluate(Mock(), Mock())
        self.assertEqual(e1, sut.evaluate(r1, Evaluator.context()))

        r2 = Mock(spec=Evaluator.Request)
        e2 = Mock(spec=Evaluator.Evaluation)
        evaluator2 = MockEvaluator(r2, e2)

        sut.add(evaluator2)
        self.assertEqual(e2, sut.evaluate(r2, Evaluator.context()))


class MockEvaluator(ContextualEvaluator):

    def __init__(self, request, evaluation):
        super(MockEvaluator, self).__init__()
        self.__request = request
        self.__evaluation = evaluation

    def supports(self, request):
        return request == self.__request

    def evaluate_internal(self, request, context):
        return self.__evaluation
