from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.match.target_matcher import TargetMatcher
from hackle.internal.evaluation.target.experiment_target_determiner import ExperimentTargetDeterminer
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request
from tests.internal.model.test_entities import create_experiment


class ExperimentTargetDeterminerTest(TestCase):
    def setUp(self):
        self.target_matches = []
        self.target_matcher = Mock(spec=TargetMatcher)
        self.target_matcher.matches = Mock(side_effect=self.target_matches)
        self.sut = ExperimentTargetDeterminer(self.target_matcher)

    def test_audiences가_비어있으면_true(self):
        # given
        request = create_experiment_request()

        # when
        actual = self.sut.is_user_in_experiment_target(request, Evaluator.context())

        # then
        self.assertTrue(actual)

    def test_하나라도_일치하는_audience가_있는경우_true(self):
        # given
        experiment = create_experiment(target_audiences=[
            self._audience_target(False),
            self._audience_target(False),
            self._audience_target(False),
            self._audience_target(True),
            self._audience_target(False),
        ])
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.is_user_in_experiment_target(request, Evaluator.context())

        # then
        self.assertTrue(actual)
        self.assertEqual(4, self.target_matcher.matches.call_count)

    def test_일치하는_audience가_하나도_없는경우_false(self):
        # given
        experiment = create_experiment(target_audiences=[
            self._audience_target(False),
            self._audience_target(False),
            self._audience_target(False),
            self._audience_target(False),
            self._audience_target(False),
        ])
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.is_user_in_experiment_target(request, Evaluator.context())

        # then
        self.assertFalse(actual)
        self.assertEqual(5, self.target_matcher.matches.call_count)

    def _audience_target(self, is_match):
        self.target_matches.append(is_match)
        return Mock()
