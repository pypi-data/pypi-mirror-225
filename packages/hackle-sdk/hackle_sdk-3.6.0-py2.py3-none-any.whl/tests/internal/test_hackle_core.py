from unittest import TestCase
from unittest.mock import Mock

from hackle.decision import ExperimentDecision, FeatureFlagDecision, DecisionReason
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluation import ExperimentEvaluation
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluator import ExperimentEvaluator
from hackle.internal.evaluation.evaluator.remoteconfig.remote_config_evaluation import RemoteConfigEvaluation
from hackle.internal.evaluation.evaluator.remoteconfig.remote_config_evaluator import RemoteConfigEvaluator
from hackle.internal.event.event_processor import EventProcessor
from hackle.internal.event.user_event_factory import UserEventFactory
from hackle.internal.hackle_core import HackleCore
from hackle.internal.model.entities import EventType, ParameterConfiguration
from hackle.internal.time.clock import SYSTEM_CLOCK
from hackle.internal.user.identifier_type import IdentifierType
from hackle.internal.user.internal_hackle_user import InternalHackleUser
from hackle.internal.workspace.workspace import Workspace
from hackle.internal.workspace.workspace_fetcher import WorkspaceFetcher
from hackle.model import HackleEvent
from tests.internal.model.test_entities import create_experiment, create_parameter


