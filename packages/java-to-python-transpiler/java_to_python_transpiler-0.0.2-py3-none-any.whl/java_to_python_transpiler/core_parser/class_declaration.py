"""
BNF for Class Declaration:
    class_declaration : class_modifier_list CLASS identifier extends_or_empty '{' class_body '}'

    class_modifier_list : class_modifier
                        | class_modifier_list class_modifier
    
    class_modifier : PUBLIC
                   | PRIVATE
                   | VOID
                   | STATIC
                   | variable_type

    extends_or_empty : EXTENDS qualified_identifier
                     | empty

    class_body : method_list_or_empty

    method_list_or_empty : method_list
                         | empty

    method_list : method_or_comment
                | method_list method_or_comment

    method_or_comment : field
                      | method
                      | comment

    field : class_modifier_list identifier '=' expression ';'

    method : class_modifier_list identifier '(' parameter_list_or_empty ')' '{' statement_list_or_empty '}'

    parameter_list_or_empty : parameter_list
                            | empty

    parameter_list : parameter_with_type
                   | parameter_with_type ',' parameter_list

    parameter_with_type : variable_type identifier

    statement_list_or_empty : statement_list
                            | empty

    statement_list : statement_with_semicolon_or_comment
                   | statement_list statement_with_semicolon_or_comment
"""


from java_to_python_transpiler.util import language_elements as comp


def p_class_declaration(p):
    """
    class_declaration : class_modifier_list CLASS identifier extends_or_empty '{' class_body '}'
    """

    # - Apr 9: I still have no clue
    # - Feb 21: I have no clue what the comment below me is referring to
    # - The reason class body isnt printed is becuz it has been worked
    # into the class declaration

    p[0] = comp.ClassDeclaration(
        identifier=p[3], inherited_class=p[4], class_body=p[6])


def p_class_modifier_list(p):
    """
    class_modifier_list : class_modifier
                        | class_modifier_list class_modifier
    """
    
    # Basic list of class modifiers
    # It doesn't matter which comes first in the second arity
    pass


def p_class_modifier(p):
    """
    class_modifier : PUBLIC
                   | PRIVATE
                   | VOID
                   | STATIC
                   | variable_type
    """

    # Class modifiers change a class but they aren't in Python so
    # They can kinda just be thrown away
    pass


def p_extends_or_empty(p):
    """
    extends_or_empty : EXTENDS qualified_identifier
                     | empty
    """

    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = None


def p_class_body(p):
    """
    class_body : method_list_or_empty
    """

    p[0] = comp.ClassBody(p[1])


def p_method_list_or_empty(p):
    """
    method_list_or_empty : method_list
                         | empty
    """

    if p[1] is None:
        p[0] = comp.MethodList()
    else:
        p[0] = p[1]


def p_method_list(p):
    """
    method_list : method_or_comment
                | method_list method_or_comment
    """

    if len(p) == 2:
        p[0] = comp.MethodList(p[1])
    elif len(p) == 3:
        p[0] = comp.MethodList(additional_list=p[1], method_or_comment=p[2])

    # If only comments in a method, pass keywword is needed
    # I don't have a clue what this does and I've tried to change it for
    # clarity but i dont think it does anything
    if not isinstance(p[0].method_or_comment, comp.Comment):

        # THIS WORKS BUT IT NEEDS TO BE CHANGED FOR CLARITY        
        p[0].method_or_comment.comments_only = False


def p_method_or_comment(p):
    """
    method_or_comment : field
                      | method
                      | comment
    """

    # Technically, this is not a statement but idc
    if isinstance(p[1], comp.Comment):
        p[1].is_statement = True

    p[0] = p[1]


def p_field(p):
    """
    field : class_modifier_list identifier '=' expression ';'
    """

    p[0] = comp.VariableInitialization(p[2], p[4])


def p_method(p):
    """
    method : class_modifier_list identifier '(' parameter_list_or_empty ')' '{' statement_list_or_empty '}'
    """

    p[0] = comp.Method(p[2], p[4], p[7])


def p_parameter_list_or_empty(p):
    """
    parameter_list_or_empty : parameter_list
                            | empty
    """

    if p[1] is None:
        p[0] = comp.ParameterList()
    else:
        p[0] = p[1]


def p_parameter_list(p):
    """
    parameter_list : parameter_with_type
                   | parameter_with_type ',' parameter_list
    """

    # This project gives me a headache
    if len(p) == 2:
        p[0] = comp.ParameterList(p[1])
    elif len(p) == 4:
        p[0] = comp.ParameterList(p[1], p[3])


def p_parameter_with_type(p):
    """
    parameter_with_type : variable_type identifier
    """

    p[0] = p[2]


def p_statement_list_or_empty(p):
    """
    statement_list_or_empty : statement_list
                            | empty
    """

    if p[1] is None:
        p[0] = comp.StatementList()
    else:
        p[0] = p[1]


def p_statement_list(p):
    """
    statement_list : statement_with_semicolon_or_comment
                   | statement_list statement_with_semicolon_or_comment
    """

    if len(p) == 2:
        p[0] = comp.StatementList(p[1])
    elif len(p) == 3:
        p[0] = comp.StatementList(
            additional_list=p[1], statement=p[2])
