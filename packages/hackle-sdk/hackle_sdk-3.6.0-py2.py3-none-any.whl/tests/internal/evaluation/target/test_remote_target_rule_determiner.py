from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.bucket.bucketer import Bucketer
from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.match.target_matcher import TargetMatcher
from hackle.internal.evaluation.target.remote_config_target_rule_determiner import RemoteConfigTargetRuleDeterminer, \
    RemoteConfigTargetRuleMatcher
from hackle.internal.model.entities import *
from hackle.internal.workspace.workspace import Workspace
from tests.internal.evaluation.evaluator.remoteconfig.test_remote_config_request import create_remote_config_request
from tests.internal.model.test_entities import create_parameter


class RemoteConfigTargetRuleDeterminerTest(TestCase):

    def setUp(self):
        self.matches = []
        self.matcher = Mock(spec=RemoteConfigTargetRuleMatcher)
        self.matcher.matches = Mock(side_effect=self.matches)
        self.sut = RemoteConfigTargetRuleDeterminer(self.matcher)

    def test_등록된_rule이_없는경우_None리턴(self):
        # given
        parameter = create_parameter()
        request = create_remote_config_request(parameter=parameter)

        # when
        actual = self.sut.determine_target_rule_or_none(request, Evaluator.context())

        # then
        self.assertIsNone(actual)

    def test_등록된_규칙중_일치하는_첫번쨰_규칙을_리턴한다(self):
        # given
        parameter = create_parameter(target_rules=[
            self.__target_rule(False),
            self.__target_rule(False),
            self.__target_rule(False),
            self.__target_rule(False),
            self.__target_rule(True),
            self.__target_rule(False),
        ])
        request = create_remote_config_request(parameter=parameter)

        # when
        actual = self.sut.determine_target_rule_or_none(request, Evaluator.context())

        # then
        self.assertEqual(parameter.target_rules[4], actual)
        self.assertEqual(5, self.matcher.matches.call_count)

    def test_등록된_규칙중_일치하는_규칙이_하나도_없는경우_None리턴(self):
        parameter = create_parameter(target_rules=[
            self.__target_rule(False),
            self.__target_rule(False),
            self.__target_rule(False),
            self.__target_rule(False),
            self.__target_rule(False),
            self.__target_rule(False),
        ])
        request = create_remote_config_request(parameter=parameter)

        # when
        actual = self.sut.determine_target_rule_or_none(request, Evaluator.context())

        # then
        self.assertIsNone(actual)
        self.assertEqual(6, self.matcher.matches.call_count)

    def __target_rule(self, is_match):
        self.matches.append(is_match)
        target_rule = Mock(spec=RemoteConfigTargetRule)
        return target_rule


class RemoteConfigTargetRuleMatcherTest(TestCase):

    def setUp(self):
        self.target_matcher = Mock(spec=TargetMatcher)
        self.bucketer = Mock(spec=Bucketer)
        self.sut = RemoteConfigTargetRuleMatcher(self.target_matcher, self.bucketer)

    def test_target_rule_not_matched(self):
        target_rule = self.__target_rule(False)
        request = create_remote_config_request()

        actual = self.sut.matches(request, Evaluator.context(), target_rule)

        self.assertFalse(actual)

    def test_identifier_not_found(self):
        target_rule = self.__target_rule(True)
        request = create_remote_config_request(parameter=create_parameter(identifier_type='custom_id'))

        actual = self.sut.matches(request, Evaluator.context(), target_rule)

        self.assertFalse(actual)

    def test_bucket_not_found(self):
        target_rule = self.__target_rule(True)
        target_rule.bucket_id = 42

        request = create_remote_config_request()

        with self.assertRaises(Exception) as actual:
            self.sut.matches(request, Evaluator.context(), target_rule)

        self.assertEqual('Bucket[42]', str(actual.exception))

    def test_not_allocated(self):
        target_rule = self.__target_rule(True)
        target_rule.bucket_id = 42

        workspace = Mock(spec=Workspace)
        workspace.get_bucket_or_none.return_value = Mock()

        self.bucketer.bucketing.return_value = None

        request = create_remote_config_request(workspace=workspace, parameter=create_parameter())

        actual = self.sut.matches(request, Evaluator.context(), target_rule)

        self.assertFalse(actual)

    def test_allocated(self):
        target_rule = self.__target_rule(True)
        target_rule.bucket_id = 42

        workspace = Mock(spec=Workspace)
        workspace.get_bucket_or_none.return_value = Mock()

        self.bucketer.bucketing.return_value = Mock()

        request = create_remote_config_request(workspace=workspace, parameter=create_parameter())

        actual = self.sut.matches(request, Evaluator.context(), target_rule)

        self.assertTrue(actual)

    def __target_rule(self, is_match):
        self.target_matcher.matches.return_value = is_match
        target_rule = Mock(spec=RemoteConfigTargetRule)
        target_rule.target = Mock()
        return target_rule
