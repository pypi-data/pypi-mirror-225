from unittest import TestCase

from hackle.internal.evaluation.match.operator_matcher import *


class OperatorMatcherTest(TestCase):

    # IN
    def test_in_string(self):
        sut = InMatcher()
        self.assertTrue(sut.string_matches('abc', 'abc'))
        self.assertFalse(sut.string_matches('abc', 'abc1'))
        self.assertFalse(sut.string_matches('1', 1))
        self.assertFalse(sut.string_matches(1, 1))

    def test_in_number(self):
        sut = InMatcher()
        self.assertTrue(sut.number_matches(320, 320))
        self.assertFalse(sut.number_matches(320, 3200))
        self.assertFalse(sut.number_matches(320, '320'))
        self.assertFalse(sut.number_matches('320', '320'))
        self.assertFalse(sut.number_matches(0, False))
        self.assertFalse(sut.number_matches(False, 0))
        self.assertFalse(sut.number_matches(False, False))
        self.assertFalse(sut.number_matches(1, True))
        self.assertFalse(sut.number_matches(True, 1))
        self.assertFalse(sut.number_matches(True, True))

    def test_in_bool(self):
        sut = InMatcher()
        self.assertTrue(sut.bool_matches(True, True))
        self.assertFalse(sut.bool_matches(True, False))
        self.assertTrue(sut.bool_matches(False, False))
        self.assertFalse(sut.bool_matches(False, True))
        self.assertFalse(sut.bool_matches(True, 'True'))
        self.assertFalse(sut.bool_matches('True', True))
        self.assertFalse(sut.bool_matches('True', True))
        self.assertFalse(sut.number_matches(0, False))
        self.assertFalse(sut.number_matches(False, 0))
        self.assertFalse(sut.number_matches(False, False))
        self.assertFalse(sut.number_matches(1, True))
        self.assertFalse(sut.number_matches(True, 1))
        self.assertFalse(sut.number_matches(True, True))

    def test_in_version(self):
        sut = InMatcher()
        self.assertTrue(sut.version_matches(self.v('1.0.0'), self.v('1.0.0')))
        self.assertFalse(sut.version_matches(self.v('1.0.0'), self.v('2.0.0')))

    # CONTAINS
    def test_contains_string(self):
        sut = ContainsMatcher()
        self.assertTrue(sut.string_matches('abc', 'abc'))
        self.assertTrue(sut.string_matches('abc', 'a'))
        self.assertTrue(sut.string_matches('abc', 'b'))
        self.assertTrue(sut.string_matches('abc', 'c'))
        self.assertTrue(sut.string_matches('abc', 'ab'))
        self.assertFalse(sut.string_matches('abc', 'ac'))
        self.assertFalse(sut.string_matches('a', 'acb'))
        self.assertFalse(sut.string_matches('1', 1))
        self.assertFalse(sut.string_matches(1, 1))

    def test_continas_number(self):
        sut = ContainsMatcher()
        self.assertFalse(sut.number_matches(1, 1))
        self.assertFalse(sut.number_matches(11, 1))

    def test_contains_bool(self):
        sut = ContainsMatcher()
        self.assertFalse(sut.bool_matches(True, True))
        self.assertFalse(sut.bool_matches(True, False))
        self.assertFalse(sut.bool_matches(False, False))
        self.assertFalse(sut.bool_matches(False, True))

    def test_contains_version(self):
        sut = ContainsMatcher()
        self.assertFalse(sut.version_matches(self.v('1.0.0'), self.v('1.0.0')))
        self.assertFalse(sut.version_matches(self.v('1.0.0'), self.v('2.0.0')))

    # STARTS_WITH
    def test_starts_with_string(self):
        sut = StartsWithMatcher()
        self.assertTrue(sut.string_matches('abc', 'abc'))
        self.assertTrue(sut.string_matches('abc', 'a'))
        self.assertFalse(sut.string_matches('abc', 'b'))
        self.assertFalse(sut.string_matches('a', 'ab'))
        self.assertFalse(sut.string_matches('1', 1))
        self.assertFalse(sut.string_matches(1, 1))

    def test_starts_with_number(self):
        sut = StartsWithMatcher()
        self.assertFalse(sut.number_matches(1, 1))
        self.assertFalse(sut.number_matches(11, 1))
        self.assertFalse(sut.number_matches(1, 11))

    def test_starts_with_bool(self):
        sut = StartsWithMatcher()
        self.assertFalse(sut.bool_matches(True, True))
        self.assertFalse(sut.bool_matches(True, False))
        self.assertFalse(sut.bool_matches(False, False))
        self.assertFalse(sut.bool_matches(False, True))

    def test_starts_with_version(self):
        sut = StartsWithMatcher()
        self.assertFalse(sut.version_matches(self.v('1.0.0'), self.v('1.0.0')))
        self.assertFalse(sut.version_matches(self.v('1.0.0'), self.v('2.0.0')))

    # ENS_WITH
    def test_ends_with_string(self):
        sut = EndsWithMatcher()
        self.assertTrue(sut.string_matches('abc', 'abc'))
        self.assertFalse(sut.string_matches('abc', 'a'))
        self.assertTrue(sut.string_matches('abc', 'c'))
        self.assertTrue(sut.string_matches('abc', 'bc'))
        self.assertFalse(sut.string_matches('a', 'ab'))
        self.assertFalse(sut.string_matches('1', 1))
        self.assertFalse(sut.string_matches(1, 1))

    def test_ends_with_number(self):
        sut = EndsWithMatcher()
        self.assertFalse(sut.number_matches(1, 1))
        self.assertFalse(sut.number_matches(11, 1))
        self.assertFalse(sut.number_matches(1, 11))

    def test_ends_with_bool(self):
        sut = EndsWithMatcher()
        self.assertFalse(sut.bool_matches(True, True))
        self.assertFalse(sut.bool_matches(True, False))
        self.assertFalse(sut.bool_matches(False, False))
        self.assertFalse(sut.bool_matches(False, True))

    def test_ends_with_version(self):
        sut = EndsWithMatcher()
        self.assertFalse(sut.version_matches(self.v('1.0.0'), self.v('1.0.0')))
        self.assertFalse(sut.version_matches(self.v('1.0.0'), self.v('2.0.0')))

    # GT
    def test_gt_string(self):
        sut = GreaterThanMatcher()
        self.assertFalse(sut.string_matches('41', '42'))
        self.assertFalse(sut.string_matches('42', '42'))
        self.assertTrue(sut.string_matches('43', '42'))

        self.assertFalse(sut.string_matches('20230114', '20230115'))
        self.assertFalse(sut.string_matches('20230115', '20230115'))
        self.assertTrue(sut.string_matches('20230116', '20230115'))

        self.assertFalse(sut.string_matches('2023-01-14', '2023-01-15'))
        self.assertFalse(sut.string_matches('2023-01-15', '2023-01-15'))
        self.assertTrue(sut.string_matches('2023-01-16', '2023-01-15'))

        self.assertFalse(sut.string_matches('a', 'a'))
        self.assertTrue(sut.string_matches('a', 'A'))
        self.assertFalse(sut.string_matches('A', 'a'))
        self.assertTrue(sut.string_matches('aa', 'a'))
        self.assertFalse(sut.string_matches('a', 'aa'))

    def test_gt_number(self):
        sut = GreaterThanMatcher()
        self.assertTrue(sut.number_matches(1.0001, 1))
        self.assertTrue(sut.number_matches(2, 1))
        self.assertFalse(sut.number_matches(1, 1))
        self.assertFalse(sut.number_matches(1, 2))
        self.assertFalse(sut.number_matches(0.9999, 1))
        self.assertFalse(sut.number_matches('2', 1))
        self.assertFalse(sut.number_matches(2, '1'))

    def test_gt_bool(self):
        sut = GreaterThanMatcher()
        self.assertFalse(sut.bool_matches(True, True))
        self.assertFalse(sut.bool_matches(True, False))
        self.assertFalse(sut.bool_matches(False, False))
        self.assertFalse(sut.bool_matches(False, True))

    def test_gt_version(self):
        sut = GreaterThanMatcher()
        self.assertFalse(sut.version_matches(self.v('1.0.0'), self.v('1.0.0')))
        self.assertFalse(sut.version_matches(self.v('1.0.0'), self.v('2.0.0')))
        self.assertTrue(sut.version_matches(self.v('2.0.0'), self.v('1.0.0')))

    # GTE
    def test_gte_string(self):
        sut = GreaterThanOrEqualToMatcher()
        self.assertFalse(sut.string_matches('41', '42'))
        self.assertTrue(sut.string_matches('42', '42'))
        self.assertTrue(sut.string_matches('43', '42'))

        self.assertFalse(sut.string_matches('20230114', '20230115'))
        self.assertTrue(sut.string_matches('20230115', '20230115'))
        self.assertTrue(sut.string_matches('20230116', '20230115'))

        self.assertFalse(sut.string_matches('2023-01-14', '2023-01-15'))
        self.assertTrue(sut.string_matches('2023-01-15', '2023-01-15'))
        self.assertTrue(sut.string_matches('2023-01-16', '2023-01-15'))

        self.assertTrue(sut.string_matches('a', 'a'))
        self.assertTrue(sut.string_matches('a', 'A'))
        self.assertFalse(sut.string_matches('A', 'a'))
        self.assertTrue(sut.string_matches('aa', 'a'))
        self.assertFalse(sut.string_matches('a', 'aa'))

    def test_gte_number(self):
        sut = GreaterThanOrEqualToMatcher()
        self.assertTrue(sut.number_matches(1.0001, 1))
        self.assertTrue(sut.number_matches(2, 1))
        self.assertTrue(sut.number_matches(1, 1))
        self.assertFalse(sut.number_matches(1, 2))
        self.assertFalse(sut.number_matches(0.9999, 1))
        self.assertFalse(sut.number_matches('1', 1))
        self.assertFalse(sut.number_matches(1, '1'))

    def test_gte_bool(self):
        sut = GreaterThanOrEqualToMatcher()
        self.assertFalse(sut.bool_matches(True, True))
        self.assertFalse(sut.bool_matches(True, False))
        self.assertFalse(sut.bool_matches(False, False))
        self.assertFalse(sut.bool_matches(False, True))

    def test_gte_version(self):
        sut = GreaterThanOrEqualToMatcher()
        self.assertTrue(sut.version_matches(self.v('1.0.0'), self.v('1.0.0')))
        self.assertFalse(sut.version_matches(self.v('1.0.0'), self.v('2.0.0')))
        self.assertTrue(sut.version_matches(self.v('2.0.0'), self.v('1.0.0')))

    # LT
    def test_lt_string(self):
        sut = LessThanMatcher()
        self.assertTrue(sut.string_matches('41', '42'))
        self.assertFalse(sut.string_matches('42', '42'))
        self.assertFalse(sut.string_matches('43', '42'))

        self.assertTrue(sut.string_matches('20230114', '20230115'))
        self.assertFalse(sut.string_matches('20230115', '20230115'))
        self.assertFalse(sut.string_matches('20230116', '20230115'))

        self.assertTrue(sut.string_matches('2023-01-14', '2023-01-15'))
        self.assertFalse(sut.string_matches('2023-01-15', '2023-01-15'))
        self.assertFalse(sut.string_matches('2023-01-16', '2023-01-15'))

        self.assertFalse(sut.string_matches('a', 'a'))
        self.assertFalse(sut.string_matches('a', 'A'))
        self.assertTrue(sut.string_matches('A', 'a'))
        self.assertFalse(sut.string_matches('aa', 'a'))
        self.assertTrue(sut.string_matches('a', 'aa'))

    def test_lt_number(self):
        sut = LessThanMatcher()
        self.assertFalse(sut.number_matches(1.0001, 1))
        self.assertFalse(sut.number_matches(2, 1))
        self.assertFalse(sut.number_matches(1, 1))
        self.assertTrue(sut.number_matches(1, 2))
        self.assertTrue(sut.number_matches(0.9999, 1))
        self.assertFalse(sut.number_matches('1', 2))
        self.assertFalse(sut.number_matches(1, '2'))

    def test_lt_bool(self):
        sut = LessThanMatcher()
        self.assertFalse(sut.bool_matches(True, True))
        self.assertFalse(sut.bool_matches(True, False))
        self.assertFalse(sut.bool_matches(False, False))
        self.assertFalse(sut.bool_matches(False, True))

    def test_lt_version(self):
        sut = LessThanMatcher()
        self.assertFalse(sut.version_matches(self.v('1.0.0'), self.v('1.0.0')))
        self.assertTrue(sut.version_matches(self.v('1.0.0'), self.v('2.0.0')))
        self.assertFalse(sut.version_matches(self.v('2.0.0'), self.v('1.0.0')))

    # LTE
    def test_lte_string(self):
        sut = LessThanOrEqualToMatcher()
        self.assertTrue(sut.string_matches('41', '42'))
        self.assertTrue(sut.string_matches('42', '42'))
        self.assertFalse(sut.string_matches('43', '42'))

        self.assertTrue(sut.string_matches('20230114', '20230115'))
        self.assertTrue(sut.string_matches('20230115', '20230115'))
        self.assertFalse(sut.string_matches('20230116', '20230115'))

        self.assertTrue(sut.string_matches('2023-01-14', '2023-01-15'))
        self.assertTrue(sut.string_matches('2023-01-15', '2023-01-15'))
        self.assertFalse(sut.string_matches('2023-01-16', '2023-01-15'))

        self.assertTrue(sut.string_matches('a', 'a'))
        self.assertFalse(sut.string_matches('a', 'A'))
        self.assertTrue(sut.string_matches('A', 'a'))
        self.assertFalse(sut.string_matches('aa', 'a'))
        self.assertTrue(sut.string_matches('a', 'aa'))

    def test_lte_number(self):
        sut = LessThanOrEqualToMatcher()
        self.assertFalse(sut.number_matches(1.0001, 1))
        self.assertFalse(sut.number_matches(2, 1))
        self.assertTrue(sut.number_matches(1, 1))
        self.assertTrue(sut.number_matches(1, 2))
        self.assertTrue(sut.number_matches(0.9999, 1))
        self.assertFalse(sut.number_matches('1', 1))
        self.assertFalse(sut.number_matches(1, '1'))

    def test_lte_bool(self):
        sut = LessThanOrEqualToMatcher()
        self.assertFalse(sut.bool_matches(True, True))
        self.assertFalse(sut.bool_matches(True, False))
        self.assertFalse(sut.bool_matches(False, False))
        self.assertFalse(sut.bool_matches(False, True))

    def test_lte_version(self):
        sut = LessThanOrEqualToMatcher()
        self.assertTrue(sut.version_matches(self.v('1.0.0'), self.v('1.0.0')))
        self.assertTrue(sut.version_matches(self.v('1.0.0'), self.v('2.0.0')))
        self.assertFalse(sut.version_matches(self.v('2.0.0'), self.v('1.0.0')))

    @staticmethod
    def v(version):
        return SemanticVersion.parse_or_none(version)
