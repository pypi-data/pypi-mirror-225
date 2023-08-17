from unittest import TestCase
from unittest.mock import Mock

from hackle.decision import DecisionReason
from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluation import ExperimentEvaluation
from hackle.internal.evaluation.evaluator.remoteconfig.remote_config_evaluation import RemoteConfigEvaluation
from hackle.internal.event.event_dispatcher import EventDispatcher
from hackle.internal.event.user_event import UserEvent
from hackle.internal.http.http_client import HttpClient
from hackle.internal.model.entities import EventType
from hackle.internal.model.properties_builder import PropertiesBuilder
from hackle.internal.user.identifier_type import IdentifierType
from hackle.internal.user.internal_hackle_user import InternalHackleUser
from hackle.model import HackleEvent
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request
from tests.internal.evaluation.evaluator.remoteconfig.test_remote_config_request import create_remote_config_request


class EventDispatcherTest(TestCase):

    def test_dispatch(self):
        user = InternalHackleUser.builder() \
            .identifier(IdentifierType.ID, "id") \
            .identifier(IdentifierType.USER, "user_id") \
            .identifier(IdentifierType.DEVICE, "device_id") \
            .property('age', 42) \
            .build()

        experiment_evaluation = ExperimentEvaluation.of_default(
            create_experiment_request(), Evaluator.context(), DecisionReason.TRAFFIC_ALLOCATED)
        exposure_event = UserEvent.exposure(user, experiment_evaluation, {}, 42)

        event = HackleEvent.builder('test').property('amount', 4200).build()
        track_event = UserEvent.track(user, EventType(2, 'test'), event, 43)

        remote_config_evaluation = RemoteConfigEvaluation.of_default(
            create_remote_config_request(), Evaluator.context(), DecisionReason.DEFAULT_RULE, PropertiesBuilder())
        remote_config_event = UserEvent.remote_config(user, remote_config_evaluation, {}, 44)

        http_client = Mock(spec=HttpClient)
        sut = EventDispatcher('localhost', http_client)

        sut.dispatch([exposure_event, track_event, remote_config_event])

        http_client.post.assert_called_once()
        self.assertEqual('localhost/api/v2/events', http_client.post.call_args[0][0])
        a = len(http_client.post.call_args[0][1])
        self.assertGreater(len(http_client.post.call_args[0][1]), 1000)
