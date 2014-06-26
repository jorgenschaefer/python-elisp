# coding: utf-8

import unittest

from elisp import types


class TestELispSymbol(unittest.TestCase):
    def test_should_create_string(self):
        sym = types.ELispSymbol("foo")

        self.assertEqual("foo", sym)

    def test_should_intern_string(self):
        sym1 = types.ELispSymbol("foo")
        sym2 = types.ELispSymbol("foo")

        self.assertIs(sym1, sym2)

    def test_should_interpreter_string_correctly(self):
        sym1 = types.ELispSymbol.from_string("f\\oo")
        sym2 = types.ELispSymbol.from_string("foo")

        self.assertIs(sym1, sym2)


class TestELispCons(unittest.TestCase):
    def test_should_have_car_and_cdr(self):
        cell = types.ELispCons("car", "cdr")

        self.assertEqual("car", cell.car)
        self.assertEqual("cdr", cell.cdr)

    def test_should_know_from_list(self):
        list_ = types.ELispCons.from_list([0, 1])

        self.assertEqual(0, list_.car)
        self.assertEqual(1, list_.cdr.car)
        self.assertEqual(types.NIL, list_.cdr.cdr)

    def test_should_know_from_list_with_tail(self):
        list_ = types.ELispCons.from_list([0, 1], 2)

        self.assertEqual(0, list_.car)
        self.assertEqual(1, list_.cdr.car)
        self.assertEqual(2, list_.cdr.cdr)


class TestELispString(unittest.TestCase):
    def test_should_know_multibyte_string(self):
        obj = types.ELispString.from_string(u"möp".encode("utf-8"))

        self.assertEqual(u"möp", obj)

    def test_should_unibyte_string(self):
        obj = types.ELispString.from_string(b"\xff")

        self.assertEqual(b'\xff', obj)

    def test_should_know_escape_newlines(self):
        obj = types.ELispString.from_string(b"foo\\\nbar")

        self.assertEqual(u"foobar", obj)

    def t(self, string, expected):
        actual = types.ELispString.from_string(string)

        self.assertEqual(expected, actual)

    def test_escapes(self):
        # \uNNNN
        self.t(br'\u00E4', u"ä")
        # \U00NNNNNN
        self.t(br'\U000000E4', u"ä")
        # \x[hex]+
        self.t(br'\xe4', u"ä")
        # \[oct]+
        self.t(br'\344', u"ä")
        # \a = 7
        self.t(br'\a', u"\x07")
        # \b = 8
        self.t(br'\b', u"\x08")
        # \t = 9
        self.t(br'\t', u"\x09")
        # \n = 10
        self.t(br'\n', u"\x0a")
        # \v = 11
        self.t(br'\v', u"\x0b")
        # \f = 12
        self.t(br'\f', u"\x0c")
        # \r = 13
        self.t(br'\r', u"\x0d")
        # \e = 27
        self.t(br'\e', u"\x1b")
        # \s = 32
        self.t(br'\s', u"\x20")
        # \\ = 92
        self.t(br'\\', u"\x5c")
        # \d = 127
        self.t(br'\d', u"\x7f")
