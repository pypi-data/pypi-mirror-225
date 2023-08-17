from unittest import TestCase
from unittest.mock import Mock

from hackle.decision import DecisionReason
from hackle.internal.evaluation.action.action_resolver import ActionResolver
from hackle.internal.evaluation.container.container_resolver import ContainerResolver
from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluation import ExperimentEvaluation
from hackle.internal.evaluation.flow.evaluation_flow import EvaluationFlow
from hackle.internal.evaluation.flow.flow_evaluator import OverrideEvaluator, DraftEvaluator, PausedEvaluator, \
    CompletedEvaluator, ExperimentTargetEvaluator, TrafficAllocateEvaluator, TargetRuleEvaluator, DefaultRuleEvaluator, \
    ContainerEvaluator, IdentifierEvaluator
from hackle.internal.evaluation.target.experiment_target_determiner import ExperimentTargetDeterminer
from hackle.internal.evaluation.target.experiment_target_rule_determiner import ExperimentTargetRuleDeterminer
from hackle.internal.evaluation.target.override_resolver import OverrideResolver
from hackle.internal.model.entities import TargetRule
from hackle.internal.workspace.workspace import Workspace
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request
from tests.internal.model.test_entities import create_experiment, create_variation


class FlowEvaluatorTest(TestCase):

    def setUp(self):
        self.evaluation = Mock(spec=ExperimentEvaluation)
        self.next_flow = Mock(spec=EvaluationFlow)
        self.next_flow.evaluate.return_value = self.evaluation
        self.context = Evaluator.context()


class OverrideEvaluatorTest(FlowEvaluatorTest):

    def setUp(self):
        super().setUp()
        self.override_resolver = Mock(spec=OverrideResolver)
        self.sut = OverrideEvaluator(self.override_resolver)

    def test_unsupported_type(self):
        experiment = create_experiment(type='INVALID')
        request = create_experiment_request(experiment=experiment)

        with self.assertRaises(Exception):
            self.sut.evaluate(request, self.context, self.next_flow)

    def test_AB_TEST에_수동할당된_사용자인_경우_수동할당된_그룹으로_평가한다(self):
        # given
        experiment = create_experiment(type='AB_TEST')
        variation = experiment.variations[0]
        self.override_resolver.resolve_or_none.return_value = variation

        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.OVERRIDDEN, actual.reason)
        self.assertEqual(variation.id, actual.variation_id)

    def test_FEATURE_FLAG에_개별타겟된_사용자는_개별타겟된_그룹으로_평가한다(self):
        # given
        experiment = create_experiment(type='FEATURE_FLAG')
        variation = experiment.variations[0]
        self.override_resolver.resolve_or_none.return_value = variation

        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.INDIVIDUAL_TARGET_MATCH, actual.reason)
        self.assertEqual(variation.id, actual.variation_id)

    def test_수동할당된_사용자가_아닌경우_다음_flow로_평가한다(self):
        # given
        self.override_resolver.resolve_or_none.return_value = None

        # when
        actual = self.sut.evaluate(create_experiment_request(), self.context, self.next_flow)

        # then
        self.assertEqual(self.evaluation, actual)
        self.next_flow.evaluate.assert_called_once()


class DraftEvaluatorTest(FlowEvaluatorTest):

    def setUp(self):
        super().setUp()
        self.sut = DraftEvaluator()

    def test_DRAFT_상태면_기본그룹으로_평가한다(self):
        # given
        experiment = create_experiment(
            type='AB_TEST',
            status='DRAFT',
            variations=[
                create_variation(id=42, key='A'),
                create_variation(id=43, key='B')
            ]
        )
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.EXPERIMENT_DRAFT, actual.reason)
        self.assertEqual(42, actual.variation_id)

    def test_DRAFT_상태가_아니면_다름_플로우로_평가한다(self):
        # given
        experiment = create_experiment(type='AB_TEST', status='RUNNING')
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(self.evaluation, actual)
        self.next_flow.evaluate.assert_called_once()


