"""
This file covers things like method lists and parameters that happen
in classes
"""

from java_to_python_transpiler.util import language_elements as comp
from java_to_python_transpiler.util.code_emitter import CodeEmitter


def transpiler_class_declaration(transpiler, current: comp.ClassDeclaration):
    """
    Class declaration is complex
    """
    
    out = CodeEmitter(transpiler)

    # Does the file have a package statement?
    if current.package_statement is not None:
        out.add_output(transpiler.traverse(current.package_statement))

    # Check for stuff that happens before the class
    if current.pre_class_declaration_list is not None:
        out.add_output(transpiler.traverse(current.pre_class_declaration_list))

    # The "head" of the class is here.
    out.add_output(out.CLASS_KW, out.SPACE)

    # Class name
    out.add_output(transpiler.traverse(current.identifier))
    
    # Now inheritance
    out.add_output(out.OPEN_PAREN)

    # Is their an inherited class?
    if current.inherited_class is not None:
        out.add_output(transpiler.traverse(current.inherited_class))
    
    out.add_output(out.CLOSE_PAREN)

    out.add_output(out.COLON)

    # Next, go down a line and ident
    out.add_newline(increase_indent=True)

    # Finally, traverse the class_body
    out.add_output(transpiler.traverse(current.class_body))

    # Check if there are any comments after the class
    if current.comments_after is not None:

        # If comments after, dec ident + comments
        out.add_newline(decrease_indent=True)
        out.add_output(transpiler.traverse(current.comments_after))

    return out.output


def transpiler_class_body(transpiler, current: comp.ClassBody):
    """
    Regarding the pass keyword, relocated to MethodList
    """

    return transpiler.traverse(current.method_list)


def transpiler_method_list(transpiler, current: comp.MethodList):
    """
    Overall, method list gives me headaches

    I reordered StatementList and MethodList because it is
    giving me warnings and rejected rules (<empty> -> empty)
    But it works and stops bothering me
    """
    
    out = CodeEmitter(transpiler)

    # If there are not any methods, then the class is empty.
    # In Java, a class can be left as such because the brackets
    # indicate the start and end of a class; however, in Python,
    if current.method_or_comment is None:
        return out.PASS_KW

    # Check if there are additional methods
    if current.additional_list is not None:
        out.add_output(transpiler.traverse(current.additional_list))

    # For some reason Im traversing after additional methods?
    # I don't get it
    out.add_output(transpiler.traverse(current.method_or_comment))

    # Don't decrease ident after this because it will
    # cause problems
    # out.add_newline(dec_ident=True)

    return out.output


def transpiler_method(transpiler, current: comp.Method):
    """
    Method starts with def keyword, then parameters and finally
    the statement body
    """
    
    out = CodeEmitter(transpiler)

    # Start off the head of the method with a def keyword
    out.add_output(out.DEF_KW, out.SPACE)
    out.add_output(transpiler.traverse(current.identifier))
    
    # Add the parenthesis around the parameters
    out.add_output(out.OPEN_PAREN)

    if current.parameter_list is not None:
        out.add_output(transpiler.traverse(current.parameter_list))
    
    out.add_output(out.CLOSE_PAREN)

    # The colon rounds off the head of the method
    out.add_output(out.COLON)

    # Next, go down a line and ident
    out.add_newline(increase_indent=True)

    # Check if there are any statements in the method body
    if current.statement_list.statement is None:
        out.add_output(out.PASS_KW)
    else:
        # Else, just traverse the statements
        out.add_output(transpiler.traverse(current.statement_list))

    # If there are only comments in the method, append pass kw
    if current.comments_only and \
            current.statement_list.statement is not None:
        out.add_output(out.PASS_KW)

    # Once the method is done, go down a line and decrease
    out.add_newline(decrease_indent=True)

    return out.output


def transpiler_parameter_list(transpiler, current: comp.ParameterList):
    """
    Parameter list works different from argument list
    """
    
    out = CodeEmitter(transpiler)

    # Parameter works different from argument_list
    if current.identifier is not None:
        out.add_output(transpiler.traverse(current.identifier))

    # Check if there are additional parameters
    # (remember, additional_list works diff)
    if current.additional_list is not None:
        out.add_output(out.COMMA)
        out.add_output(out.SPACE)  # Prettier this way
        out.add_output(transpiler.traverse(current.additional_list))

    return out.output


def transpiler_statement_list(transpiler, current: comp.StatementList):
    """
    I reordered StatementList and MethodList because it is
    giving me warnings and rejected rules (<empty> -> empty)
    But it works and stops bothering me
    """

    out = CodeEmitter(transpiler)
    
    # Check if there are additional statements
    if current.additional_list is not None:
        out.add_output(transpiler.traverse(current.additional_list))

    out.add_output(transpiler.traverse(current.statement))

    return out.output
