import os
import pytest
from transpiler import Transpiler

@pytest.fixture


def test_valid_input():
    transpiler = Transpiler("tests/parser_test_files/test_valid_input.py")
    transpiler.input()
    assert transpiler.lexer.error_count == 0, "Lexer should not report errors for valid input."
    assert transpiler.parser.error_count == 0, "Parser should not report errors for valid input."

def test_syntax_error():
    transpiler = Transpiler("tests/parser_test_files/test_syntax_error.py")
    transpiler.input()
    assert transpiler.parser.error_count > 0, "Parser should report syntax errors for invalid input."

def test_unexpected_eof():
    transpiler = Transpiler("tests/parser_test_files/test_unexpected_eof.py")
    transpiler.input()
    assert transpiler.parser.error_count > 0, "Parser should report an error for unexpected EOF."

def test_multiple_errors():
    transpiler = Transpiler("tests/parser_test_files/test_multiple_errors.py")
    transpiler.input()
    assert transpiler.parser.error_count >= 2, "Parser should report multiple errors."

def test_indentation_error():
    transpiler = Transpiler("tests/parser_test_files/test_indentation_error.py")
    transpiler.input()
    assert transpiler.parser.error_count > 0, "Parser should report an indentation error."

def test_function_calls():
    transpiler = Transpiler("tests/parser_test_files/test_function_calls.py")
    transpiler.input()
    assert transpiler.parser.error_count == 0, "Parser should not report errors for valid function calls."

def test_variable_assignments():
    transpiler = Transpiler("tests/parser_test_files/test_variable_assignments.py")
    transpiler.input()
    assert transpiler.parser.error_count == 0, "Parser should not report errors for valid variable assignments."

def test_math_operations():
    transpiler = Transpiler("tests/parser_test_files/test_math_operations.py")
    transpiler.input()
    assert transpiler.parser.error_count == 0, "Parser should not report errors for valid math operations."

def test_conditional_statements():
    transpiler = Transpiler("tests/parser_test_files/test_conditional_statements.py")
    transpiler.input()
    assert transpiler.parser.error_count == 0, "Parser should not report errors for valid conditional statements."

def test_loops():
    transpiler = Transpiler("tests/parser_test_files/test_loops.py")
    transpiler.input()
    assert transpiler.parser.error_count == 0, "Parser should not report errors for valid loops."

def test_nested_functions():
    transpiler = Transpiler("tests/parser_test_files/test_nested_functions.py")
    transpiler.input()
    assert transpiler.parser.error_count == 0, "Parser should not report errors for valid nested functions."

def test_complex_structure():
    transpiler = Transpiler("tests/parser_test_files/test_complex_structure")
    transpiler.input()
    assert transpiler.parser.error_count == 0, "Parser should not report errors for valid complex structures."

def test_unexpected_token_error():
    transpiler = Transpiler("tests/parser_test_files/test_unexpected_token_error.py")
    transpiler.input()
    assert transpiler.parser.error_count > 0, "Parser should detect unexpected tokens and report an error."

def test_empty_file():
    transpiler = Transpiler("tests/parser_test_files/test_empty_file.py")
    transpiler.input()
    assert transpiler.parser.error_count == 0, "Parser should handle an empty file without errors."

def test_invalid_characters():
    transpiler = Transpiler("tests/parser_test_files/test_invalid_characters.py")
    transpiler.input()
    assert transpiler.parser.error_count > 0, "Parser should detect invalid characters and report an error."

def test_code_with_comments():
    transpiler = Transpiler("tests/parser_test_files/test_code_with_comments.py")
    transpiler.input()
    assert transpiler.parser.error_count == 0, "Parser should correctly ignore comments and not report errors."
