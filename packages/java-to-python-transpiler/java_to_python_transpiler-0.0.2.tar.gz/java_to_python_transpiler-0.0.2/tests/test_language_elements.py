"""
Tests Language Elements with methods; however, most language dataclasses
don't require tests
"""

import unittest
import java_to_python_transpiler.util.language_elements as elements
from config import config_test_language_elements


class TestIdentifier(unittest.TestCase):
    """
    Unit Test for the identifier __str__() dunder method
    """

    IDENTIFIER_STRING = \
        config_test_language_elements.IDENTIFIER_STRING_TEST_IDENTIFIER

    def test_identifier_str_method(self):
        identifier = elements.Identifier(self.IDENTIFIER_STRING)
        identifier_as_string = str(identifier)

        self.assertEqual(identifier_as_string, self.IDENTIFIER_STRING)


class TestQualifiedIdentifier(unittest.TestCase):
    """
    Unit Test for the qualified identifier dunder methods:
    __str__() and __repr__()
    """

    IDENTIFIER_STRING = config_test_language_elements.\
        IDENTIFIER_STRING_TEST_QUALIFIED_IDENTIFIER

    COMBINED_IDENTIFIER_STRING = IDENTIFIER_STRING + "." + IDENTIFIER_STRING

    def test_single_qualified_identifier_str_method(self):
        identifier = elements.Identifier(self.IDENTIFIER_STRING)

        qualified_identifier = elements.QualifiedIdentifier(identifier)
        qualified_identifier_as_string = str(qualified_identifier)

        self.assertEqual(qualified_identifier_as_string, self.IDENTIFIER_STRING)

    def test_chained_qualified_identifier_str_method(self):
        identifier = elements.Identifier(self.IDENTIFIER_STRING)
        secondary_identifier = elements.QualifiedIdentifier(identifier)

        qualified_identifier = elements.QualifiedIdentifier(identifier,
                                                            secondary_identifier)
        qualified_identifier_as_string = str(qualified_identifier)

        self.assertEqual(qualified_identifier_as_string,
                         self.COMBINED_IDENTIFIER_STRING)

    def test_repr_method(self):
        identifier = elements.Identifier(self.IDENTIFIER_STRING)

        qualified_identifier = elements.QualifiedIdentifier(identifier)
        qualified_identifier_as_string = repr(qualified_identifier)

        self.assertEqual(qualified_identifier_as_string, self.IDENTIFIER_STRING)


if __name__ == '__main__':
    unittest.main()
