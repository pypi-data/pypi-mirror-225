"""
Configuration file for code_emitter
"""

# A standard ident tab space is 4 spaces
INDENT_SPACES = " " * 4

NEWLINE = "\n"

VARIABLE_TYPES_DICTIONARY = {
    "byte": "int",
    "Byte": "int",
    "short": "int",
    "Short": "int",
    "int": "int",
    "Integer": "int",
    "long": "int",
    "Long": "int",

    "float": "float",
    "Float": "float",
    "double": "float",
    "Double": "float",

    "char": "str",
    "Char": "str",
    "String": "str",

    "boolean": "bool",
    "Boolean": "bool"
}
