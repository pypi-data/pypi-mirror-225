from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.match.segment_condition_matcher import SegmentMatcher, SegmentConditionMatcher
from hackle.internal.model.entities import *
from tests.internal.evaluation.evaluator.experiment.test_experiment_request import create_experiment_request


class SegmentConditionMatcherTest(TestCase):

    def setUp(self):
        self.segment_matcher = Mock(spec=SegmentMatcher)
        self.sut = SegmentConditionMatcher(self.segment_matcher)

    def test_keyType이_SEGMENT_타입이_아니면_예외가_발생한다(self):
        # given
        condition = TargetCondition(
            TargetKey('USER_PROPERTY', "age"),
            TargetMatch('MATCH', 'IN', 'NUMBER', [30])
        )

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.matches(Mock(), Mock(), condition)

        # then
        self.assertEqual('Unsupported target.key.type [USER_PROPERTY]', str(actual.exception))

    def test_등록된_segmentKey가_String_타입이_아니면_예외가_발생한다(self):
        # given
        condition = TargetCondition(
            TargetKey('SEGMENT', "SEGMENT"),
            TargetMatch('MATCH', 'IN', 'NUMBER', [30])
        )

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.matches(Mock(), Mock(), condition)

        # then
        self.assertEqual('SegmentKey[30]', str(actual.exception))

    def test_등록된_segmentKey에_해당하는_Segment가_없으면_예외가_발생한다(self):
        # given
        condition = TargetCondition(
            TargetKey('SEGMENT', "SEGMENT"),
            TargetMatch('MATCH', 'IN', 'STRING', ["seg_01"])
        )
        workspace = WorkspaceStub()
        request = create_experiment_request(workspace=workspace)

        # when
        with self.assertRaises(Exception) as actual:
            self.sut.matches(request, Evaluator.context(), condition)

        # then
        self.assertEqual('Segment[seg_01]', str(actual.exception))

    def test_등록된_segment_중_일치하는게_하나라도_있으면_true(self):
        # given
        condition = TargetCondition(
            TargetKey('SEGMENT', "SEGMENT"),
            TargetMatch('MATCH', 'IN', 'STRING', ["seg_01"])
        )
        workspace = WorkspaceStub()
        workspace.add_segment("seg_01")
        self.segment_matcher.matches.return_value = True

        request = create_experiment_request(workspace=workspace)

        # when
        actual = self.sut.matches(request, Evaluator.context(), condition)

        # then
        self.assertTrue(actual)

    def test_TC_MatchType(self):
        # given
        condition = TargetCondition(
            TargetKey('SEGMENT', "SEGMENT"),
            TargetMatch('NOT_MATCH', 'IN', 'STRING', ["seg_01"])
        )
        workspace = WorkspaceStub()
        workspace.add_segment("seg_01")
        self.segment_matcher.matches.return_value = True

        request = create_experiment_request(workspace=workspace)

        # when
        actual = self.sut.matches(request, Evaluator.context(), condition)

        # then
        self.assertFalse(actual)

    def test_등록된_segment_중_일치하는게_없으면_false(self):
        # given
        condition = TargetCondition(
            TargetKey('SEGMENT', "SEGMENT"),
            TargetMatch('MATCH', 'IN', 'STRING', ["seg_01", "seg_02"])
        )
        workspace = WorkspaceStub()
        workspace.add_segment("seg_01")
        workspace.add_segment("seg_02")
        self.segment_matcher.matches.return_value = False

        request = create_experiment_request(workspace=workspace)

        # when
        actual = self.sut.matches(request, Evaluator.context(), condition)

        # then
        self.assertFalse(actual)


class WorkspaceStub:

    def __init__(self):
        self.segments = {}

    def add_segment(self, segment_key):
        self.segments[segment_key] = Mock()

    def get_segment_or_none(self, segment_key):
        return self.segments.get(segment_key)
