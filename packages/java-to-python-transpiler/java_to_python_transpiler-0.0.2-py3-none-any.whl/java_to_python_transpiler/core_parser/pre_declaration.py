"""
BNF for Pre Declaration:
    package_statement_or_empty : package_statement
                               | empty

    package_statement : PACKAGE qualified_identifier ';'

    pre_class_declaration_list : pre_class_declaration
                               | pre_class_declaration_list pre_class_declaration

    pre_class_declaration : comment_list
                          | import_statement
                          | empty

    import_statement : IMPORT qualified_identifier ';'
"""


from java_to_python_transpiler.util import language_elements as comp


# Potentially add an __all__ variable


def p_package_statement_or_empty(p):
    """
    package_statement_or_empty : package_statement
                               | empty
    """

    p[0] = p[1]


def p_package_statement(p):
    """
    package_statement : PACKAGE qualified_identifier ';'
    """

    # This can turned into a throwaway if needed
    p[0] = comp.PackageStatement(p[2])


def p_pre_class_declaration_list(p):
    """
    pre_class_declaration_list : pre_class_declaration
                               | pre_class_declaration_list pre_class_declaration
    """

    if len(p) == 2:
        p[0] = comp.PreClassDeclarationList(p[1])
    elif len(p) == 3:
        # Ahh look the classic problem is appearing
        p[0] = comp.PreClassDeclarationList(
            statement=p[2], additional_list=p[1])


def p_pre_class_declaration(p):
    """
    pre_class_declaration : comment_list
                          | import_statement
                          | empty
    """

    p[0] = p[1]


def p_import_statement(p):
    """
    import_statement : IMPORT qualified_identifier ';'
    """

    p[0] = comp.ImportStatement(p[2])
