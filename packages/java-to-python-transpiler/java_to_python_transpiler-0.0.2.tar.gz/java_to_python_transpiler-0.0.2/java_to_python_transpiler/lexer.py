"""
This module contains all the lexical and token rules for the java
to python transpiler
"""


from ply.lex import TOKEN
from java_to_python_transpiler.config import config_lexer


# 'literals' is a special keyword for ply, so the actual list is kept in config
literals = config_lexer.LITERALS_LIST

# Refer to the same reasoning for 'literals' as to why this is split up
tokens = config_lexer.TOKENS_LIST + list(config_lexer.RESERVED_KEYWORDS.values())

ID = config_lexer.IDENTIFIER_REGEX
DEC_LIT = config_lexer.DECIMAL_LITERAL_REGEX
FLOAT_LIT = config_lexer.FLOAT_LITERAL_REGEX
SINGLE_LINE_COMMENT = config_lexer.SINGLE_LINE_COMMENT_REGEX
MULTI_LINE_COMMENT = config_lexer.MULTI_LINE_COMMENT_REGEX

# Ignore spaces, tabs, returns, newlines, formfeed
t_ignore = config_lexer.PLY_IGNORED_CHARACTERS

t_CHAR_LIT = config_lexer.CHARACTER_LITERAL
t_STR_LIT = config_lexer.STRING_LITERAL
t_AND = config_lexer.AND_OPERATOR
t_OR = config_lexer.OR_OPERATOR
t_INC = config_lexer.INCREMENT_OPERATOR
t_DEC = config_lexer.DECREMENT_OPERATOR
t_MUL_INC = config_lexer.MULTIPLY_INCREMENT_OPERATOR
t_DIV_DEC = config_lexer.DIVIDE_DECREMENT_OPERATOR


@TOKEN(ID)
def t_ID(t):
    t.type = config_lexer.RESERVED_KEYWORDS.get(t.value, "ID")
    return t


# The order of functions matter
@TOKEN(FLOAT_LIT)
def t_FLOAT_LIT(t):
    return t


@TOKEN(DEC_LIT)
def t_DEC_LIT(t):
    return t


@TOKEN(SINGLE_LINE_COMMENT)
def t_SINGLE_LINE_COMMENT(t):
    # Removes the "//"
    t.value = t.value[2:]

    return t


@TOKEN(MULTI_LINE_COMMENT)
def t_MULTI_LINE_COMMENT(t):
    # Remove first 2 chars and last 2 chars
    t.value = t.value[2:]
    t.value = t.value[:-2]

    # Add the comment starters
    t.value = t.value.strip()
    t.value = t.value.replace("\n", "\n#")

    return t


# Temporary error handler. This will need to be elaborated upon
def t_error(t):
    print(f"Unknown Character {t.value}")
    t.lexer.skip(1)
