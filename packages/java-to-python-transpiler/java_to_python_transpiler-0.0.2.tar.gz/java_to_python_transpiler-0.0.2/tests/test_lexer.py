"""
This module contains tests for the lexical analysis part of the transpiler
"""

import unittest
import re
from java_to_python_transpiler import lexer
from config import config_test_lexer


class TestComplexRegularExpressions(unittest.TestCase):
    """
    Tests specifically for the more complex regular expressions
    """

    ID_VALID_INPUTS = config_test_lexer.IDENTIFIER_VALID_INPUTS
    ID_INVALID_INPUTS = config_test_lexer.IDENTIFIER_INVALID_INPUTS

    DEC_LIT_VALID_INPUTS = config_test_lexer.DECIMAL_LITERAL_VALID_INPUTS
    DEC_LIT_INVALID_INPUTS = config_test_lexer.DECIMAL_LITERAL_INVALID_INPUTS

    FLOAT_LIT_VALID_INPUTS = config_test_lexer.FLOAT_LITERAL_VALID_INPUTS
    FLOAT_LIT_INVALID_INPUTS = config_test_lexer.FLOAT_LITERAL_INVALID_INPUTS

    SINGLE_LINE_COMMENT_VALID_INPUTS = \
        config_test_lexer.SINGLE_LINE_COMMENT_VALID_INPUTS
    SINGLE_LINE_COMMENT_INVALID_INPUTS = \
        config_test_lexer.SINGLE_LINE_COMMENT_INVALID_INPUTS

    MULTI_LINE_COMMENT_VALID_INPUTS = \
        config_test_lexer.MULTI_LINE_COMMENT_VALID_INPUTS
    MULTI_LINE_COMMENT_INVALID_INPUTS = \
        config_test_lexer.MULTI_LINE_COMMENT_INVALID_INPUTS

    CHAR_LIT_VALID_INPUTS = config_test_lexer.CHARACTER_LITERAL_VALID_INPUTS
    CHAR_LIT_INVALID_INPUTS = config_test_lexer.CHARACTER_LITERAL_INVALID_INPUTS

    STR_LIT_VALID_INPUTS = config_test_lexer.STRING_LITERAL_VALID_INPUTS
    STR_LIT_INVALID_INPUTS = config_test_lexer.STRING_LITERAL_INVALID_INPUTS

    def test_ID(self):
        for input_string in self.ID_VALID_INPUTS:
            with self.subTest(input_str=input_string):
                self.assertRegex(input_string, lexer.ID)

        for input_string in self.ID_INVALID_INPUTS:
            with self.subTest(input_str=input_string):
                full_match = re.fullmatch(lexer.ID, input_string)
                self.assertIsNone(full_match)

    def test_DEC_LIT(self):
        for input_string in self.DEC_LIT_VALID_INPUTS:
            with self.subTest(input_str=input_string):
                self.assertRegex(input_string, lexer.DEC_LIT)

        for input_string in self.DEC_LIT_INVALID_INPUTS:
            with self.subTest(input_str=input_string):
                full_match = re.fullmatch(lexer.DEC_LIT, input_string)
                self.assertIsNone(full_match)

    def test_FLOAT_LIT(self):
        for input_string in self.FLOAT_LIT_VALID_INPUTS:
            with self.subTest(input_str=input_string):
                self.assertRegex(input_string, lexer.FLOAT_LIT)

        for input_string in self.FLOAT_LIT_INVALID_INPUTS:
            with self.subTest(input_str=input_string):
                full_match = re.fullmatch(lexer.FLOAT_LIT, input_string)
                self.assertIsNone(full_match)

    def test_SINGLE_LINE_COMMENT(self):
        for input_string in self.SINGLE_LINE_COMMENT_VALID_INPUTS:
            with self.subTest(input_str=input_string):
                self.assertRegex(input_string, lexer.SINGLE_LINE_COMMENT)

        for input_string in self.SINGLE_LINE_COMMENT_INVALID_INPUTS:
            with self.subTest(input_str=input_string):
                full_match = re.fullmatch(lexer.SINGLE_LINE_COMMENT, input_string)
                self.assertIsNone(full_match)

    def test_MULTI_LINE_COMMENT(self):
        for input_string in self.MULTI_LINE_COMMENT_VALID_INPUTS:
            with self.subTest(input_str=input_string):
                self.assertRegex(input_string, lexer.MULTI_LINE_COMMENT)

        for input_string in self.MULTI_LINE_COMMENT_INVALID_INPUTS:
            with self.subTest(input_str=input_string):
                full_match = re.fullmatch(lexer.MULTI_LINE_COMMENT, input_string)
                self.assertIsNone(full_match)

    def test_CHAR_LIT(self):
        for input_string in self.CHAR_LIT_VALID_INPUTS:
            with self.subTest(input_str=input_string):
                self.assertRegex(input_string, lexer.t_CHAR_LIT)

        for input_string in self.CHAR_LIT_INVALID_INPUTS:
            with self.subTest(input_str=input_string):
                full_match = re.fullmatch(lexer.t_CHAR_LIT, input_string)
                self.assertIsNone(full_match)

    def test_STR_LIT(self):
        for input_string in self.STR_LIT_VALID_INPUTS:
            with self.subTest(input_str=input_string):
                self.assertRegex(input_string, lexer.t_STR_LIT)

        for input_string in self.STR_LIT_INVALID_INPUTS:
            with self.subTest(input_str=input_string):
                full_match = re.fullmatch(lexer.t_STR_LIT, input_string)
                self.assertIsNone(full_match)


if __name__ == '__main__':
    unittest.main()
