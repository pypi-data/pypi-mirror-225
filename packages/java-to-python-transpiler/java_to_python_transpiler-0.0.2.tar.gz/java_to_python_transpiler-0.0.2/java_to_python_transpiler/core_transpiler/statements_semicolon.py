"""
Covers things that are statements that don't need a semicolon
or "already have" a semi-colon like while loops or if statements
"""

from java_to_python_transpiler.util import language_elements as comp
from java_to_python_transpiler.util.code_emitter import CodeEmitter


def transpiler_statement(transpiler, current: comp.Statement):
    """
    Even though there are two statement files, the bnf fits better
    having statement here
    """
    
    out = CodeEmitter(transpiler)

    out.add_output(transpiler.traverse(current.statement_body))

    # After every statement, you need a newline; however, you
    # dont need one after return, but this adds one anyway
    out.add_newline()
    
    return out.output


def transpiler_if_statement(transpiler, current: comp.IfStatement):
    """
    If statements may cause problems with newlines
    Just know that this a potential problem ere
    """

    out = CodeEmitter(transpiler)

    # Traverse the if statement head
    out.add_output(out.IF_KW)
    out.add_output(out.SPACE)

    # Python does not require parenthesis around comp expr
    out.add_output(transpiler.traverse(current.comparison_expression))

    # Add the colon and a newline
    out.add_output(out.COLON)

    out.add_newline(increase_indent=True)

    # StatementList is never actually set to None, but its
    # most fundamental field is set to None when it is None
    # does that make sense?

    if current.statement_list_or_empty.statement is not None:
        out.add_output(transpiler.traverse(current.statement_list_or_empty))
    else:
        # If the statement body is empty, you'll need to pass
        out.add_output(out.PASS_KW)
    
    # This decrease ident might actually be unnecessary
    # but who knows
    out.add_newline(decrease_indent=True)
    
    # Check for else statement
    if current.else_statement_or_empty.statement is not None:
        
        # Head of the else statement
        out.add_output(out.ELSE_KW)
        out.add_output(out.COLON)
        out.add_newline(increase_indent=True)

        # Traverse the body and decrease ident
        out.add_output(transpiler.traverse(current.else_statement_or_empty))
        out.add_newline(decrease_indent=True)

    return out.output


def transpiler_comparison_expression(transpiler, current: comp.ComparisonExpression):
    """
    Comparison Expressions are fairly
    """
    
    out = CodeEmitter(transpiler)

    # if left expr is just true or false, no traverse necessary
    if isinstance(current.left_expression, str):
        out.add_output(current.left_expression)
    else:
        out.add_output(transpiler.traverse(current.left_expression))
    
    # If operator has a value, so does right expr; theyre linked
    if current.operator is not None:

        # Put some spacing
        out.add_output(out.SPACE)
        out.add_output(transpiler.traverse(current.operator))
        out.add_output(out.SPACE)
        
        out.add_output(transpiler.traverse(current.right_expression))

    return out.output


def transpiler_while_statement(transpiler, current: comp.WhileStatement):
    out = CodeEmitter(transpiler)

    # Head of the statement
    out.add_output(out.WHILE_KW)
    out.add_output(out.SPACE)
    out.add_output(transpiler.traverse(current.comparison_expression))
    out.add_output(out.COLON)

    # Increase the ident
    out.add_newline(increase_indent=True)
    
    # traverse the body of statement; if empty, pass it through
    if current.statement_list_or_empty.statement is not None:
        out.add_output(transpiler.traverse(current.statement_list_or_empty))
    else:
        out.add_output(out.PASS_KW)

    # Decrease identation
    out.add_newline(decrease_indent=True)

    return out.output


def transpiler_comparison_operator(transpiler, current):
    # I mean this is kind of unnecessary to have this here
    # but future-proofing!

    return current.value
