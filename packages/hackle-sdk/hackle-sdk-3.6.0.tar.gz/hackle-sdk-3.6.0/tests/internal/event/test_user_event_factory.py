from unittest import TestCase

from hackle.decision import DecisionReason
from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.evaluator.experiment.experiment_evaluation import ExperimentEvaluation
from hackle.internal.evaluation.evaluator.remoteconfig.remote_config_evaluation import RemoteConfigEvaluation
from hackle.internal.event.user_event import RemoteConfigEvent, ExposureEvent
from hackle.internal.event.user_event_factory import UserEventFactory
from hackle.internal.model.entities import ParameterConfiguration
from hackle.internal.model.properties_builder import PropertiesBuilder
from tests.internal.evaluation.evaluator.remoteconfig.test_remote_config_request import create_remote_config_request
from tests.internal.model.test_entities import create_experiment
from tests.internal.time.test_clock import FixedClock


class UserEventFactoryTest(TestCase):
    def test_create(self):
        sut = UserEventFactory(FixedClock(47, 48))

        context = Evaluator.context()
        evaluation_1 = ExperimentEvaluation(
            DecisionReason.TRAFFIC_ALLOCATED,
            [],
            create_experiment(id=1),
            42,
            'B',
            ParameterConfiguration(42, {})
        )

        evaluation_2 = ExperimentEvaluation(
            DecisionReason.DEFAULT_RULE,
            [],
            create_experiment(id=2, type='FEATURE_FLAG', version=2, execution_version=3),
            320,
            'A',
            None
        )

        context.add_evaluation(evaluation_1)
        context.add_evaluation(evaluation_2)

        request = create_remote_config_request()
        evaluation = RemoteConfigEvaluation.of(
            request,
            context,
            999,
            'RC',
            DecisionReason.TARGET_RULE_MATCH,
            PropertiesBuilder()
        )

        events = sut.create(request, evaluation)

        self.assertTrue(3, len(events))

        self.assertIsInstance(events[0], RemoteConfigEvent)
        self.assertEqual(47, events[0].timestamp)
        self.assertEqual(request.user, events[0].user)
        self.assertEqual(request.parameter, events[0].parameter)
        self.assertEqual(999, events[0].value_id)
        self.assertEqual(DecisionReason.TARGET_RULE_MATCH, events[0].reason)
        self.assertEqual({'returnValue': 'RC'}, events[0].properties)

        self.assertIsInstance(events[1], ExposureEvent)
        self.assertEqual(47, events[1].timestamp)
        self.assertEqual(request.user, events[1].user)
        self.assertEqual(evaluation_1.experiment, events[1].experiment)
        self.assertEqual(42, events[1].variation_id)
        self.assertEqual('B', events[1].variation_key)
        self.assertEqual(DecisionReason.TRAFFIC_ALLOCATED, events[1].reason)
        self.assertEqual(
            {
                '$targetingRootType': 'REMOTE_CONFIG',
                '$targetingRootId': 1,
                '$parameterConfigurationId': 42,
                '$experiment_version': 1,
                '$execution_version': 1
            },
            events[1].properties)

        self.assertIsInstance(events[2], ExposureEvent)
        self.assertEqual(47, events[2].timestamp)
        self.assertEqual(request.user, events[2].user)
        self.assertEqual(evaluation_2.experiment, events[2].experiment)
        self.assertEqual(320, events[2].variation_id)
        self.assertEqual('A', events[2].variation_key)
        self.assertEqual(DecisionReason.DEFAULT_RULE, events[2].reason)
        self.assertEqual(
            {
                '$targetingRootType': 'REMOTE_CONFIG',
                '$targetingRootId': 1,
                '$experiment_version': 2,
                '$execution_version': 3
            },
            events[2].properties)