class PausedEvaluatorTest(FlowEvaluatorTest):

    def setUp(self):
        super().setUp()
        self.sut = PausedEvaluator()

    def test_unsupported_type(self):
        experiment = create_experiment(type='INVALID', status='PAUSED')
        request = create_experiment_request(experiment=experiment)

        with self.assertRaises(Exception):
            self.sut.evaluate(request, self.context, self.next_flow)

    def test_AB_TEST의_상태가_PAUSED면_기본그룹으로_평가한다(self):
        # given
        experiment = create_experiment(
            type='AB_TEST',
            status='PAUSED',
            variations=[
                create_variation(id=42, key='A'),
                create_variation(id=43, key='B')
            ]
        )
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.EXPERIMENT_PAUSED, actual.reason)
        self.assertEqual(42, actual.variation_id)

    def test_FEATURE_FLAG의_상태가_PAUSED면_기본그룹으로_평가한다(self):
        # given
        experiment = create_experiment(
            type='FEATURE_FLAG',
            status='PAUSED',
            variations=[
                create_variation(id=42, key='A'),
                create_variation(id=43, key='B')
            ]
        )
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.FEATURE_FLAG_INACTIVE, actual.reason)
        self.assertEqual(42, actual.variation_id)

    def test_PAUSED_상태가_아니면_다름_플로우로_평가한다(self):
        # given
        experiment = create_experiment(type='AB_TEST', status='RUNNING')
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(self.evaluation, actual)
        self.next_flow.evaluate.assert_called_once()


class CompletedEvaluatorTest(FlowEvaluatorTest):

    def setUp(self):
        super().setUp()
        self.sut = CompletedEvaluator()

    def test_COMPLETED_상태면_기본그룹으로_평가한다(self):
        # given
        experiment = create_experiment(
            type='AB_TEST',
            status='COMPLETED',
            variations=[
                create_variation(id=42, key='A'),
                create_variation(id=43, key='B')
            ],
            winner_variation_id=43
        )
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.EXPERIMENT_COMPLETED, actual.reason)
        self.assertEqual(43, actual.variation_id)

    def test_COMPLETED_상태지만_winner가_없으면_예외(self):
        # given
        experiment = create_experiment(
            id=320,
            type='AB_TEST',
            status='COMPLETED',
            variations=[
                create_variation(id=42, key='A'),
                create_variation(id=43, key='B')
            ]
        )
        request = create_experiment_request(experiment=experiment)

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual('Winner variation[320]', str(actual.exception))

    def test_COMPLETED_상태가_아니면_다름_플로우로_평가한다(self):
        # given
        experiment = create_experiment(type='AB_TEST', status='RUNNING')
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(self.evaluation, actual)
        self.next_flow.evaluate.assert_called_once()


class ExperimentTargetEvaluatorTest(FlowEvaluatorTest):

    def setUp(self):
        super().setUp()
        self.experiment_target_determiner = Mock(spec=ExperimentTargetDeterminer)
        self.sut = ExperimentTargetEvaluator(self.experiment_target_determiner)

    def test_AB_TEST_타입이_아니면_예외_발생(self):
        # given
        experiment = create_experiment(id=42, type='FEATURE_FLAG')
        request = create_experiment_request(experiment=experiment)

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual('experiment type must be AB_TEST [42]', str(actual.exception))

    def test_사용자가_실험_참여_대상이면_다음_플로우로_평가한다(self):
        # given
        experiment = create_experiment(type='AB_TEST')
        request = create_experiment_request(experiment=experiment)

        self.experiment_target_determiner.is_user_in_experiment_target.return_value = True

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(self.evaluation, actual)
        self.next_flow.evaluate.assert_called_once()

    def test_사용자가_실험_참여_대상이_아니면_기본그룹으로_평가한다(self):
        # given
        experiment = create_experiment(type='AB_TEST')
        request = create_experiment_request(experiment=experiment)

        self.experiment_target_determiner.is_user_in_experiment_target.return_value = False

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.NOT_IN_EXPERIMENT_TARGET, actual.reason)
        self.assertEqual('A', actual.variation_key)


