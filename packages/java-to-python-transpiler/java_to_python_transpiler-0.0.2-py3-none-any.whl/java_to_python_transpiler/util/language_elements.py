from __future__ import annotations

import enum
from typing import *
from dataclasses import dataclass


"""
This module contains elements that are used in the Python language and they are
represented here as classes
"""


@dataclass
class ClassDeclaration(object):
    """
    ClassDeclaration is a language element that specifies the declaration of
    a class

    - identifier refers to the name of the class that is being declared
    - class_body refers to the ClassBody object that contains methods, fields,
    etc.
    - inherited_body (optional) refers to the parent class for the class that
    is being declared
    - package_statement (optional) is grouped together with class_declaration;
    however, it is separate
    - pre_class_declaration_list (optional) refers to comments, and import
    statements that precede the class_declaration. As with package_statement,
    it is more convenient to group it in with the class_declaration
    - comments_after (optional) refers to comments that appear after the
    class_declaration
    """

    identifier: Identifier
    class_body: ClassBody

    inherited_class: Optional[QualifiedIdentifier] = None   
    package_statement: Optional[PackageStatement] = None
    pre_class_declaration_list: Optional[PreClassDeclarationList] = None
    comments_after: Optional[Comment] = None


@dataclass
class VariableType(object):
    """
    VariableType is a language element that specifies the type of variable

    - variable_type refers to the string or Identifier that specifies the type
    of variable that was used
    """

    variable_type: Union[AnyStr, Identifier]


@dataclass
class PackageStatement(object):
    """
    PackageStatement is a language element that specifies the path of the
    package

    - qualified_identifier refers to the path of the package
    """

    qualified_identifier: QualifiedIdentifier


@dataclass
class PreClassDeclarationList(object):
    """
    PreClassDeclarationList is a language element that specifies the elements
    that precede the ClassDeclaration

    - statement (optional) refers to the PackageStatement or CommentList that
    precedes the ClassDeclaration

    - additional_list (optional) allows this class to chain itself and add more
    statements
    """

    statement: Union[PackageStatement, CommentList, None] = None
    additional_list: Optional[PreClassDeclarationList] = None


@dataclass
class CommentList(object):
    """
    CommentList is a language element that represents a list of comments

    - comment is a singular comment
    - additional_list (optional) allows this class to chain itself and add more
    comments
    """

    comment: Comment
    additional_list: Optional[CommentList] = None


@dataclass
class Comment(object):
    """
    Comment is a language element that represents a piece of code excluded from
    evaluation

    - value refers to the string containing the contents of the comment
    - is_statement (optional) refers to the boolean that specifies if the
    comment is a statement or not (it requires a newline if it is)
    """

    value: AnyStr
    is_statement: bool = False


@dataclass
class ImportStatement(object):
    """
    ImportStatement is a language element that represents a package, file, or
    class that is imported into the file

    - qualified_identifier refers to the path of this package, file, or class
    """

    qualified_identifier: QualifiedIdentifier


@dataclass
class Identifier(object):
    """
    Identifier is a language element that represents identifiers

    - value refers to the string value of the identifier

    __str__ method returns the value attribute
    """
    
    value: AnyStr

    def __str__(self) -> str:
        return self.value


@dataclass
class ClassBody(object):
    """
    ClassBody is a language element that represents the body of a class\

    - method_list refers to the list of methods inside of class
    """

    method_list: MethodList


@dataclass
class MethodList(object):
    """
    MethodList is a language element that represents a list of methods in a
    class

    - method_or_comment (optional) refers to a method or comment inside a class
    - additional_list (optional) allows this class to chain itself and add more
    methods
    """

    method_or_comment: Union[Method, Comment, None] = None
    additional_list: Optional[MethodList] = None


@dataclass
class Method(object):
    """
    Method is a language element that represents a method in a class
    - identifier refers to the name of the method
    - parameter_list refers to the list of the parameters for the method
    - statement_list refers to the list of the statements for the method

    - comments_only (optional) refers to a boolean that specifies if the method
    only contains comments (if so, a pass statement must be appended at
    transpile time)
    """

    identifier: Identifier
    parameter_list: ParameterList
    statement_list: StatementList

    comments_only: bool = True


@dataclass
class ParameterList(object):
    """
    ParameterList is a language element that represents a list of parameters

    - identifier (optional) refers to the name of the parameter
    - additional_list (optional) allows this class to chain itself and add more
    parameters
    """

    identifier: Optional[Identifier] = None
    additional_list: Optional[ParameterList] = None


@dataclass
class StatementList(object):
    """
    StatementList is a language element that represents a list of statements

    - statement (optional) refers to a statement
    - additional_list (optional) allows this class to chain itself and add more
    statements
    """

    statement: Optional[Statement] = None
    additional_list: Optional[StatementList] = None


@dataclass
class Statement(object):
    """
    Statement is a language element that represents a statement such as an
    If Statement or a While Statement

    - statement_body refers to various types of statements in the Python
    language
    """

    statement_body: Union[
        VariableDeclaration, VariableInitialization, Expression,
        ReturnStatement, VariableIncrement, IfStatement, WhileStatement,
        Comment
    ]


