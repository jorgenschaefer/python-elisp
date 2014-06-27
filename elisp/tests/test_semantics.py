# coding: utf-8

import unittest

from elisp import semantics
from elisp import types


class LoadsTestCase(unittest.TestCase):
    def t(self, data, expected=None):
        if expected is None:
            expected = data
        parsed = semantics.loads(data)
        self.assertEqual([expected], parsed)


class TestComment(LoadsTestCase):
    def test(self):
        self.t("23 ; This is a comment", 23)


class TestQuote(LoadsTestCase):
    def test_simple_expression(self):
        expected = types.ELispCons.from_list(["quote", 23])
        self.t("'23", expected)

    def test_complex_expression(self):
        inner = types.ELispCons.from_list([1, 2, 3])
        expected = types.ELispCons.from_list(["quote", inner])
        self.t("'(1 2 3)", expected)


class TestInteger(LoadsTestCase):
    def test(self):
        self.t("-1", -1)
        self.t("1", 1)
        self.t("1.", 1)
        self.t("+1", 1)


class TestFloat(LoadsTestCase):
    def test(self):
        self.t("1500.0", 1500.0)
        self.t("15e2", 1500.0)
        self.t("15.0e2", 1500.0)
        self.t("1.5e3", 1500.0)
        self.t(".15e4", 1500.0)


class TestSymbol(LoadsTestCase):
    def test_should_parse_unescaped_symbol(self):
        self.t("foo")
        self.t("FOO")
        self.t("1+")
        self.t("+-*/_~!@$%^&=:<>{}")

    def test_should_parse_escaped_symbol(self):
        self.t(r"\+1", "+1")
        self.t(r"\(*\ 1\ 2\)", "(* 1 2)")

    def test_should_parse_keyword(self):
        self.t(":foo")

    def test_should_parse_symbols_with_dots(self):
        self.t("foo/bar.frob", "foo/bar.frob")
        self.t(".0000a", ".0000a")
        self.t("100a.", "100a.")


class TestCons(LoadsTestCase):
    def test_should_parse_list(self):
        obj = semantics.loads('(A 2 "A")')[0]
        self.assertEqual("A", obj.car)
        self.assertEqual(2, obj.cdr.car)
        self.assertEqual("A", obj.cdr.cdr.car)

        self.t("()", types.NIL)
        self.t("nil", types.NIL)

        obj = semantics.loads('("A ()")')[0]
        self.assertEqual("A ()", obj.car)

        obj = semantics.loads("(A ())")[0]
        self.assertEqual("A", obj.car)
        self.assertEqual(types.NIL, obj.cdr.car)

        obj = semantics.loads("(A nil)")[0]
        self.assertEqual("A", obj.car)
        self.assertEqual(types.NIL, obj.cdr.car)

        obj = semantics.loads("((A B C))")[0]
        self.assertEqual("A", obj.car.car)
        self.assertEqual("B", obj.car.cdr.car)
        self.assertEqual("C", obj.car.cdr.cdr.car)

        obj = semantics.loads("(1 2 3)")[0]
        self.assertEqual(1, obj.car)
        self.assertEqual(2, obj.cdr.car)
        self.assertEqual(3, obj.cdr.cdr.car)

    def test_should_parse_incomplete_list(self):
        obj = semantics.loads("(A . B)")[0]
        self.assertEqual("A", obj.car)
        self.assertEqual("B", obj.cdr)

        obj = semantics.loads("(A B . C)")[0]
        self.assertEqual("A", obj.car)
        self.assertEqual("B", obj.cdr.car)
        self.assertEqual("C", obj.cdr.cdr)


class TestString(LoadsTestCase):
    def test_empty_string(self):
        self.t('""', "")

    def test_single_line_string(self):
        self.t('"foo"', "foo")

    def test_multiline_string(self):
        s = '''"It is useful to include newlines
in documentation strings,
but the newline is \
ignored if escaped."'''
        expected = '''It is useful to include newlines
in documentation strings,
but the newline is ignored if escaped.'''
        self.t(s, expected)

    def test_multibyte_string(self):
        self.t(u'"möp"', u"möp")

    def test_escapes(self):
        # \uNNNN
        self.t(r'"\u00E4"', u"ä")
        # \U00NNNNNN
        self.t(r'"\U000000E4"', u"ä")
        # \x[hex]+
        self.t(r'"\xe4"', u"ä")
        # \[oct]+
        self.t(r'"\344"', u"ä")
        # \a = 7
        self.t(r'"\a"', u"\x07")
        # \b = 8
        self.t(r'"\b"', u"\x08")
        # \t = 9
        self.t(r'"\t"', u"\x09")
        # \n = 10
        self.t(r'"\n"', u"\x0a")
        # \v = 11
        self.t(r'"\v"', u"\x0b")
        # \f = 12
        self.t(r'"\f"', u"\x0c")
        # \r = 13
        self.t(r'"\r"', u"\x0d")
        # \e = 27
        self.t(r'"\e"', u"\x1b")
        # \s = 32
        self.t(r'"\s"', u"\x20")
        # \\ = 92
        self.t(r'"\\"', u"\x5c")
        # \d = 127
        self.t(r'"\d"', u"\x7f")


class TestVector(LoadsTestCase):
    def test(self):
        self.t('[]', [])
        self.t('[a b]', ["a", "b"])
