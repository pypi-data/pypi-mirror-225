"""
This file acts as the entry point for the transpiler
"""

#! Transpiler imports !#
from java_to_python_transpiler.core_transpiler.pre_declaration import *
from java_to_python_transpiler.core_transpiler.class_declaration import *
from java_to_python_transpiler.core_transpiler.statements_semicolon import *
from java_to_python_transpiler.core_transpiler.statements_no_semicolon import *
from java_to_python_transpiler.core_transpiler.expressions import *
from java_to_python_transpiler.core_transpiler.misc import *

from java_to_python_transpiler.util import language_elements as comp
from java_to_python_transpiler.util.code_emitter import CodeEmitter


class Transpiler(object):
    """
    Traverses the abstract syntax tree (ast) and produces the output
    in the programming language python
    """

    def __init__(self, ast: object):
        self.ast = ast
        self.indent_level = 0

        self.variable_list = []

    def traverse(self, current=None):
        # This if-statement exists for when traverse is initially called
        if current is None:
            current = self.ast

        # Pre Declaration Stuff
        if isinstance(current, comp.PackageStatement):
            return transpiler_package_statement(self, current)

        elif isinstance(current, comp.PreClassDeclarationList):
            return transpiler_pre_class_declaration_list(self, current)

        elif isinstance(current, comp.ImportStatement):
            return transpiler_import_statement(self, current)

        # Class Declaration!
        elif isinstance(current, comp.ClassDeclaration):
            return transpiler_class_declaration(self, current)

        elif isinstance(current, comp.ClassBody):
            return transpiler_class_body(self, current)

        elif isinstance(current, comp.MethodList):
            return transpiler_method_list(self, current)

        elif isinstance(current, comp.Method):
            return transpiler_method(self, current)

        elif isinstance(current, comp.ParameterList):
            return transpiler_parameter_list(self, current)

        elif isinstance(current, comp.StatementList):
            return transpiler_statement_list(self, current)

        # Statements Semicolon
        elif isinstance(current, comp.Statement):
            return transpiler_statement(self, current)

        elif isinstance(current, comp.IfStatement):
            return transpiler_if_statement(self, current)
        
        elif isinstance(current, comp.ComparisonExpression):
            return transpiler_comparison_expression(self, current)

        elif isinstance(current, comp.ComparisonOperator):
            return transpiler_comparison_operator(self, current)

        elif isinstance(current, comp.WhileStatement):
            return transpiler_while_statement(self, current)

        # Statements No Semicolon
        elif isinstance(current, comp.VariableDeclaration):
            return transpiler_variable_declaration(self, current)

        elif isinstance(current, comp.VariableInitialization):
            return transpiler_variable_initialization(self, current)

        elif isinstance(current, comp.ReturnStatement):
            return transpiler_return_statement(self, current)
        
        elif isinstance(current, comp.VariableIncrement):
            return transpiler_variable_increment(self, current)

        # Expressions        
        elif isinstance(current, comp.Expression):
            return transpiler_expression(self, current)

        elif isinstance(current, comp.Factor):
            return transpiler_factor(self, current)

        elif isinstance(current, comp.MethodCall):
            return transpiler_method_call(self, current)

        elif isinstance(current, comp.ArgumentList):
            return transpiler_argument_list(self, current)

        elif isinstance(current, comp.NewStatement):
            return transpiler_new_statement(self, current)

        # Misc
        elif isinstance(current, comp.CommentList):
            return transpiler_comment_list(self, current)
        
        elif isinstance(current, comp.Comment):
            return transpiler_comment(self, current)

        elif isinstance(current, comp.VariableType):
            return transpiler_variable_type(self, current)

        elif isinstance(current, comp.Identifier):
            return transpiler_identifier(self, current)

        elif isinstance(current, comp.QualifiedIdentifier):
            return transpiler_qualified_identifier(self, current)

        # Error Handling
        else:
            return f"A problem has occurred. {current} not found"
