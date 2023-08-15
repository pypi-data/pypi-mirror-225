"""
The code_emitter module contains a singular class by the same name. This class
is responsible for constructing statements and expressions inside the
transpiler.
"""


from java_to_python_transpiler.config import config_code_emitter


class CodeEmitter(object):
    """
    This class is responsible for constructing statements and expressions
    inside the transpiler.

    This class's constructor takes in a singular argument, "transpiler" of the
    Transpiler class found in the transpiler module.

    This class contains a number of constants that are used to construct
    outputs.
    """

    INDENT_SPACES = config_code_emitter.INDENT_SPACES
    NEWLINE = config_code_emitter.NEWLINE
    
    VARIABLE_TYPES = config_code_emitter.VARIABLE_TYPES_DICTIONARY

    CLASS_KW = "class"
    PASS_KW = "pass"
    DEF_KW = "def"
    RETURN_KW = "return"
    IMPORT_KW = "import"
    IF_KW = "if"
    ELSE_KW = "else"
    WHILE_KW = "while"

    SPACE, COMMA = " ", ","
    PERIOD, COLON = ".", ":"

    OPEN_PAREN, CLOSE_PAREN = "(", ")"
    EQUALS_SIGN = "="
    COMMENT_STARTER = "#"
    PLUS_SIGN = "+"

    PRINT_FUNC_PY = "print"

    PRINTLN_FUNC_JAVA = "System.out.println"
    PRINT_FUNC_JAVA = "System.out.print"

    MATH_IMPORT_JAVA = "java.lang.Math"
    MATH_IMPORT_PY = "math"

    JAVA_IDENTIFIERS = {
        PRINTLN_FUNC_JAVA: PRINT_FUNC_PY,
        PRINT_FUNC_JAVA: PRINT_FUNC_PY,
        MATH_IMPORT_JAVA: MATH_IMPORT_PY,
    }

    def __init__(self, transpiler):
        self.transpiler = transpiler
        self.output = ""

    def add_output(self, string, delimiter=""):
        """
        This method takes in "string" of type str, and an optional parameter
        "delimiter" of type str that defaults to any string.
        """

        self.output += string + delimiter

    def add_newline(self, increase_indent=False, decrease_indent=False):
        """
        This method takes in two optionals boolean parameters: inc_ident and
        dec_ident. Both of these parameters default to False.
        """

        if increase_indent:
            self.transpiler.indent_level += 1
        
        if decrease_indent:
            self.transpiler.indent_level -= 1

        calculated_indentation = self.INDENT_SPACES * self.transpiler.indent_level
        self.output += self.NEWLINE + calculated_indentation
