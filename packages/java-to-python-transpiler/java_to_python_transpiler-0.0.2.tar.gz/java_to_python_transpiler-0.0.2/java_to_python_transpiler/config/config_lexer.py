"""
Configuration file for the lexer
"""

RESERVED_KEYWORDS = {
    "true": "TRUE",
    "false": "FALSE",
    "null": "NULL",

    "public": "PUBLIC",
    "private": "PRIVATE",
    "void": "VOID",
    "static": "STATIC",

    "byte": "BYTE",
    "short": "SHORT",
    "char": "CHAR",
    "int": "INT",
    "long": "LONG",
    "float": "FLOAT",
    "double": "DOUBLE",
    "boolean": "BOOLEAN",

    "class": "CLASS",
    "return": "RETURN",
    "new": "NEW",
    "package": "PACKAGE",
    "import": "IMPORT",
    "extends": "EXTENDS",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
}

LITERALS_LIST = [
    "(", ")", "{", "}", "[", "]", ";", ".", ",", "=", "<", ">", "!", "~", "?",
    ":", "+", "-", "*", "/", "%"
]

TOKENS_LIST = ["ID", "DEC_LIT", "FLOAT_LIT", "CHAR_LIT", "STR_LIT", "AND", "OR",
               "INC", "DEC", "MUL_INC", "DIV_DEC", "SINGLE_LINE_COMMENT",
               "MULTI_LINE_COMMENT"]

IDENTIFIER_REGEX = r"[a-zA-Z_$][\da-zA-Z_]*"

# The reason why a number is called "decimal literal" refers to the number system
# Like Hex, Oct, Binary, etc.
DECIMAL_LITERAL_REGEX = r"([1-9]([_\d]*\d+)?|0)[lL]?"

FLOAT_LITERAL_REGEX = \
    r"(\d[_\d]*\d|\d)\.(\d[_\d]*\d|\d)?([eE][+-]?(\d[_\d]*\d|\d))?[fFdD]?"

SINGLE_LINE_COMMENT_REGEX = r"//.*"

MULTI_LINE_COMMENT_REGEX = r"/\*[\s\S]*?\*/"

PLY_IGNORED_CHARACTERS = " \t\r\n\f"

CHARACTER_LITERAL = r"'([^'\\]|\\[btnfr\"\'\\])'"

STRING_LITERAL = r"\"([^\"\\]|\\[btnfr\"\'\\])*\""

AND_OPERATOR = r"&&"

OR_OPERATOR = r"\|\|"

INCREMENT_OPERATOR = r"\+="

DECREMENT_OPERATOR = r"-="

MULTIPLY_INCREMENT_OPERATOR = r"\*="

DIVIDE_DECREMENT_OPERATOR = r"/="
