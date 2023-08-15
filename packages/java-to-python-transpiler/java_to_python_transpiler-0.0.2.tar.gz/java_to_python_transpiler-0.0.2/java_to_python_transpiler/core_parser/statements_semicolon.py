"""
Statements w/ Semicolon (or those that don't need one) BNF:
    statement_with_semicolon_or_comment : statement_without_semicolon ';'
                                        | if_statement
                                        | while_statement
                                        | comment_statement

    if_statement : IF '(' comparison_expression ')' '{' statement_list_or_empty '}' else_statement_or_empty

    comparison_expression : comparison_expression '=' '=' comparison_expression
                          | comparison_expression '!' '=' comparison_expression
                          | comparison_expression '>' '=' comparison_expression
                          | comparison_expression '<' '=' comparison_expression
                          | comparison_expression '<' comparison_expression
                          | comparison_expression '>' comparison_expression
                          | TRUE
                          | FALSE

    else_statement_or_empty : ELSE '{' statement_list_or_empty '}'
                            | empty

    while_statement : WHILE '(' comparison_expression ')' '{' statement_list_or_empty '}'

    comment_statement : comment
"""


from java_to_python_transpiler.util import language_elements as comp


def p_statement_with_semicolon_or_comment(p):
    """
    statement_with_semicolon_or_comment : statement_without_semicolon ';'
                                        | if_statement
                                        | while_statement
                                        | comment_statement
    """
    p[0] = comp.Statement(p[1])


def p_if_statement(p):
    """
    if_statement : IF '(' comparison_expression ')' '{' statement_list_or_empty '}' else_statement_or_empty
    """

    p[0] = comp.IfStatement(p[3], p[6], p[8])


def p_comparison_expression(p):
    """
    comparison_expression : comparison_expression '=' '=' comparison_expression
                          | comparison_expression '!' '=' comparison_expression
                          | comparison_expression '>' '=' comparison_expression
                          | comparison_expression '<' '=' comparison_expression
                          | comparison_expression '<' comparison_expression
                          | comparison_expression '>' comparison_expression
                          | TRUE
                          | FALSE
    """

    # T OR F
    if len(p) == 2:
        p[0] = comp.ComparisonExpression(p[1].capitalize())

    # GT OR LT
    elif len(p) == 4:
        if p[2] == ">":
            operator = comp.ComparisonOperator.GT
        elif p[2] == "<":
            operator = comp.ComparisonOperator.LT

        p[0] = comp.ComparisonExpression(p[1], operator, p[3])

    # GT_EQ, LT_EQ, BQ_EQ, NT_EQ
    elif len(p) == 5:
        if p[2] == "=":
            operator = comp.ComparisonOperator.BOOL_EQ
        elif p[2] == "!":
            operator = comp.ComparisonOperator.NOT_EQ
        elif p[2] == ">":
            operator = comp.ComparisonOperator.GT_OR_EQ
        elif p[2] == "<":
            operator = comp.ComparisonOperator.LT_OR_EQ

        p[0] = comp.ComparisonExpression(p[1], operator, p[4])


def p_else_statement_or_empty(p):
    """
    else_statement_or_empty : ELSE '{' statement_list_or_empty '}'
                            | empty
    """

    # If it is an else statement
    if len(p) > 2:
        p[0] = p[3]
    else:
        # Otherwise make an empty statement list to pass thru
        p[0] = comp.StatementList()


def p_while_statement(p):
    """
    while_statement : WHILE '(' comparison_expression ')' '{' statement_list_or_empty '}'
    """

    p[0] = comp.WhileStatement(p[3], p[6])


def p_comment_statement(p):
    """
    comment_statement : comment
    """

    # Make sure that the transpiler knows that comment is a statement
    # so that it puts a newline

    p[1].is_statement = True
    p[0] = p[1]
