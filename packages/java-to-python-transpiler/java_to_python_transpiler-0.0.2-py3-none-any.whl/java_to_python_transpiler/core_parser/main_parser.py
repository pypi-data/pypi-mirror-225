"""
The parser is the most important and complex part of the project
and, so I thought it necessary to divide it into multiple files

- Pre Declaration covers everything that happens before a class
declaration such as imports
- Class Declarations covers things like method lists and parameters
- Statements Semicolons are statements that don't need a semicolon
or "already have" a semi-colon like while loops
- Statements No Semicolons covers statements that don't already a
colon like return statements
- Expressions is self-explanatory
- Misc is everything else
"""

import sys

# tokens must be imported
from java_to_python_transpiler.lexer import tokens

# Parser imports
from java_to_python_transpiler.core_parser.pre_declaration import *
from java_to_python_transpiler.core_parser.class_declaration import *
from java_to_python_transpiler.core_parser.statements_semicolon import *
from java_to_python_transpiler.core_parser.statements_no_semicolon import *
from java_to_python_transpiler.core_parser.expressions import *
from java_to_python_transpiler.core_parser.misc import *

from java_to_python_transpiler.core_transpiler.main_transpiler import Transpiler
from java_to_python_transpiler.util import language_elements as comp

# Im not sure precedence even does anything since this is a transpiler
# and is not an interpreter
precedence = (
    ('left', '+', '-'),  # Level 1
    ('left', '*', '/'),  # Level 2
)

# Start is necessary since the grammar is broken up
start = "program"


def p_program(p):
    """
    program : class_declaration_with_comments
    """

    # - Program acts as the entry point for the parser
    # - This function creates and calls Transpiler.traverse()
    # - Though Transpiler.traverse() is a recursive method (thus, the
    # method takes in at least one argument), its argument defaults to
    # None which allows this function to call traverse() without any input
    # given to traverse()

    transpiler = Transpiler(p[1])
    p[0] = transpiler.traverse()


def p_class_declaration_with_comments(p):
    """
    class_declaration_with_comments : package_statement_or_empty pre_class_declaration_list class_declaration comment_list_or_empty
    """

    # This little line below will make this rule more readable
    class_declaration: comp.ClassDeclaration = p[3]

    # Package statement has to be seperate because there could be multiple
    class_declaration.package_statement = p[1]

    class_declaration.pre_class_declaration_list = p[2]
    class_declaration.comments_after = p[4]

    # Finally, pass ClassDeclaration through
    p[0] = p[3]


def p_error(p):
    print("Syntax Errror!")
    print(f"VALUE: {p.value}")
    print(f"TYPE: {p.type}")
    print(f"P: {p}")
