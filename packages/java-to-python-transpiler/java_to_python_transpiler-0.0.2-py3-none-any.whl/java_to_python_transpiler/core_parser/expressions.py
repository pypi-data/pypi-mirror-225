"""
EXPRESSIONS:
    expression : expression '+' expression
               | expression '-' expression
               | expression '*' expression
               | expression '/' expression
               | '(' expression ')'
               | factor

    factor : DEC_LIT
           | FLOAT_LIT
           | STR_LIT
           | CHAR_LIT
           | unary_minus
           | qualified_identifier
           | method_call
           | new_statement

    unary_minus : '-' DEC_LIT
                | '-' FLOAT_LIT

    method_call : qualified_identifier '(' argument_list ')'

    argument_list : expression
                  | expression ',' argument_list
                  | empty

    new_statement : NEW qualified_identifier '(' argument_list ')'
"""


from java_to_python_transpiler.util import language_elements as comp


def p_expression(p):
    """
    expression : expression '+' expression
               | expression '-' expression
               | expression '*' expression
               | expression '/' expression
               | expression '%' expression
               | '(' expression ')'
               | factor
    """

    # Im fairly certain that new statement is used in expressions

    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '(':
        p[0] = comp.Expression(p[2], with_parenthesis=True)
    else:
        if p[2] == "+":
            operator = comp.Operator.PLUS
        elif p[2] == "-":
            operator = comp.Operator.MINUS
        elif p[2] == "*":
            operator = comp.Operator.MULTIPLY
        elif p[2] == "/":
            operator = comp.Operator.DIVIDE
        elif p[2] == "%":
            operator = comp.Operator.MODULUS

        p[0] = comp.Expression(p[1], operator, p[3])


def p_factor(p):
    """
    factor : DEC_LIT
           | FLOAT_LIT
           | STR_LIT
           | CHAR_LIT
           | unary_minus
           | qualified_identifier
           | method_call
           | new_statement
    """

    # Factor omits identifier in its definition because qualified_ident
    # can be an identifier.

    p[0] = comp.Factor(p[1])


def p_unary_minus(p):
    """
    unary_minus : '-' DEC_LIT
                | '-' FLOAT_LIT
    """

    # Pretty barbaric but it is what is    
    p[0] = p[1] + p[2]


def p_method_call(p):
    """
    method_call : qualified_identifier '(' argument_list ')'
    """

    p[0] = comp.MethodCall(p[1], p[3])


def p_argument_list(p):
    """
    argument_list : expression
                  | expression ',' argument_list
                  | empty
    """

    if p[1] is None:
        p[0] = comp.ArgumentList()
    elif len(p) == 2:
        p[0] = comp.ArgumentList(p[1])
    elif len(p) == 4:
        p[0] = comp.ArgumentList(p[1], p[3])


def p_new_statement(p):
    """
    new_statement : NEW qualified_identifier '(' argument_list ')'
    """

    # Even though the function's name has "statement" in it,
    # new is used as an expression

    p[0] = comp.NewStatement(p[2], p[4])
