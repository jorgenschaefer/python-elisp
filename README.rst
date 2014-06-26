=================
Emacs Lisp Parser
=================

A simple package to parse Emacs Lisp expressions from Python.

.. image:: https://secure.travis-ci.org/jorgenschaefer/python-elisp.png?branch=master
   :target: http://travis-ci.org/jorgenschaefer/python-elisp?branch=master

.. image:: https://coveralls.io/repos/jorgenschaefer/python-elisp/badge.png?branch=master
   :target: https://coveralls.io/r/jorgenschaefer/python-elisp?branch=master


Simple Usage
============

.. code-block:: python

   >>> import elisp
   >>> numbers = elisp.loads("(1 2 3)")
   >>> numbers.car
   1
   >>> numbers.cdr.cdr.car
   3
   >>> numbers.cdr.cdr.cdr is elisp.NIL
   True


Type Mappings
=============

The following types are supported and are mapped to the respective
Python types.

- ``integer`` to ``int``
- ``float`` to ``float``
- ``symbol`` to ``elisp.ELispSymbol``, a subclass of ``str``
- ``list``, ``cons`` to ``elisp.ELispCons``
- ``unibyte string`` to ``bytearray``
- ``multibyte string`` to ``unicode`` (without the ``\C-a`` syntax)
- ``vector`` to ``list``


Unsupported Types
-----------------

The following types are not supported:

- Characters (like ``?a`` or ``?\C-f``)
- Char-Table
- Bool-Vector
- Hash Table
- Byte-Code


Grammar
=======

See the file `elisp.ebnf`_ for the grammar used by
this package.

.. _elisp.ebnf: https://github.com/jorgenschaefer/python-elisp/blob/master/elisp/elisp.ebnf