class HackleCoreTest(TestCase):

    def setUp(self):
        self.experiment_evaluator = Mock(spec=ExperimentEvaluator)
        self.remote_config_evaluator = Mock(spec=RemoteConfigEvaluator)
        self.workspace_fetcher = Mock(spec=WorkspaceFetcher)
        self.event_factory = Mock(spec=UserEventFactory)
        self.event_processor = Mock(spec=EventProcessor)
        self.clock = SYSTEM_CLOCK
        self.sut = HackleCore(
            self.experiment_evaluator,
            self.remote_config_evaluator,
            self.workspace_fetcher,
            self.event_factory,
            self.event_processor
        )

        self.user = InternalHackleUser.builder().identifier(IdentifierType.ID, "user").build()

    def test_close(self):
        self.sut.close()
        self.workspace_fetcher.stop.assert_called_once()
        self.event_processor.stop.assert_called_once()

    def test__experiment__설정정보를_가져오지_못한_경우_기본그룹으로_결정하고_노출이벤트는_전송하지_않는다(self):
        # given
        self.workspace_fetcher.fetch.return_value = None

        # when
        actual = self.sut.experiment(42, self.user, 'D')

        # then
        self.assertEqual(ExperimentDecision('D', DecisionReason.SDK_NOK_READY), actual)
        self.event_processor.process.assert_not_called()

    def test__experiment__실험키에_해당하는_실험이_없는경우_기본그룹으로_결정하고_노출이벤트는_전송하지_않는다(self):
        # given
        workspace = Workspace('{}')
        self.workspace_fetcher.fetch.return_value = workspace

        # when
        actual = self.sut.experiment(42, self.user, 'G')

        # then
        self.assertEqual(ExperimentDecision('G', DecisionReason.EXPERIMENT_NOT_FOUND), actual)
        self.event_processor.process.assert_not_called()

    def test__experiment__평가결과로_노출이벤트를_전송하고_평가된_그룹으로_결정한다(self):
        # given
        experiment = create_experiment()

        workspace = Mock(spec=Workspace)
        workspace.get_experiment_or_none.return_value = experiment
        self.workspace_fetcher.fetch.return_value = workspace

        config = Mock(spec=ParameterConfiguration)
        config.id = 420

        evaluation = ExperimentEvaluation(
            DecisionReason.TRAFFIC_ALLOCATED,
            [],
            experiment,
            320,
            'B',
            config
        )

        self.experiment_evaluator.evaluate.return_value = evaluation
        self.event_factory.create.return_value = [Mock(), Mock()]

        # when
        actual = self.sut.experiment(42, self.user, 'J')

        # then
        self.assertEqual('B', actual.variation)
        self.assertEqual(DecisionReason.TRAFFIC_ALLOCATED, actual.reason)
        self.assertEqual(config, actual.config)
        self.assertEqual(2, self.event_processor.process.call_count)

    def test__experiment__평가결과로_Config_가_없으면_Empty_config(self):
        # given
        experiment = create_experiment()

        workspace = Mock(spec=Workspace)
        workspace.get_experiment_or_none.return_value = experiment
        self.workspace_fetcher.fetch.return_value = workspace

        evaluation = ExperimentEvaluation(
            DecisionReason.TRAFFIC_ALLOCATED,
            [],
            experiment,
            320,
            'B',
            None
        )

        self.experiment_evaluator.evaluate.return_value = evaluation
        self.event_factory.create.return_value = [Mock(), Mock()]

        # when
        actual = self.sut.experiment(42, self.user, 'J')

        # then
        self.assertEqual('B', actual.variation)
        self.assertEqual(DecisionReason.TRAFFIC_ALLOCATED, actual.reason)
        self.assertEqual({}, actual.config)

    def test__feature_flag__설정정보를_가져오지_못하면_OFF로_결정하고_노출이벤트는_전송하지_않는다(self):
        # given
        self.workspace_fetcher.fetch.return_value = None

        # when
        actual = self.sut.feature_flag(42, self.user)

        # then
        self.assertEqual(FeatureFlagDecision(False, DecisionReason.SDK_NOK_READY), actual)
        self.event_processor.process.assert_not_called()

    def test__feature_flag__기능키에_해당하는_기능플래그가_없는경우_OFF로_결정하고_노출이벤트는_전송하지_않는다(self):
        # given
        workspace = Mock(spec=Workspace)
        workspace.get_feature_flag_or_none.return_value = None

        self.workspace_fetcher.fetch.return_value = workspace

        # when
        actual = self.sut.feature_flag(42, self.user)

        # then
        self.assertEqual(FeatureFlagDecision(False, DecisionReason.FEATURE_FLAG_NOT_FOUND), actual)
        self.event_processor.process.assert_not_called()

    def test__feature_flag__평가결과로_노출이벤트를_전송한다(self):
        # given
        feature_flag = create_experiment(type='FEATURE_FLAG')

        workspace = Mock(spec=Workspace)
        workspace.get_feature_flag_or_none.return_value = feature_flag
        self.workspace_fetcher.fetch.return_value = workspace

        config = Mock(spec=ParameterConfiguration)
        config.id = 420

        evaluation = ExperimentEvaluation(
            DecisionReason.TRAFFIC_ALLOCATED,
            [],
            feature_flag,
            320,
            'A',
            config
        )

        self.experiment_evaluator.evaluate.return_value = evaluation
        self.event_factory.create.return_value = [Mock(), Mock()]

        # when
        self.sut.feature_flag(42, self.user)

        # then
        self.assertEqual(2, self.event_processor.process.call_count)

    def test__feature_flag__그룹_A로_평가되면_OFF로_결정한다(self):
        # given
        feature_flag = create_experiment(type='FEATURE_FLAG')

        workspace = Mock(spec=Workspace)
        workspace.get_feature_flag_or_none.return_value = feature_flag
        self.workspace_fetcher.fetch.return_value = workspace

        evaluation = ExperimentEvaluation(
            DecisionReason.DEFAULT_RULE,
            [],
            feature_flag,
            320,
            'A',
            None
        )

        self.experiment_evaluator.evaluate.return_value = evaluation
        self.event_factory.create.return_value = [Mock(), Mock()]

        # when
        actual = self.sut.feature_flag(42, self.user)

        # then
        self.assertEqual(False, actual.is_on)
        self.assertEqual(DecisionReason.DEFAULT_RULE, actual.reason)

    def test__feature_flag__그룹_A로_평가되지_않으면_ON으로_결정한다(self):
        # given
        feature_flag = create_experiment(type='FEATURE_FLAG')

        workspace = Mock(spec=Workspace)
        workspace.get_feature_flag_or_none.return_value = feature_flag
        self.workspace_fetcher.fetch.return_value = workspace

        evaluation = ExperimentEvaluation(
            DecisionReason.TARGET_RULE_MATCH,
            [],
            feature_flag,
            320,
            'B',
            None
        )

        self.experiment_evaluator.evaluate.return_value = evaluation
        self.event_factory.create.return_value = [Mock(), Mock()]

        # when
        actual = self.sut.feature_flag(42, self.user)

        # then
        self.assertEqual(True, actual.is_on)
        self.assertEqual(DecisionReason.TARGET_RULE_MATCH, actual.reason)

    def test__feature_flag__Config(self):
        # given
        feature_flag = create_experiment(type='FEATURE_FLAG')

        workspace = Mock(spec=Workspace)
        workspace.get_feature_flag_or_none.return_value = feature_flag
        self.workspace_fetcher.fetch.return_value = workspace

        config = Mock(spec=ParameterConfiguration)
        config.id = 420

        evaluation = ExperimentEvaluation(
            DecisionReason.TRAFFIC_ALLOCATED,
            [],
            feature_flag,
            320,
            'A',
            config
        )
        self.experiment_evaluator.evaluate.return_value = evaluation
        self.event_factory.create.return_value = [Mock(), Mock()]

        # when
        actual = self.sut.feature_flag(42, self.user)

        # then
        self.assertEqual(config, actual.config)

    def test__feature_flag__Config_None(self):
        # given
        feature_flag = create_experiment(type='FEATURE_FLAG')

        workspace = Mock(spec=Workspace)
        workspace.get_feature_flag_or_none.return_value = feature_flag
        self.workspace_fetcher.fetch.return_value = workspace

        evaluation = ExperimentEvaluation(
            DecisionReason.TRAFFIC_ALLOCATED,
            [],
            feature_flag,
            320,
            'A',
            None
        )
        self.experiment_evaluator.evaluate.return_value = evaluation
        self.event_factory.create.return_value = [Mock(), Mock()]

        # when
        actual = self.sut.feature_flag(42, self.user)

        # then
        self.assertEqual({}, actual.config)

    def test__track__event_Workspace를_가져오지_못하면_Undefined_이벤트를_전송한다(self):
        # given
        event = HackleEvent.builder('event_key').build()
        user = InternalHackleUser(identifiers={'$id': 'user_id'}, properties={})

        self.workspace_fetcher.fetch.return_value = None

        # when
        self.sut.track(event, user)

        # then
        self.event_processor.process.assert_called_once()

        track_event = self.event_processor.process.call_args[0][0]
        self.assertEqual(0, track_event.event_type.id)
        self.assertEqual('event_key', track_event.event_type.key)

    def test__track__event_eventKey에_대한_eventType을_찾지_못하면_Undeified_이벤트를_전송한다(self):
        # given
        event = HackleEvent.builder('event_key').build()
        user = InternalHackleUser(identifiers={'$id': 'user_id'}, properties={})

        workspace = Mock(spec=Workspace)
        workspace.get_event_type_or_none.return_value = None
        self.workspace_fetcher.fetch.return_value = workspace

        # when
        self.sut.track(event, user)

        # then
        self.event_processor.process.assert_called_once()

        track_event = self.event_processor.process.call_args[0][0]
        self.assertEqual(0, track_event.event_type.id)
        self.assertEqual('event_key', track_event.event_type.key)

    def test_track_event_설정정보에서_입력받은_이벤트키에_해당하는_이벤트타입정보로_이벤트를_전송한다(self):
        # given
        event = HackleEvent.builder('event_key').build()
        user = InternalHackleUser(identifiers={'$id': 'user_id'}, properties={})

        workspace = Mock(spec=Workspace)
        event_type = EventType(320, 'event_key')
        workspace.get_event_type_or_none.return_value = event_type
        self.workspace_fetcher.fetch.return_value = workspace

        # when
        self.sut.track(event, user)

        # then
        self.event_processor.process.assert_called_once()

        track_event = self.event_processor.process.call_args[0][0]
        self.assertEqual(320, track_event.event_type.id)
        self.assertEqual('event_key', track_event.event_type.key)

    def test_remote_config_설정정보를_가져오지_못하면_SDK_NOT_READY_사유와_default_value를_반환한다(self):
        # given
        user = InternalHackleUser(identifiers={'$id': 'user_id'}, properties={})
        self.workspace_fetcher.fetch.return_value = None

        # when
        decision = self.sut.remote_config('test_key', user, 'STRING', 'default')

        # then
        self.assertEqual(decision.reason, DecisionReason.SDK_NOK_READY)
        self.assertEqual(decision.value, 'default')

    def test_remote_config_parameter를_가져오지_못하면_REMOTE_CONFIG_PARAMETER_NOT_FOUND_사유와_default_value를_반환한다(self):
        # given
        user = InternalHackleUser(identifiers={'$id': 'user_id'}, properties={})
        workspace = Mock(spec=Workspace)
        self.workspace_fetcher.fetch.return_value = workspace
        workspace.get_remote_config_parameter_or_none.return_value = None

        # when
        decision = self.sut.remote_config('test_key', user, 'STRING', 'default')

        # then
        self.assertEqual(decision.reason, DecisionReason.REMOTE_CONFIG_PARAMETER_NOT_FOUND)
        self.assertEqual(decision.value, 'default')

    def test_remote_config_parameter를_정상적으로_가져오는_경우_해당_파라미터의_value_와_reason을_반환함(self):
        # given
        parameter = create_parameter()

        workspace = Mock(spec=Workspace)
        self.workspace_fetcher.fetch.return_value = workspace
        workspace.get_remote_config_parameter_or_none.return_value = parameter

        evaluation = RemoteConfigEvaluation(
            DecisionReason.DEFAULT_RULE,
            [],
            parameter,
            42,
            "vvv",
            {}
        )

        self.remote_config_evaluator.evaluate.return_value = evaluation
        self.event_factory.create.return_value = [Mock(), Mock()]

        # when
        decision = self.sut.remote_config('test_key', self.user, 'STRING', 'default')

        # then
        self.assertEqual(DecisionReason.DEFAULT_RULE, decision.reason)
        self.assertEqual('vvv', decision.value)
        self.assertEqual(2, self.event_processor.process.call_count)