class TrafficAllocateEvaluatorTest(FlowEvaluatorTest):

    def setUp(self):
        super().setUp()
        self.action_resolver = Mock(spec=ActionResolver)
        self.sut = TrafficAllocateEvaluator(self.action_resolver)

    def test_실행중이_아니면_예외_발생(self):
        # given
        experiment = create_experiment(id=42, type='AB_TEST', status='DRAFT')
        request = create_experiment_request(experiment=experiment)

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual('experiment status must be RUNNING [42]', str(actual.exception))

    def test_AB_TEST_타입이_아니면_예외_발생(self):
        # given
        experiment = create_experiment(id=42, type='FEATURE_FLAG', status='RUNNING')
        request = create_experiment_request(experiment=experiment)

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual('experiment type must be AB_TEST [42]', str(actual.exception))

    def test_기본룰에_해당하는_Variation이_없으면_기본그룹으로_평가한다(self):
        # given
        experiment = create_experiment(id=42, type='AB_TEST', status='RUNNING')
        request = create_experiment_request(experiment=experiment)

        self.action_resolver.resolve_or_none.return_value = None

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.TRAFFIC_NOT_ALLOCATED, actual.reason)
        self.assertEqual('A', actual.variation_key)

    def test_할당된_그룹이_드랍되었으면_그본그룹으로_평가한다(self):
        # given
        experiment = create_experiment(
            id=42, type='AB_TEST', status='RUNNING',
            variations=[
                create_variation(id=41, key='A'),
                create_variation(id=42, key='B'),
                create_variation(id=43, key='C', is_dropped=True),
            ]
        )
        request = create_experiment_request(experiment=experiment)

        self.action_resolver.resolve_or_none.return_value = experiment.get_variation_by_key_or_none('C')

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.VARIATION_DROPPED, actual.reason)
        self.assertEqual('A', actual.variation_key)

    def test_할당된_그룹으로_평가한다(self):
        # given
        experiment = create_experiment(
            id=42, type='AB_TEST', status='RUNNING',
            variations=[
                create_variation(id=41, key='A'),
                create_variation(id=42, key='B'),
            ]
        )
        request = create_experiment_request(experiment=experiment)

        self.action_resolver.resolve_or_none.return_value = experiment.get_variation_by_key_or_none('B')

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.TRAFFIC_ALLOCATED, actual.reason)
        self.assertEqual(42, actual.variation_id)


class TargetRuleEvaluatorTest(FlowEvaluatorTest):

    def setUp(self):
        super().setUp()
        self.target_rule_determiner = Mock(spec=ExperimentTargetRuleDeterminer)
        self.action_resolver = Mock(spec=ActionResolver)
        self.sut = TargetRuleEvaluator(self.target_rule_determiner, self.action_resolver)

    def test_실행중이_아니면_예외_발생(self):
        # given
        experiment = create_experiment(id=42, type='FEATURE_FLAG', status='DRAFT')
        request = create_experiment_request(experiment=experiment)

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual('experiment status must be RUNNING [42]', str(actual.exception))

    def test_FEATURE_FLAG_타입이_아니면_예외_발생(self):
        # given
        experiment = create_experiment(id=42, type='AB_TEST', status='RUNNING')
        request = create_experiment_request(experiment=experiment)

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual('experiment type must be FEATURE_FLAG [42]', str(actual.exception))

    def test_identifier_type에_해당하는_식별자가_없으면_다음_플로우를_실행한다(self):
        # given
        experiment = create_experiment(id=42, type='FEATURE_FLAG', status='RUNNING', identifier_type='custom_id')
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(self.evaluation, actual)
        self.next_flow.evaluate.assert_called_once()

    def test_타겟룰에_해당하지_않으면_다음_플로우로_평가한다(self):
        # given
        experiment = create_experiment(id=42, type='FEATURE_FLAG', status='RUNNING')
        request = create_experiment_request(experiment=experiment)

        self.target_rule_determiner.determine_target_rule_or_none.return_value = None

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(self.evaluation, actual)
        self.next_flow.evaluate.assert_called_once()

    def test_타겟룰에_해당하지만_Action에_해당하는_Variation이_결정되지_않으면_예외발생(self):
        # given
        experiment = create_experiment(id=42, type='FEATURE_FLAG', status='RUNNING')
        request = create_experiment_request(experiment=experiment)
        target_rule = TargetRule(Mock(), Mock())

        self.target_rule_determiner.determine_target_rule_or_none.return_value = target_rule
        self.action_resolver.resolve_or_none.return_value = None

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual('FeatureFlag must decide the variation [42]', str(actual.exception))
        self.target_rule_determiner.determine_target_rule_or_none.assert_called_once()
        self.action_resolver.resolve_or_none.assert_called_once()

    def test_타겟룰에_해당하면_해당룰로_결정된_Variation으로_평가한다(self):
        # given
        experiment = create_experiment(id=42, type='FEATURE_FLAG', status='RUNNING')
        request = create_experiment_request(experiment=experiment)
        target_rule = TargetRule(Mock(), Mock())

        self.target_rule_determiner.determine_target_rule_or_none.return_value = target_rule
        self.action_resolver.resolve_or_none.return_value = experiment.variations[0]

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.TARGET_RULE_MATCH, actual.reason)
        self.assertEqual(experiment.variations[0].id, actual.variation_id)


