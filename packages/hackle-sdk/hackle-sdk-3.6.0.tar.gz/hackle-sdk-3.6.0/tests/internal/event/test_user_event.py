from unittest import TestCase

from hackle.decision import DecisionReason
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluation import ExperimentEvaluation
from hackle.internal.evaluation.evaluator.remoteconfig.remote_config_evaluation import RemoteConfigEvaluation
from hackle.internal.event.user_event import UserEvent, ExposureEvent, TrackEvent, RemoteConfigEvent
from hackle.internal.model.entities import ParameterConfiguration, EventType
from hackle.internal.user.internal_hackle_user import InternalHackleUser
from hackle.model import HackleEvent
from tests.internal.model.test_entities import create_experiment, create_parameter


class UserEventTest(TestCase):

    def test_exposure(self):
        config = ParameterConfiguration(42, {})

        experiment = create_experiment()
        evaluation = ExperimentEvaluation(
            DecisionReason.TRAFFIC_ALLOCATED,
            [],
            experiment,
            42,
            'B',
            config
        )
        user = InternalHackleUser.builder().identifier("$id", "test_id").build()

        event = UserEvent.exposure(user, evaluation, {"a": "1"}, 320)

        self.assertIsInstance(event, ExposureEvent)
        self.assertEqual(320, event.timestamp)
        self.assertEqual(user, event.user)
        self.assertEqual(experiment, event.experiment)
        self.assertEqual(42, event.variation_id)
        self.assertEqual('B', event.variation_key)
        self.assertEqual(DecisionReason.TRAFFIC_ALLOCATED, event.reason)
        self.assertEqual({"a": "1"}, event.properties)

    def test_track(self):
        user = InternalHackleUser.builder().identifier("$id", "test_id").build()
        event_type = EventType(320, 'test_event_key')
        event = HackleEvent.builder('test_event_key').build()

        user_event = UserEvent.track(user, event_type, event, 42)

        self.assertIsInstance(user_event, TrackEvent)
        self.assertEqual(42, user_event.timestamp)
        self.assertEqual(user, user_event.user)
        self.assertEqual(event_type, user_event.event_type)
        self.assertEqual(event, user_event.event)

    def test_remote_config(self):
        user = InternalHackleUser.builder().identifier("$id", "test_id").build()
        parameter = create_parameter()

        evaluation = RemoteConfigEvaluation(
            DecisionReason.DEFAULT_RULE,
            [],
            parameter,
            42,
            'final_value',
            {"a": "1"}
        )

        event = UserEvent.remote_config(user, evaluation, {"b": "2"}, 320)

        self.assertIsInstance(event, RemoteConfigEvent)
        self.assertEqual(320, event.timestamp)
        self.assertEqual(user, event.user)
        self.assertEqual(parameter, event.parameter)
        self.assertEqual(42, event.value_id)
        self.assertEqual(DecisionReason.DEFAULT_RULE, event.reason)
        self.assertEqual({"b": "2"}, event.properties)
