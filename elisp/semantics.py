from . import parser
from . import types


def loads(data):
    p = parser.elispParser(nameguard=False,
                           semantics=ELispSemantics(),
                           comments_re=";.*")
    return p.parse(data,
                   rule_name="file")


class ELispSemantics(object):
    def integer(self, ast):
        return int(ast.rstrip("."))

    def float(self, ast):
        return float(ast)

    def symbol(self, ast):
        return types.ELispSymbol.from_string(ast)

    def proper_list(self, ast):
        return types.ELispCons.from_list(ast[0])

    def improper_list(self, ast):
        return types.ELispCons.from_list(ast[0], ast[2])

    def vector(self, ast):
        return list(ast)

    def string(self, ast):
        return types.ELispString.from_string(ast.encode("utf-8"))

    def _default(self, ast):
        return ast
