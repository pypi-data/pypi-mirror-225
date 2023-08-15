"""
Tests for the code_emitter module
"""


import unittest
from java_to_python_transpiler.util.code_emitter import CodeEmitter
from java_to_python_transpiler.core_transpiler.main_transpiler import Transpiler
from config import config_test_code_emitter


class TestCodeEmitter(unittest.TestCase):
    """
    Tests for the CodeEmitter class
    """

    EMPTY_STRING = config_test_code_emitter.EMPTY_STRING
    STRING_TO_ADD = config_test_code_emitter.STRING_TO_ADD
    NEWLINE = config_test_code_emitter.NEWLINE
    NEWLINE_AND_INDENT = config_test_code_emitter.NEWLINE_AND_INDENT

    def test_add_output(self):
        transpiler = Transpiler(None)
        code_emitter = CodeEmitter(transpiler)

        self.assertEqual(code_emitter.output, self.EMPTY_STRING)

        code_emitter.add_output(self.STRING_TO_ADD)
        self.assertEqual(code_emitter.output, self.STRING_TO_ADD)

    def test_add_newline(self):
        transpiler = Transpiler(None)
        code_emitter = CodeEmitter(transpiler)

        self.assertEqual(code_emitter.output, self.EMPTY_STRING)

        code_emitter.add_newline(increase_indent=True)
        self.assertEqual(code_emitter.output, self.NEWLINE_AND_INDENT)

        expected_output = self.NEWLINE_AND_INDENT + self.NEWLINE
        code_emitter.add_newline(decrease_indent=True)
        self.assertEqual(code_emitter.output, expected_output)


if __name__ == '__main__':
    unittest.main()
