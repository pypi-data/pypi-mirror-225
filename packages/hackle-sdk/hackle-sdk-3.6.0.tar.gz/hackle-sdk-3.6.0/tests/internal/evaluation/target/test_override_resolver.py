from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.action.action_resolver import ActionResolver
from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.match.target_matcher import TargetMatcher
from hackle.internal.evaluation.target.override_resolver import OverrideResolver
from hackle.internal.model.entities import Variation, TargetAction, Experiment, TargetRule, Target, TargetCondition, \
    TargetKey, \
    TargetMatch
from hackle.internal.user.internal_hackle_user import InternalHackleUser
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request


class OverrideResolverTest(TestCase):

    def setUp(self):
        self.target_matcher = Mock(spec=TargetMatcher)
        self.action_resolver = Mock(spec=ActionResolver)
        self.sut = OverrideResolver(self.target_matcher, self.action_resolver)

    def test_identnfer_type에_해당하는_식별자가_없으면_segment_override를_평가한다(self):
        # given
        user = InternalHackleUser(identifiers={'$id': 'test'}, properties={})
        experiment = Experiment(
            id=1,
            key=1,
            type='AB_TEST',
            identifier_type='custom_id',
            status='RUNNING',
            version=1,
            execution_version=1,
            variations=[
                Variation(11, 'A', False),
                Variation(22, 'B', False)
            ],
            user_overrides={'test_user_id': 22},
            segment_overrides=[
                TargetRule(
                    Target([TargetCondition(TargetKey('SEGMENT', "SEGMENT"),
                                            TargetMatch('MATCH', 'IN', 'STRING', ["seg_01"]))]),
                    TargetAction('BUCKET', None, 1)
                )
            ],
            target_audiences=[],
            target_rules=[],
            default_rule=TargetAction('BUCKET', bucket_id=1),
            container_id=None,
            winner_variation_id=None
        )

        self.target_matcher.matches.return_value = True
        self.action_resolver.resolve_or_none.return_value = Variation(11, 'A', False)

        request = create_experiment_request(experiment=experiment, user=user)

        # when
        actual = self.sut.resolve_or_none(request, Evaluator.context())

        # then
        self.assertEqual(Variation(11, 'A', False), actual)
        self.target_matcher.matches.assert_called_once()
        self.action_resolver.resolve_or_none.assert_called_once()

    def test_user_override_되어있지않으면_segment_override를_평가한다(self):
        # given
        user = InternalHackleUser(identifiers={'$id': 'test'}, properties={})
        experiment = Experiment(
            id=1,
            key=1,
            type='AB_TEST',
            identifier_type='$id',
            status='RUNNING',
            version=1,
            execution_version=1,
            variations=[
                Variation(11, 'A', False),
                Variation(22, 'B', False)
            ],
            user_overrides={},
            segment_overrides=[
                TargetRule(
                    Target([TargetCondition(TargetKey('SEGMENT', "SEGMENT"),
                                            TargetMatch('MATCH', 'IN', 'STRING', ["seg_01"]))]),
                    TargetAction('BUCKET', None, 1)
                )
            ],
            target_audiences=[],
            target_rules=[],
            default_rule=TargetAction('BUCKET', bucket_id=1),
            container_id=None,
            winner_variation_id=None
        )

        self.target_matcher.matches.return_value = True
        self.action_resolver.resolve_or_none.return_value = Variation(11, 'A', False)

        request = create_experiment_request(experiment=experiment, user=user)

        # when
        actual = self.sut.resolve_or_none(request, Evaluator.context())

        # then
        self.assertEqual(Variation(11, 'A', False), actual)
        self.target_matcher.matches.assert_called_once()
        self.action_resolver.resolve_or_none.assert_called_once()

    def test_user_override되어있는_경우(self):
        # given
        user = InternalHackleUser(identifiers={'$id': 'test'}, properties={})
        experiment = Experiment(
            id=1,
            key=1,
            type='AB_TEST',
            identifier_type='$id',
            status='RUNNING',
            version=1,
            execution_version=1,
            variations=[
                Variation(11, 'A', False),
                Variation(22, 'B', False)
            ],
            user_overrides={'test': 22},
            segment_overrides=[
                TargetRule(
                    Target([TargetCondition(TargetKey('SEGMENT', "SEGMENT"),
                                            TargetMatch('MATCH', 'IN', 'STRING', ["seg_01"]))]),
                    TargetAction('BUCKET', None, 1)
                )
            ],
            target_audiences=[],
            target_rules=[],
            default_rule=TargetAction('BUCKET', bucket_id=1),
            container_id=None,
            winner_variation_id=None
        )

        request = create_experiment_request(experiment=experiment, user=user)

        # when
        actual = self.sut.resolve_or_none(request, Evaluator.context())

        # then
        self.assertEqual(Variation(22, 'B', False), actual)
        self.target_matcher.matches.assert_not_called()
        self.action_resolver.resolve_or_none.assert_not_called()

    def test_직접입력_Segment_둘다_override_되어있지_않으면_None(self):
        # given
        user = InternalHackleUser(identifiers={'$id': 'test'}, properties={})
        experiment = Experiment(
            id=1,
            key=1,
            type='AB_TEST',
            identifier_type='$id',
            status='RUNNING',
            version=1,
            execution_version=1,
            variations=[
                Variation(11, 'A', False),
                Variation(22, 'B', False)
            ],
            user_overrides={},
            segment_overrides=[
                TargetRule(
                    Target([TargetCondition(TargetKey('SEGMENT', "SEGMENT"),
                                            TargetMatch('MATCH', 'IN', 'STRING', ["seg_01"]))]),
                    TargetAction('BUCKET', None, 1)
                )
            ],
            target_audiences=[],
            target_rules=[],
            default_rule=TargetAction('BUCKET', bucket_id=1),
            container_id=None,
            winner_variation_id=None
        )

        self.target_matcher.matches.return_value = False

        request = create_experiment_request(experiment=experiment, user=user)

        # when
        actual = self.sut.resolve_or_none(request, Evaluator.context())

        # then
        self.assertIsNone(actual)