class DefaultRuleEvaluatorTest(FlowEvaluatorTest):
    def setUp(self):
        super().setUp()
        self.action_resolver = Mock(spec=ActionResolver)
        self.sut = DefaultRuleEvaluator(self.action_resolver)

    def test_실행중이_아니면_예외_발생(self):
        # given
        experiment = create_experiment(id=42, type='FEATURE_FLAG', status='DRAFT')
        request = create_experiment_request(experiment=experiment)

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual('experiment status must be RUNNING [42]', str(actual.exception))

    def test_FEATURE_FLAG_타입이_아니면_예외_발생(self):
        # given
        experiment = create_experiment(id=42, type='AB_TEST', status='RUNNING')
        request = create_experiment_request(experiment=experiment)

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual('experiment type must be FEATURE_FLAG [42]', str(actual.exception))

    def test_identifier_type에_해당하는_식별자가_없으면_default_variation을_리턴한다(self):
        # given
        experiment = create_experiment(id=42, type='FEATURE_FLAG', status='RUNNING', identifier_type='custom_id')
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.DEFAULT_RULE, actual.reason)
        self.assertEqual('A', actual.variation_key)

    def test_기본룰에_해당하는_Variation을_결정하지_못하면_예외_발생(self):
        # given
        experiment = create_experiment(id=42, type='FEATURE_FLAG', status='RUNNING')
        request = create_experiment_request(experiment=experiment)
        self.action_resolver.resolve_or_none.return_value = None

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual('FeatureFlag must decide the variation [42]', str(actual.exception))

    def test_기본룰에_해당하는_Variation으로_평가한다(self):
        # given
        experiment = create_experiment(id=42, type='FEATURE_FLAG', status='RUNNING')
        request = create_experiment_request(experiment=experiment)
        self.action_resolver.resolve_or_none.return_value = experiment.variations[0]

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.DEFAULT_RULE, actual.reason)
        self.assertEqual(experiment.variations[0].id, actual.variation_id)


class ContainerEvaluatorTest(FlowEvaluatorTest):

    def setUp(self):
        super().setUp()
        self.container_resolver = Mock(spec=ContainerResolver)
        self.sut = ContainerEvaluator(self.container_resolver)

    def test_상호배타적실험이_아니면_다음_플로우_실행(self):
        # given
        workspace = Mock(spec=Workspace)
        experiment = create_experiment()
        request = create_experiment_request(workspace=workspace, experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(self.evaluation, actual)
        self.next_flow.evaluate.assert_called_once()

    def test_container_id로_Container를_찾을수_없으면_예외발생(self):
        # given
        workspace = Mock(spec=Workspace)
        experiment = create_experiment(id=42, container_id=320)
        request = create_experiment_request(workspace=workspace, experiment=experiment)

        workspace.get_container_or_none.return_value = None

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual('Container[320]', str(actual.exception))

    def test_상호배타그룹이면_다음플로우(self):
        # given
        workspace = Mock(spec=Workspace)
        experiment = create_experiment(id=42, container_id=320)
        request = create_experiment_request(workspace=workspace, experiment=experiment)

        workspace.get_container_or_none.return_value = Mock()
        self.container_resolver.is_user_in_container_group.return_value = True

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(self.evaluation, actual)
        self.next_flow.evaluate.assert_called_once()

    def test_상호배타에_속해있지만_상호배타그룹에_포함하지_않으면_기본그룹(self):
        # given
        workspace = Mock(spec=Workspace)
        experiment = create_experiment(id=42, container_id=320)
        request = create_experiment_request(workspace=workspace, experiment=experiment)

        workspace.get_container_or_none.return_value = Mock()
        self.container_resolver.is_user_in_container_group.return_value = False

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.NOT_IN_MUTUAL_EXCLUSION_EXPERIMENT, actual.reason)
        self.assertEqual('A', actual.variation_key)


class IdentifierEvaluatorTest(FlowEvaluatorTest):
    def setUp(self):
        super().setUp()
        self.sut = IdentifierEvaluator()

    def test_식별자가_있으면_다음플로우_실행(self):
        # given
        experiment = create_experiment()
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(self.evaluation, actual)
        self.next_flow.evaluate.assert_called_once()

    def test_식별자가_없으면_IDENTIFIER_NOT_FOUND(self):
        experiment = create_experiment(identifier_type='custom_id')
        request = create_experiment_request(experiment=experiment)

        # when
        actual = self.sut.evaluate(request, self.context, self.next_flow)

        # then
        self.assertEqual(DecisionReason.IDENTIFIER_NOT_FOUND, actual.reason)
        self.assertEqual('A', actual.variation_key)
