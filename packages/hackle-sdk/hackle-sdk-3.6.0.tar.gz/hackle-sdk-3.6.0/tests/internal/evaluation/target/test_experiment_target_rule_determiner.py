from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.match.target_matcher import TargetMatcher
from hackle.internal.evaluation.target.experiment_target_rule_determiner import ExperimentTargetRuleDeterminer
from hackle.internal.model.entities import *
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request
from tests.internal.model.test_entities import create_experiment


class ExperimentTargetRuleDeterminerTest(TestCase):

    def setUp(self):
        self.target_matches = []
        self.target_matcher = Mock(spec=TargetMatcher)
        self.target_matcher.matches = Mock(side_effect=self.target_matches)
        self.sut = ExperimentTargetRuleDeterminer(self.target_matcher)

    def test_등록된_rule이_없는경우_None리턴(self):
        # given
        experiment = create_experiment(target_rules=[])
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.determine_target_rule_or_none(request, Evaluator.context())

        # then
        self.assertIsNone(actual)

    def test_등록된_규칙중_일치하는_첫번쨰_규칙을_리턴한다(self):
        # given
        experiment = create_experiment(target_rules=[
            self._rule(False),
            self._rule(False),
            self._rule(False),
            self._rule(False),
            self._rule(True),
            self._rule(False),
        ])
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.determine_target_rule_or_none(request, Evaluator.context())

        # then
        self.assertEqual(experiment.target_rules[4], actual)
        self.assertEqual(5, self.target_matcher.matches.call_count)

    def test_등록된_규칙중_일치하는_규칙이_하나도_없는경우_None리턴(self):
        # given

        experiment = create_experiment(target_rules=[
            self._rule(False),
            self._rule(False),
            self._rule(False),
            self._rule(False),
            self._rule(False),
            self._rule(False),
        ])
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.determine_target_rule_or_none(request, Evaluator.context())

        # then
        self.assertIsNone(actual)
        self.assertEqual(6, self.target_matcher.matches.call_count)

    def _rule(self, is_match):
        self.target_matches.append(is_match)
        target_rule = Mock(spec=TargetRule)
        target_rule.target = Mock()
        return target_rule
