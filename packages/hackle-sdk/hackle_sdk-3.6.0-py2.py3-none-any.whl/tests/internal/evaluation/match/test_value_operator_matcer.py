from unittest import TestCase

from hackle.internal.evaluation.match.operator_matcher import *
from hackle.internal.evaluation.match.value_matcher import *
from hackle.internal.evaluation.match.value_operator_matcher import ValueOperatorMatcherFactory, ValueOperatorMatcher
from hackle.internal.model.entities import TargetMatch
from tests import base


class ValueOperatorMatcherTest(TestCase):

    def setUp(self):
        self.sut = ValueOperatorMatcher(ValueOperatorMatcherFactory())

    def test_match_values중_하나라도_일치하는_값이_있으면_true(self):
        # given
        match = TargetMatch(
            type='MATCH',
            operator='IN',
            value_type='NUMBER',
            values=[1, 2, 3]
        )

        # when
        actual = self.sut.matches(3, match)

        # then
        self.assertTrue(actual)

    def test_match_values중_일치하는_값이_하나도_없으면_false(self):
        # given
        match = TargetMatch(
            type='MATCH',
            operator='IN',
            value_type='NUMBER',
            values=[1, 2, 3]
        )

        # when
        actual = self.sut.matches(4, match)

        # then
        self.assertFalse(actual)

    def test_일치하는_값이_있지만_match_type이_NOT_MATCH면_false(self):
        # given
        match = TargetMatch(
            type='NOT_MATCH',
            operator='IN',
            value_type='NUMBER',
            values=[1, 2, 3]
        )

        # when
        actual = self.sut.matches(3, match)

        # then
        self.assertFalse(actual)

    def test_일치하는_값이_없지만_match_type이_NOT_MATCH면_true(self):
        # given
        match = TargetMatch(
            type='NOT_MATCH',
            operator='IN',
            value_type='NUMBER',
            values=[1, 2, 3]
        )

        # when
        actual = self.sut.matches(4, match)

        # then
        self.assertTrue(actual)

    def test_user_value_가_array_인_경우_하나라도_매칭되면_true(self):
        # given
        match = TargetMatch(
            type='MATCH',
            operator='IN',
            value_type='NUMBER',
            values=[1, 2, 3]
        )

        sut = ValueOperatorMatcher(ValueOperatorMatcherFactory())

        # when
        actual = sut.matches([-1, 0, 1], match)

        # then
        self.assertTrue(actual)

    def test_array_user_value_중_매치되는게_하나도_없으면_false(self):
        # given
        match = TargetMatch(
            type='MATCH',
            operator='IN',
            value_type='NUMBER',
            values=[1, 2, 3]
        )

        sut = ValueOperatorMatcher(ValueOperatorMatcherFactory())

        # when
        actual = sut.matches([4, 5, 6], match)

        # then
        self.assertFalse(actual)

    def test_array_user_value_가_empty_인_경우_false(self):
        # given
        match = TargetMatch(
            type='MATCH',
            operator='IN',
            value_type='NUMBER',
            values=[1, 2, 3]
        )

        sut = ValueOperatorMatcher(ValueOperatorMatcherFactory())

        # when
        actual = sut.matches([], match)

        # then
        self.assertFalse(actual)


class ValueOperatorMatcherFactoryTest(base.BaseTest):

    def test_value_matcher(self):
        sut = ValueOperatorMatcherFactory()
        self.assertIsInstance(sut.get_value_matcher_or_none('STRING'), StringValueMatcher)
        self.assertIsInstance(sut.get_value_matcher_or_none('NUMBER'), NumberValueMatcher)
        self.assertIsInstance(sut.get_value_matcher_or_none('BOOLEAN'), BoolValueMatcher)
        self.assertIsInstance(sut.get_value_matcher_or_none('VERSION'), VersionValueMatcher)

    def test_operator_matcher(self):
        sut = ValueOperatorMatcherFactory()
        self.assertIsInstance(sut.get_operator_matcher_or_none('IN'), InMatcher)
        self.assertIsInstance(sut.get_operator_matcher_or_none('CONTAINS'), ContainsMatcher)
        self.assertIsInstance(sut.get_operator_matcher_or_none('STARTS_WITH'), StartsWithMatcher)
        self.assertIsInstance(sut.get_operator_matcher_or_none('ENDS_WITH'), EndsWithMatcher)
        self.assertIsInstance(sut.get_operator_matcher_or_none('GT'), GreaterThanMatcher)
        self.assertIsInstance(sut.get_operator_matcher_or_none('GTE'), GreaterThanOrEqualToMatcher)
        self.assertIsInstance(sut.get_operator_matcher_or_none('LT'), LessThanMatcher)
        self.assertIsInstance(sut.get_operator_matcher_or_none('LTE'), LessThanOrEqualToMatcher)