@dataclass
class VariableDeclaration(object):
    """
    VariableDeclaration is a language element that represents a declared
    variable

    - variable_type refers to the type of variable
    - identifier refers to the name of the variable
    """

    variable_type: VariableType
    identifier: Identifier


@dataclass
class VariableInitialization(object):
    """
    VariableInitialization is a language element that represents a variable
    being initialized

    - key_identifier refers to the name of the variable (key meaning that
    variables and their value are a key-value pair)
    - expression refers to the value of the variable
    """

    key_identifier: Identifier
    expression: Expression


@dataclass
class Expression(object):
    """
    Expression is a language element that represents any Python expression

    - left_expression (optional) refers to the chain part of an expression
    - operator (optional) refers to the operator used in the expression
    - right_expression (optional) refers to the unchained part of an expression
    - is_statement (optional) is a boolean that specifies whether the
    expression is a statement or not
    - with_parenthesis (optional) is a boolean that specifies whether the
    expression is  surrounded by parenthesis
    """

    left_expression: Union[Factor, Expression, None] = None
    operator: Optional[Operator] = None
    right_expression: Union[Factor, Expression, None] = None
    is_statement: bool = False
    with_parenthesis: bool = False


class Operator(enum.Enum):
    """
    Operator is a language element (and enumeration) that holds the operators
    of Python used in expressions (arithmetic operators)
    """

    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULUS = "%"


@dataclass
class Factor(object):
    """
    Factor is a language element that represents a single component of an
    expression

    - value refers to a string or Identifier that is the value of a Factor
    """

    value: Union[AnyStr, Identifier]
    

@dataclass
class QualifiedIdentifier(object):
    """
    QualifiedIdentifier is a language element that represents a more complex
    identifier

    - identifier refers to a single (unchained) identifier

    - qualified_identifier (optional) refers to a chain of
    qualified_identifiers

    __str__(), __repr__(), and __eq__() all have been implemented
    """

    identifier: Identifier
    qualified_identifier: Optional[QualifiedIdentifier] = None

    def __str__(self):
        if self.qualified_identifier is None:
            return str(self.identifier)

        return str(self.identifier) + "." + str(self.qualified_identifier)

    def __repr__(self):
        return str(self)


@dataclass
class MethodCall(object):
    """
    MethodCall is a language element that represents a called method in Python

    - qualified_identifier refers to a complex identifier
    - argument_list refers to a list of arguments
    """

    qualified_identifier: Union[QualifiedIdentifier, Identifier]
    argument_list: ArgumentList


@dataclass
class ArgumentList(object):
    """
    ArgumentList is a language element that represents a list of arguments

    - argument (optional) refers to a single (unchained) argument
    - additional_list (optional) allows this class to chain itself and add more
    arguments
    """

    argument: Optional[Factor] = None
    additional_list: Optional[ArgumentList] = None


@dataclass
class NewStatement(object):
    """
    NewStatement is a language element that represents that creation of a new
    object in Python (instantiation)

    - qualified_identifier refers to the name of the class being called
    - argument_list refers to the list of arguments input into the instance
    """
    qualified_identifier: QualifiedIdentifier
    argument_list: ArgumentList


@dataclass
class ReturnStatement(object):
    """
    ReturnStatement is a language element that represents a return statement

    - expression refers to the expression that is returned
    """

    expression: Union[Expression, Factor]


@dataclass
class VariableIncrement(object):
    """
    VariableIncrement is a language element that represents the increase of a
    variable

    - identifier refers to the name of variable
    - amount (optional) refers to the value that the variable is incremented by
    """

    identifier: Identifier
    amount: Union[Expression, AnyStr] = "1"


@dataclass
class IfStatement(object):
    """
    IfStatement is a language element that represents an if statement

    - comparison_expression refers to the expression that returns a boolean
    and is the condition for the if_statement

    statement_list_or_empty (optional) refers to the list of statements that
    are executed if the IfStatement is true
    else_statement_or_empty (optional) refers to the else clause of an if
    statement
    """

    comparison_expression: ComparisonExpression
    statement_list_or_empty: Optional[StatementList] = None
    else_statement_or_empty: Optional[StatementList] = None


@dataclass
class ComparisonExpression(object):
    """
    ComparisonExpression is a language element that evaluates to a boolean
    value

    - left_expression refers to the required part of a comparison expression

    - operator (optional) refers to the comparison operator used in the
    comparison expression
    - right_expression (optional) refers to the chained part of a comparison
    expression
    """

    left_expression: Union[ComparisonExpression, AnyStr]
    operator: Optional[ComparisonOperator] = None
    right_expression: Optional[ComparisonExpression] = None


class ComparisonOperator(enum.Enum):
    """
    ComparisonOperator is an enumeration that collects every comparison
    operator (==, !=, > , etc.)
    """

    BOOL_EQ = "=="
    NOT_EQ = "!="
    GT_OR_EQ = ">="
    LT_OR_EQ = "<="
    GT = ">"
    LT = "<"


@dataclass
class WhileStatement(object):
    """
    WhileStatement is a langauge element that represents a while loop

    - comparison_expression refers to the condition of the while loop

    - statement_list_or_empty (optional) refers to the statements contained
    inside the while loop
    """

    comparison_expression: ComparisonExpression
    statement_list_or_empty: Optional[StatementList] = None
