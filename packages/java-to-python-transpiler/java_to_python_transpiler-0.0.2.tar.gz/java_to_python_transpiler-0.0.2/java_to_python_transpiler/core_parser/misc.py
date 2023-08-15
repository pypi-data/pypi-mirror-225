"""
MISC (order of these really doesn't matter):
    comment_list : comment
                 | comment comment_list

    comment : SINGLE_LINE_COMMENT
            | multi_line_comment

    multi_line_comment : MULTI_LINE_COMMENT

    variable_type : identifier
                  | BYTE
                  | SHORT
                  | CHAR
                  | INT
                  | LONG
                  | FLOAT
                  | DOUBLE
                  | BOOLEAN
                  | array_type

    identifier : ID

    array_type : variable_type '[' ']'

    qualified_identifier : identifier
                         | identifier '.' qualified_identifier

    empty :

    comment_list_or_empty : comment_list
                          | empty
"""


from java_to_python_transpiler.util import language_elements as comp


def p_comment_list(p):
    """
    comment_list : comment
                 | comment comment_list
    """

    if len(p) == 2:
        p[0] = comp.CommentList(p[1])
    elif len(p) == 3:
        p[0] = comp.CommentList(p[1], p[2])


def p_comment(p):
    """
    comment : SINGLE_LINE_COMMENT
            | multi_line_comment
    """

    # The comment below (about comments) is incorrect
    # A comment list is unnecessary because comment can be used in place
    # of method_list

    p[0] = comp.Comment(p[1])


def p_multi_line_comment(p):
    """
    multi_line_comment : MULTI_LINE_COMMENT
    """

    # Once you make a comment list, replace this with a commentlist
    # But, for now, this will just pass on the terminal instead
    # Because a commenet is created in the p_comment function
    p[0] = p[1]


def p_variable_type(p):
    """
    variable_type : identifier
                  | BYTE
                  | SHORT
                  | CHAR
                  | INT
                  | LONG
                  | FLOAT
                  | DOUBLE
                  | BOOLEAN
                  | array_type
    """

    # This is used in variable declaration
    p[0] = comp.VariableType(p[1])


def p_identifier(p):
    """
    identifier : ID
    """

    p[0] = comp.Identifier(p[1])


def p_array_type(p):
    """
    array_type : variable_type '[' ']'
    """

    p[0] = p[1]


def p_qualified_identifier(p):
    """
    qualified_identifier : identifier
                         | identifier '.' qualified_identifier
    """

    if len(p) == 2:
        p[0] = comp.QualifiedIdentifier(p[1])
    elif len(p) == 4:
        p[0] = comp.QualifiedIdentifier(p[1], p[3])


def p_empty(p):
    """
    empty :
    """

    p[0] = None


def p_comment_list_or_empty(p):
    """
    comment_list_or_empty : comment_list
                          | empty
    """

    p[0] = p[1]
