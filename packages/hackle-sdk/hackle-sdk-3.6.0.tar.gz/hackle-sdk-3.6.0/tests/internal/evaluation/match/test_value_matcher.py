from unittest import TestCase
from unittest.mock import Mock

from hackle.internal.evaluation.match.operator_matcher import OperatorMatcher, InMatcher
from hackle.internal.evaluation.match.value_matcher import StringValueMatcher, NumberValueMatcher, BoolValueMatcher, \
    VersionValueMatcher, NoneValueMatcher


class StringValueMatcherTest(TestCase):

    def setUp(self):
        self.sut = StringValueMatcher()

    def __check(self, user_value, match_value, is_matched):
        self.assertEqual(self.sut.matches(InMatcher(), user_value, match_value), is_matched)

    def test_string_type(self):
        self.__check("42", "42", True)

    def test_number_type(self):
        self.__check(42, 42, True)
        self.__check("42", 42, True)
        self.__check(42, "42", True)

        self.__check(42.42, 42.42, True)
        self.__check("42.42", 42.42, True)
        self.__check(42.42, "42.42", True)

        self.__check(42.0, 42.0, True)
        self.__check("42.0", 42.0, True)
        self.__check(42.0, "42.0", True)

    def test_unsupported_type(self):
        self.__check(True, True, False)
        self.__check(True, "True", False)
        self.__check("True", True, False)


class NumberValueMatcherTest(TestCase):

    def setUp(self):
        self.sut = NumberValueMatcher()

    def __check(self, user_value, match_value, is_matched):
        self.assertEqual(self.sut.matches(InMatcher(), user_value, match_value), is_matched)

    def test_number_type(self):
        self.__check(42, 42, True)
        self.__check(42.42, 42.42, True)
        self.__check(42.0, 42, True)
        self.__check(42, 42.0, True)
        self.__check(0, 0, True)

    def test_string_type(self):
        self.__check("42", "42", True)
        self.__check("42", 42, True)
        self.__check(42, "42", True)

        self.__check("42.42", "42.42", True)
        self.__check("42.42", 42.42, True)
        self.__check(42.42, "42.42", True)

        self.__check("42.0", "42.0", True)
        self.__check("42.0", 42.0, True)
        self.__check(42.0, "42.0", True)

    def test_unsupported_type(self):
        self.__check("42a", 42, False)
        self.__check(0, False, False)
        self.__check(True, True, False)


class BoolValueMatcherTest(TestCase):

    def setUp(self):
        self.sut = BoolValueMatcher()

    def test_user_value_match_value_둘다_Bool타입이면_operator_matcher의_일치_결과를_리턴(self):
        # given
        operator_matcher = Mock(spec=OperatorMatcher)
        operator_matcher.bool_matches.return_value = True

        # when
        actual = self.sut.matches(operator_matcher, True, True)

        # then
        self.assertTrue(actual)
        operator_matcher.bool_matches.assert_called_once_with(True, True)

    def test_user_value가_Bool_타입이_아니면_false(self):
        # given
        operator_matcher = Mock(spec=OperatorMatcher)

        # when
        actual = self.sut.matches(operator_matcher, 'True', True)

        # then
        self.assertFalse(actual)
        operator_matcher.assert_not_called()

    def test_user_value가_Bool타입이지만_match_value가_String타입이_아니면_false(self):
        # given
        operator_matcher = Mock(spec=OperatorMatcher)

        # when
        actual = self.sut.matches(operator_matcher, True, 'True')

        # then
        self.assertFalse(actual)
        operator_matcher.assert_not_called()


class VersionValueMatcherTest(TestCase):

    def setUp(self):
        self.sut = VersionValueMatcher()

    def test_user_value_match_value_둘다_version_타입이면_operator_matcher_결과를_리턴(self):
        # given
        operator_matcher = Mock(spec=OperatorMatcher)
        operator_matcher.version_matches.return_value = True

        # when
        actual = self.sut.matches(operator_matcher, '1.0.0', '2.0.0')

        # then
        self.assertTrue(actual)
        operator_matcher.version_matches.assert_called_once()

    def test_user_value가_version_타입이_아니면_False(self):
        # given
        operator_matcher = Mock(spec=OperatorMatcher)

        # when
        actual = self.sut.matches(operator_matcher, 1, '1.0.0')

        # then
        self.assertFalse(actual)
        operator_matcher.assert_not_called()

    def test_user_value가_version_타입이지만_match_value가_version_타입이_아니면_False(self):
        # given
        operator_matcher = Mock(spec=OperatorMatcher)

        # when
        actual = self.sut.matches(operator_matcher, '1.0.0', 1)

        # then
        self.assertFalse(actual)
        operator_matcher.assert_not_called()


class NoneValueMatcherTest(TestCase):

    def setUp(self):
        self.sut = NoneValueMatcher()

    def test_user_value_match_value_가_어떤_타입이건_False를_리턴(self):
        # given
        operator_matcher = Mock(spec=OperatorMatcher)

        # when
        # then
        self.assertFalse(self.sut.matches(operator_matcher, None, None))
        self.assertFalse(self.sut.matches(operator_matcher, None, 'test'))
        self.assertFalse(self.sut.matches(operator_matcher, 'test', 'test'))
        self.assertFalse(self.sut.matches(operator_matcher, 'test', 10))
        self.assertFalse(self.sut.matches(operator_matcher, 10, 10))
