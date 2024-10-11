import pytest
from lexer import Lexer
from parser import Parser

def run_parser_test(file_path):
    lexer = Lexer()
    lexer.build()
    parser = Parser(debug=False)

    file = open(file_path, 'r', encoding='utf-8')      
    data = file.read()

    lexer.input(data)
    parser.set_lexer(lexer)
    parser.parse(data)
    return parser.error_count, lexer.error_count


def test_valid_input():
    error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_valid_input.py")
    assert error_count_lexer == 0, "Lexer should not report errors for valid input."
    assert error_count_parser == 0, "Parser should not report errors for valid input."


def test_syntax_error():
    error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_syntax_error.py")
    assert error_count_lexer == 0, "Lexer should not report errors for syntax errors."
    assert error_count_parser > 0, "Parser should report syntax errors for invalid input."


def test_unexpected_eof():
    error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_unexpected_eof.py")
    assert error_count_lexer == 0, "Lexer should not report errors for unexpected EOF."
    assert error_count_parser > 0, "Parser should report an error for unexpected EOF."


def test_multiple_errors():
    error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_multiple_errors.py")
    assert error_count_lexer != 0, "Lexer should not report errors for multiple errors."
    assert error_count_parser >= 2, "Parser should report multiple errors."


def test_indentation_error():
    error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_indentation_error.py")
    assert error_count_lexer == 0, "Lexer should not report errors for indentation errors."
    assert error_count_parser > 0, "Parser should report an indentation error."


# def test_function_calls():
#     error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_function_calls.py")
#     assert error_count_lexer == 0, "Lexer should not report errors for valid function calls."
#     assert error_count_parser == 0, "Parser should not report errors for valid function calls."


def test_variable_assignments():
    error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_variable_assignments.py")
    assert error_count_lexer == 0, "Lexer should not report errors for valid variable assignments."
    assert error_count_parser == 0, "Parser should not report errors for valid variable assignments."


def test_math_operations():
    error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_math_operations.py")
    assert error_count_lexer == 0, "Lexer should not report errors for valid math operations."
    assert error_count_parser == 0, "Parser should not report errors for valid math operations."


# def test_conditional_statements():
#     error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_conditional_statements.py")
#     assert error_count_lexer == 0, "Lexer should not report errors for valid conditional statements."
#     assert error_count_parser == 0, "Parser should not report errors for valid conditional statements."


# def test_loops():
#     error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_loops.py")
#     assert error_count_lexer == 0, "Lexer should not report errors for valid loops."
#     assert error_count_parser == 0, "Parser should not report errors for valid loops."


# def test_complex_structure():
#     error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_complex_structure.py")
#     assert error_count_lexer == 0, "Lexer should not report errors for valid complex structures."
#     assert error_count_parser == 0, "Parser should not report errors for valid complex structures."


def test_unexpected_token_error():
    error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_unexpected_token_error.py")
    assert error_count_lexer != 0, "Lexer should not report errors for unexpected tokens."
    assert error_count_parser > 0, "Parser should detect unexpected tokens and report an error."


# def test_empty_file():
#     error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_empty_file.py")
#     assert error_count_lexer == 0, "Lexer should handle an empty file without errors."
#     assert error_count_parser == 0, "Parser should handle an empty file without errors."


def test_invalid_characters():
    error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_invalid_characters.py")
    assert error_count_lexer > 0, "Lexer should detect invalid characters and report an error."
    assert error_count_parser > 0, "Parser should detect invalid characters and report an error."


def test_code_with_comments():
    error_count_parser, error_count_lexer = run_parser_test("tests/parser_test_files/test_code_with_comments.py")
    assert error_count_lexer == 0, "Lexer should correctly ignore comments and not report errors."
    assert error_count_parser == 0, "Parser should correctly ignore comments and not report errors."
