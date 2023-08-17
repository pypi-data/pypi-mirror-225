from unittest import TestCase

from hackle.decision import DecisionReason
from hackle.internal.event.user_event import RemoteConfigEvent, ExposureEvent
from hackle.internal.hackle_core import HackleCore
from hackle.internal.user.identifier_type import IdentifierType
from hackle.internal.user.internal_hackle_user import InternalHackleUser
from tests.internal.event.test_in_memory_event_processor import InMemoryEventProcessor
from tests.internal.workspace.test_resource_workspace_fetcher import ResourceWorkspaceFetcher


class HackleCoreTest2(TestCase):

    #
    #      RC(1)
    #     /     \
    #    /       \
    # AB(2)     FF(4)
    #   |   \     |
    #   |     \   |
    # AB(3)     FF(5)
    #             |
    #             |
    #           AB(6)
    #
    def test_target_experiment(self):
        workspace_fetcher = ResourceWorkspaceFetcher('target_experiment.json')
        event_processor = InMemoryEventProcessor()
        # noinspection PyTypeChecker
        core = HackleCore.create(workspace_fetcher, event_processor)

        user = InternalHackleUser.builder().identifier(IdentifierType.ID, "user").build()
        decision = core.remote_config('rc', user, 'STRING', '42')

        self.assertEqual('Targeting!!', decision.value)
        self.assertEqual(DecisionReason.TARGET_RULE_MATCH, decision.reason)

        event = event_processor.processed_events[0]
        self.assertIsInstance(event, RemoteConfigEvent)
        self.assertEqual(
            {
                "requestValueType": "STRING",
                "requestDefaultValue": "42",
                "targetRuleKey": "rc_1_key",
                "targetRuleName": "rc_1_name",
                "returnValue": "Targeting!!"
            },
            event.properties
        )

        for event in event_processor.processed_events[1:]:
            self.assertIsInstance(event, ExposureEvent)
            self.assertEqual(
                {
                    "$targetingRootType": "REMOTE_CONFIG",
                    "$targetingRootId": 1,
                    "$experiment_version": 1,
                    "$execution_version": 1
                },
                event.properties
            )

    #
    #     RC(1)
    #      ↓
    # ┌── AB(2)
    # ↑    ↓
    # |   FF(3)
    # ↑    ↓
    # |   AB(4)
    # └────┘
    #
    def test_experiment_circular(self):
        workspace_fetcher = ResourceWorkspaceFetcher('target_experiment_circular.json')
        event_processor = InMemoryEventProcessor()
        # noinspection PyTypeChecker
        core = HackleCore.create(workspace_fetcher, event_processor)

        user = InternalHackleUser.builder().identifier(IdentifierType.ID, "user").build()

        with self.assertRaises(Exception) as actual:
            core.remote_config('rc', user, 'STRING', 'XXX')

        self.assertIn('Circular evaluation has occurred', str(actual.exception))

    #
    #                     Container(1)
    # ┌──────────────┬───────────────────────────────────────┐
    # | ┌──────────┐ |                                       |
    # | |   AB(2)  | |                                       |
    # | └──────────┘ |                                       |
    # └──────────────┴───────────────────────────────────────┘
    #       25 %                        75 %
    #
    def test_container(self):
        workspace_fetcher = ResourceWorkspaceFetcher('container.json')
        event_processor = InMemoryEventProcessor()
        # noinspection PyTypeChecker
        core = HackleCore.create(workspace_fetcher, event_processor)

        decisions = []
        for i in range(0, 10000):
            user = InternalHackleUser.builder().identifier(IdentifierType.ID, str(i)).build()
            decisions.append(core.experiment(2, user, 'A'))

        self.assertEqual(10000, len(event_processor.processed_events))
        self.assertEqual(10000, len(decisions))
        self.assertEqual(2452, len(list(filter(lambda it: it.reason == 'TRAFFIC_ALLOCATED', decisions))))
        self.assertEqual(7548,
                         len(list(filter(lambda it: it.reason == 'NOT_IN_MUTUAL_EXCLUSION_EXPERIMENT', decisions))))

    def test_segment_match(self):
        workspace_fetcher = ResourceWorkspaceFetcher('segment_match.json')
        event_processor = InMemoryEventProcessor()
        # noinspection PyTypeChecker
        core = HackleCore.create(workspace_fetcher, event_processor)

        user_1 = InternalHackleUser.builder().identifier(IdentifierType.ID, "matched_id").build()
        decision_1 = core.experiment(1, user_1, 'A')
        self.assertEqual('A', decision_1.variation)
        self.assertEqual(DecisionReason.OVERRIDDEN, decision_1.reason)

        user_2 = InternalHackleUser.builder().identifier(IdentifierType.ID, "not_matched_id").build()
        decision_2 = core.experiment(1, user_2, 'A')
        self.assertEqual('A', decision_2.variation)
        self.assertEqual(DecisionReason.TRAFFIC_ALLOCATED, decision_2.reason)
