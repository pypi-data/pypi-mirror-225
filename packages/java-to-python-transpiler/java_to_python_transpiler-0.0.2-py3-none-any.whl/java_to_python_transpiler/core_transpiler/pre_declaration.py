"""
This file covers everything that happens before a class
declaration such as imports
"""


from java_to_python_transpiler.util import language_elements as comp
from java_to_python_transpiler.util.code_emitter import CodeEmitter


def transpiler_package_statement(transpiler,
                                 current: comp.PackageStatement):
    """
    Package statements have a comment followed by the identifier
    of the package
    """
    
    out = CodeEmitter(transpiler)

    # adds this "# " before the identifier
    out.add_output(out.COMMENT_STARTER)
    out.add_output(out.SPACE)

    out.add_output(transpiler.traverse(current.qualified_identifier))

    # For spacing
    out.add_newline()

    return out.output


def transpiler_pre_class_declaration_list(
        transpiler, current: comp.PreClassDeclarationList):
    """
    Pre Class Declaration traverses like a standard list
    """

    out = CodeEmitter(transpiler)

    # The order of these two will likely need to be reversed
    # Yep, it did need to be reversed - Mar 21
    if current.additional_list is not None:
        out.add_output(transpiler.traverse(current.additional_list))

    if current.statement is not None:
        # Just in case for some reason there is nothing in
        # front of the class declaration
        out.add_output(transpiler.traverse(current.statement))
    
    return out.output


def transpiler_import_statement(transpiler, current: comp.ImportStatement):
    """
    Import statements translates (mostly) 1:1; however, the java
    standard library doesn't translate well

    The module: "Java.lang.Math" is just "math" in python
    """
    
    out = CodeEmitter(transpiler)

    # Add the keyword + identifier
    out.add_output(out.IMPORT_KW)
    out.add_output(out.SPACE)  # Spacing

    # Mess around with the identifier
    qualified_identifier = transpiler.traverse(current.qualified_identifier)
    out.add_output(qualified_identifier)

    # Get the last part of qualified identifier
    identifier_suffix = qualified_identifier.split(".")[-1]

    transpiler.variable_list.append(identifier_suffix)

    # Cap it off with a newline
    out.add_newline()

    return out.output
