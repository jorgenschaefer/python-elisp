import re

from elisp.compat import unichr


class ELispSymbol(str):
    obarray = {}

    def __new__(cls, string):
        obj = ELispSymbol.obarray.get(string)
        if obj is not None:
            return obj
        obj = super(ELispSymbol, cls).__new__(cls, string)
        ELispSymbol.obarray[string] = obj
        return obj

    @classmethod
    def from_string(cls, string):
        return cls(string.replace("\\", ""))


class ELispCons(object):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    @classmethod
    def from_list(cls, list_, tail=None):
        if tail is None:
            result = NIL
        else:
            result = tail
        for elt in reversed(list_):
            result = cls(elt, result)
        return result

    def __eq__(self, other):
        return self.car == other.car and self.cdr == other.cdr

    def __repr__(self):
        return "ELispCons({}, {})".format(repr(self.car),
                                          repr(self.cdr))

    def __getitem__(self, key):
        if key == 0:
            return self.car
        else:
            return self.cdr[key - 1]

    def __iter__(self):
        this = self
        while this != NIL:
            yield this.car
            this = this.cdr

    def __len__(self):
        result = 0
        this = self
        while isinstance(this, ELispCons):
            result += 1
            this = this.cdr
        if not isinstance(this, ELispNil):
            raise RuntimeError("Improper list has no length")
        return result


class ELispNil(ELispSymbol):
    def __new__(cls):
        return super(ELispNil, cls).__new__(cls, "nil")

    @property
    def car(self):
        return self

    @property
    def cdr(self):
        return self

    def __nonzero__(self):
        return False

    def __bool__(self):
        return False

    def __getitem__(self, key):
        return self

    def __iter__(self):
        return iter([])

    def __len__(self):
        return 0


NIL = ELispNil()


class ELispString(object):
    @classmethod
    def from_string(cls, string):
        string = cls._unescape(string)

        try:
            return ELispMultibyteString(string.decode("utf-8"))
        except (UnicodeDecodeError, UnicodeEncodeError, AttributeError):
            return ELispUnibyteString(string)

    @classmethod
    def _unescape(cls, string):
        def unicharescape(base):
            def transform(match):
                codepoint = int(match.group(1), base)
                return unichr(codepoint).encode("utf-8")
            return transform

        string = re.sub(br"\\u([0-9a-fA-F]{4})",
                        unicharescape(16),
                        string)
        string = re.sub(br"\\U00([0-9a-fA-F]{6})",
                        unicharescape(16),
                        string)
        string = re.sub(br"\\x([0-9a-fA-F]+)",
                        unicharescape(16),
                        string)
        string = re.sub(br"\\([0-7]+)",
                        unicharescape(8),
                        string)
        string = re.sub(br"\\a", b"\x07", string)
        string = re.sub(br"\\b", b"\x08", string)
        string = re.sub(br"\\t", b"\x09", string)
        string = re.sub(br"\\n", b"\x0a", string)
        string = re.sub(br"\\v", b"\x0b", string)
        string = re.sub(br"\\f", b"\x0c", string)
        string = re.sub(br"\\r", b"\x0d", string)
        string = re.sub(br"\\e", b"\x1b", string)
        string = re.sub(br"\\s", b" ", string)
        string = re.sub(br"\\\\", b"\\\\", string)
        string = re.sub(br"\\d", b"\x7f", string)
        string = re.sub(br"\\\n", b"", string)
        return string


class ELispMultibyteString(ELispString, type(u"unicode")):
    pass


class ELispUnibyteString(ELispString, bytearray):
    pass
