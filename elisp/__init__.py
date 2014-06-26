"""A simply Emacs Lisp parser for Python.

Supports the standard interface of loads.

"""

from elisp.semantics import loads
from elisp.types import ELispCons
from elisp.types import ELispSymbol, NIL
from elisp.types import ELispString, ELispUnibyteString, ELispMultibyteString


__all__ = [
    "loads",
    "ELispCons",
    "ELispSymbol", "NIL",
    "ELispString", "ELispUnibyteString", "ELispMultibyteString"
]

__author__ = "Jorgen Schaefer"
__version__ = "0.5"
__license__ = "LGPL"
