import math

from hackle.internal.type import hackle_types
from tests import base


class HackleTypesTest(base.BaseTest):
    def test_is_string(self):
        self.assertTrue(hackle_types.is_string('str'))
        self.assertTrue(hackle_types.is_string('42'))
        self.assertTrue(hackle_types.is_string(''))
        self.assertFalse(hackle_types.is_string(42))
        self.assertFalse(hackle_types.is_string(True))
        self.assertFalse(hackle_types.is_string({}))
        self.assertFalse(hackle_types.is_string(None))

    def test_is_empty_string(self):
        self.assertTrue(hackle_types.is_empty_string(''))
        self.assertFalse(hackle_types.is_empty_string(' '))
        self.assertFalse(hackle_types.is_empty_string('42'))
        self.assertFalse(hackle_types.is_empty_string(42))
        self.assertFalse(hackle_types.is_empty_string(True))
        self.assertFalse(hackle_types.is_empty_string({}))
        self.assertFalse(hackle_types.is_empty_string(None))

    def test_is_not_empty_string(self):
        self.assertFalse(hackle_types.is_not_empty_string(''))
        self.assertTrue(hackle_types.is_not_empty_string(' '))
        self.assertTrue(hackle_types.is_not_empty_string('42'))
        self.assertFalse(hackle_types.is_not_empty_string(42))
        self.assertFalse(hackle_types.is_not_empty_string(True))
        self.assertFalse(hackle_types.is_not_empty_string({}))
        self.assertFalse(hackle_types.is_not_empty_string(None))

    def test_is_number(self):
        self.assertTrue(hackle_types.is_number(42))
        self.assertTrue(hackle_types.is_number(42.0))
        self.assertTrue(hackle_types.is_number(42.42))
        self.assertTrue(hackle_types.is_number(-42))
        self.assertTrue(hackle_types.is_number(-42.0))
        self.assertTrue(hackle_types.is_number(-42.42))
        self.assertTrue(hackle_types.is_number(math.nan))
        self.assertTrue(hackle_types.is_number(math.inf))
        self.assertFalse(hackle_types.is_number('42'))
        self.assertFalse(hackle_types.is_number(False))
        self.assertFalse(hackle_types.is_number(True))
        self.assertFalse(hackle_types.is_number({}))
        self.assertFalse(hackle_types.is_number(None))

    def test_is_finite_number(self):
        self.assertTrue(hackle_types.is_finite_number(42))
        self.assertTrue(hackle_types.is_finite_number(42.0))
        self.assertTrue(hackle_types.is_finite_number(42.42))
        self.assertTrue(hackle_types.is_finite_number(-42))
        self.assertTrue(hackle_types.is_finite_number(-42.0))
        self.assertTrue(hackle_types.is_finite_number(-42.42))
        self.assertFalse(hackle_types.is_finite_number(math.nan))
        self.assertFalse(hackle_types.is_finite_number(math.inf))
        self.assertFalse(hackle_types.is_finite_number('42'))
        self.assertFalse(hackle_types.is_finite_number(False))
        self.assertFalse(hackle_types.is_finite_number(True))
        self.assertFalse(hackle_types.is_finite_number({}))
        self.assertFalse(hackle_types.is_finite_number(None))

    def test_is_positive_int(self):
        self.assertTrue(hackle_types.is_positive_int(42))
        self.assertFalse(hackle_types.is_positive_int(42.0))
        self.assertFalse(hackle_types.is_positive_int(42.42))
        self.assertFalse(hackle_types.is_positive_int(0))
        self.assertFalse(hackle_types.is_positive_int(-42))
        self.assertFalse(hackle_types.is_positive_int(-42.0))
        self.assertFalse(hackle_types.is_positive_int(-42.42))
        self.assertFalse(hackle_types.is_positive_int(math.nan))
        self.assertFalse(hackle_types.is_positive_int(math.inf))
        self.assertFalse(hackle_types.is_positive_int('42'))
        self.assertFalse(hackle_types.is_positive_int(False))
        self.assertFalse(hackle_types.is_positive_int(True))
        self.assertFalse(hackle_types.is_positive_int({}))
        self.assertFalse(hackle_types.is_positive_int(None))

    def test_is_bool(self):
        self.assertTrue(hackle_types.is_bool(True))
        self.assertTrue(hackle_types.is_bool(False))
        self.assertFalse(hackle_types.is_bool(1))
        self.assertFalse(hackle_types.is_bool(0))
        self.assertFalse(hackle_types.is_bool(-1))
        self.assertFalse(hackle_types.is_bool("True"))
        self.assertFalse(hackle_types.is_bool("False"))
