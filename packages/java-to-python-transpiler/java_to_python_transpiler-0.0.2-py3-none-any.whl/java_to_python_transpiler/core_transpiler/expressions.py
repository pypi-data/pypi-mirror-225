"""
Self Explanatory
"""

from java_to_python_transpiler.util import language_elements as comp
from java_to_python_transpiler.util.code_emitter import CodeEmitter


def transpiler_expression(transpiler, current: comp.Expression):
    out = CodeEmitter(transpiler)
    
    if current.is_statement:
        # If the expression is a statement (standalone)
        out.add_output(transpiler.traverse(current.left_expression))

    elif current.with_parenthesis:
        # Put the expression between paranthesis
        out.add_output(out.OPEN_PAREN)
        out.add_output(transpiler.traverse(current.left_expression))
        out.add_output(out.CLOSE_PAREN)
    else:
        # Put an expression on either sides of an operator
        out.add_output(transpiler.traverse(current.left_expression))
        out.add_output(current.operator.value)
        out.add_output(transpiler.traverse(current.right_expression))

    return out.output


def transpiler_factor(transpiler, current: comp.Factor):
    # If it's a string, return as is
    if isinstance(current.value, str):
        return current.value

    return transpiler.traverse(current.value)


def transpiler_method_call(transpiler, current: comp.MethodCall):
    out = CodeEmitter(transpiler)

    out.add_output(transpiler.traverse(current.qualified_identifier))
    out.add_output(out.OPEN_PAREN)

    if current.argument_list.argument is not None:
        out.add_output(transpiler.traverse(current.argument_list))
    
    out.add_output(out.CLOSE_PAREN)

    return out.output


def transpiler_argument_list(transpiler, current: comp.ArgumentList):
    out = CodeEmitter(transpiler)

    out.add_output(transpiler.traverse(current.argument))

    # This one actually can be None
    if current.additional_list is not None:
        out.add_output(out.COMMA)
        out.add_output(out.SPACE)  # Pretty formatting
        out.add_output(transpiler.traverse(current.additional_list))
    
    return out.output


def transpiler_new_statement(transpiler, current: comp.NewStatement):
    out = CodeEmitter(transpiler)

    # Qualified Identifier is used instead of just Identifier
    # because Java's package system is excessive
    out.add_output(transpiler.traverse(current.qualified_identifier))

    out.add_output(out.OPEN_PAREN)

    # Are there any arguments?
    if current.argument_list.argument is not None:
        # Append them to the output
        out.add_output(transpiler.traverse(current.argument_list))

    out.add_output(out.CLOSE_PAREN)
    
    return out.output
