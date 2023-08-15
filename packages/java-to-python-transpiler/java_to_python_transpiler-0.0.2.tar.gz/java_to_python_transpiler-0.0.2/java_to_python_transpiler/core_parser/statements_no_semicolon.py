"""
STATEMENTS NO SEMICOLON:
    statement_without_semicolon : variable_declaration
                                | variable_initialization
                                | expression_statement
                                | return_statement
                                | variable_increment

    variable_declaration : variable_type identifier

    variable_initialization : variable_type identifier '=' expression

    expression_statement : expression

    return_statement : RETURN expression
                     | RETURN empty

    variable_increment : identifier '+' '+'
                       | identifier INC expression
"""


from java_to_python_transpiler.util import language_elements as comp


def p_statement_without_semicolon(p):
    """
    statement_without_semicolon : variable_declaration
                                | variable_initialization
                                | expression_statement
                                | return_statement
                                | variable_increment
    """

    # New Statement is grouped in w/ expr so it is not needed here
    # Consider chaning new statement to new expression

    p[0] = p[1]


def p_variable_declaration(p):
    """
    variable_declaration : variable_type identifier
    """
    
    p[0] = comp.VariableDeclaration(p[1], p[2])


def p_variable_initialization(p):
    """
    variable_initialization : variable_type identifier '=' expression
    """

    # incorporate variable declaration into this
    
    p[0] = comp.VariableInitialization(p[2], p[4])


def p_expression_statement(p):
    """
    expression_statement : expression
    """

    p[0] = comp.Expression(p[1], is_statement=True)


def p_return_statement(p):
    """
    return_statement : RETURN expression
                     | RETURN empty
    """

    p[0] = comp.ReturnStatement(p[2])


def p_variable_increment(p):
    """
    variable_increment : identifier '+' '+'
                       | identifier INC expression
    """

    if p[2] == "+":
        p[0] = comp.VariableIncrement(p[1])
    else:
        p[0] = comp.VariableIncrement(p[1], p[3])
