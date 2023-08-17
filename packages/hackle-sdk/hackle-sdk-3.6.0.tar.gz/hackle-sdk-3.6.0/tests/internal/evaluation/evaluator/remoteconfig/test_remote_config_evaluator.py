from unittest import TestCase
from unittest.mock import Mock

from hackle.decision import DecisionReason
from hackle.internal.evaluation.evaluator.evaluator import Evaluator
from hackle.internal.evaluation.evaluator.experiment.experiment_request import ExperimentRequest
from hackle.internal.evaluation.evaluator.remoteconfig.remote_config_evaluator import RemoteConfigEvaluator
from hackle.internal.evaluation.evaluator.remoteconfig.remote_config_request import RemoteConfigRequest
from hackle.internal.evaluation.target.remote_config_target_rule_determiner import RemoteConfigTargetRuleDeterminer
from hackle.internal.model.entities import RemoteConfigParameterValue, RemoteConfigTargetRule
from tests.internal.evaluation.evaluator.remoteconfig.test_remote_config_request import create_remote_config_request
from tests.internal.model.test_entities import create_parameter


class RemoteConfigEvaluatorTest(TestCase):

    def setUp(self):
        self.target_rule_determiner = Mock(spec=RemoteConfigTargetRuleDeterminer)
        self.target_rule_determiner.determine_target_rule_or_none.return_value = None

        self.sut = RemoteConfigEvaluator(self.target_rule_determiner)

    def test_supports(self):
        self.assertFalse(self.sut.supports(Mock(spec=ExperimentRequest)))
        self.assertTrue(self.sut.supports(Mock(spec=RemoteConfigRequest)))

    def test__evaluate__circular_call(self):
        request = create_remote_config_request()
        context = Evaluator.context()
        context.add_request(request)

        with self.assertRaises(Exception) as actual:
            self.sut.evaluate(request, context)

        self.assertIn('Circular evaluation has occurred', str(actual.exception))

    def test__evaluate__identifier_not_found(self):
        # given
        parameter = create_parameter(
            type='STRING',
            identifier_type='custom_id',
            default_value=RemoteConfigParameterValue(43, 'parameter_default')
        )

        request = create_remote_config_request(parameter=parameter, default_value='sdk_default')

        # when
        actual = self.sut.evaluate(request, Evaluator.context())

        # then
        self.assertEqual(DecisionReason.IDENTIFIER_NOT_FOUND, actual.reason)
        self.assertEqual('sdk_default', actual.value)
        self.assertEqual(
            {'requestValueType': 'STRING', 'requestDefaultValue': 'sdk_default', 'returnValue': 'sdk_default'},
            actual.properties)

    def test__evaluate__target_rule_match(self):
        # given
        target_rule = RemoteConfigTargetRule(
            'target_rule_key',
            'target_rule_name',
            Mock(),
            42,
            RemoteConfigParameterValue(320, 'target_rule_value')
        )

        parameter = create_parameter(
            type='STRING',
            target_rules=[target_rule],
            default_value=RemoteConfigParameterValue(43, 'parameter_default')
        )

        self.target_rule_determiner.determine_target_rule_or_none.return_value = target_rule

        request = create_remote_config_request(parameter=parameter, default_value='sdk_default')

        # when
        actual = self.sut.evaluate(request, Evaluator.context())

        # then
        self.assertEqual(DecisionReason.TARGET_RULE_MATCH, actual.reason)
        self.assertEqual(320, actual.value_id)
        self.assertEqual('target_rule_value', actual.value)
        self.assertEqual(
            {
                'requestValueType': 'STRING',
                'requestDefaultValue': 'sdk_default',
                'returnValue': 'target_rule_value',
                'targetRuleKey': 'target_rule_key',
                'targetRuleName': 'target_rule_name'
            },
            actual.properties)

    def test__evaluate__default_rule(self):
        # given
        target_rule = RemoteConfigTargetRule(
            'target_rule_key',
            'target_rule_name',
            Mock(),
            42,
            RemoteConfigParameterValue(320, 'target_rule_value')
        )

        parameter = create_parameter(
            type='STRING',
            target_rules=[target_rule],
            default_value=RemoteConfigParameterValue(43, 'parameter_default')
        )

        self.target_rule_determiner.determine_target_rule_or_none.return_value = None

        request = create_remote_config_request(parameter=parameter, default_value='sdk_default')

        # when
        actual = self.sut.evaluate(request, Evaluator.context())

        # then
        self.assertEqual(DecisionReason.DEFAULT_RULE, actual.reason)
        self.assertEqual(43, actual.value_id)
        self.assertEqual('parameter_default', actual.value)
        self.assertEqual(
            {
                'requestValueType': 'STRING',
                'requestDefaultValue': 'sdk_default',
                'returnValue': 'parameter_default',
            },
            actual.properties)

    def test_type_match(self):
        self.__assert_type_match('STRING', 'match_string', 'default_string', True)
        self.__assert_type_match('STRING', '', 'default_string', True)
        self.__assert_type_match('STRING', 0, 'default_string', False)
        self.__assert_type_match('STRING', 1, 'default_string', False)
        self.__assert_type_match('STRING', False, 'default_string', False)
        self.__assert_type_match('STRING', True, 'default_string', False)

        self.__assert_type_match('NUMBER', 0, 999, True)
        self.__assert_type_match('NUMBER', 1, 999, True)
        self.__assert_type_match('NUMBER', -1, 999, True)
        self.__assert_type_match('NUMBER', 0.0, 999, True)
        self.__assert_type_match('NUMBER', 1.0, 999, True)
        self.__assert_type_match('NUMBER', -1.0, 999, True)
        self.__assert_type_match('NUMBER', 1.1, 999, True)
        self.__assert_type_match('NUMBER', '1', 999, False)
        self.__assert_type_match('NUMBER', '0', 999, False)
        self.__assert_type_match('NUMBER', True, 999, False)
        self.__assert_type_match('NUMBER', False, 999, False)

        self.__assert_type_match('BOOLEAN', True, False, True)
        self.__assert_type_match('BOOLEAN', False, True, True)
        self.__assert_type_match('BOOLEAN', 0, True, False)
        self.__assert_type_match('BOOLEAN', 1, False, False)

        self.__assert_type_match('NULL', 'match_string', None, True)
        self.__assert_type_match('NULL', 1, None, True)
        self.__assert_type_match('NULL', True, None, True)
        self.__assert_type_match('NULL', False, None, True)

        self.__assert_type_match('VERSION', '1.0.0', 'default', False)
        self.__assert_type_match('JSON', '{}', 'default', False)
        self.__assert_type_match('UNKNOWN', '{}', 'default', False)

    def __assert_type_match(self, required_type, match_value, default_value, is_match):
        parameter = create_parameter(
            type='STRING',
            default_value=RemoteConfigParameterValue(43, match_value)
        )
        request = create_remote_config_request(
            parameter=parameter, required_type=required_type, default_value=default_value)

        actual = self.sut.evaluate(request, Evaluator.context())

        if is_match:
            self.assertEqual(43, actual.value_id)
            self.assertEqual(match_value, actual.value)
            self.assertEqual(DecisionReason.DEFAULT_RULE, actual.reason)
        else:
            self.assertEqual(None, actual.value_id)
            self.assertEqual(default_value, actual.value)
            self.assertEqual(DecisionReason.TYPE_MISMATCH, actual.reason)
