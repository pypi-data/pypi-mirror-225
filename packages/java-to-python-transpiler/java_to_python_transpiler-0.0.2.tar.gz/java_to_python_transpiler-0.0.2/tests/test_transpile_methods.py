"""
Tests for the transpile_methods module
"""


import unittest
import java_to_python_transpiler.util.transpile_methods as transpile_methods
from java_to_python_transpiler.core_parser import main_parser
from java_to_python_transpiler import lexer
from config import config_test_transpile_methods


class TestTranspileMethods(unittest.TestCase):
    JAVA_FILE_PATH = config_test_transpile_methods.JAVA_FILE_PATH
    TRANSPILED_PYTHON_CODE = config_test_transpile_methods.TRANSPILED_PYTHON_CODE

    def test_transpile_java_file(self):
        python_code = transpile_methods.transpile_java_file(
            self.JAVA_FILE_PATH, lexer, main_parser)

        python_code_stripped = python_code.strip()
        self.assertEqual(python_code_stripped, self.TRANSPILED_PYTHON_CODE)

    def test_transpile_code(self):
        with open(self.JAVA_FILE_PATH, "r") as sample_java_file:
            java_code = sample_java_file.read()
            python_code = transpile_methods.transpile_code(java_code, lexer, main_parser)

            stripped_python_code = python_code.strip()
            self.assertEqual(stripped_python_code, self.TRANSPILED_PYTHON_CODE)


if __name__ == '__main__':
    unittest.main()
