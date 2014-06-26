# Python 2/3 compability

try:
    from __builtin__ import unichr
except ImportError:
    unichr = chr
