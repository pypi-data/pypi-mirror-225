"""
This module contains functions to utilize the transpiler
"""


from ply import lex, yacc


def transpile_code(
        java_code: str, lexer: lex.Lexer,
        yacc_parser: yacc.LRParser) -> str:
    """
    This function takes in 3 arguments: "java_code", "lexer", and "yacc_parser"

    This function returns a string

    This function takes in "java_code" and transpiles it into Python code.
    This code is then returned as a string
    """

    built_lexer = lex.lex(module=lexer)
    built_parser = yacc.yacc(module=yacc_parser)
    transpiled_result = built_parser.parse(java_code, lexer=built_lexer)

    return transpiled_result


def transpile_java_file(
        java_file_path: str, lexer: lex.Lexer,
        yacc_parser: yacc.LRParser) -> str:

    """
    This function takes in 3 arguments: "java_file_path",
    "lexer", and "yacc_parser"

    This function returns a string.

    This function takes in a Java file and transpiles it into Python code.
    This code is then returned as a string.
    """

    with open(java_file_path, "r") as java_file:
        data = java_file.read()

        return transpile_code(data, lexer, yacc_parser)
