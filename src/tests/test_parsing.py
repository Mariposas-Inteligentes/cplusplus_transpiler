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

# def test_variable_assignments(test_file_name):
#     variable_assign_code = """
# def my_function():
#     x = 10
#     y = "Hello"
#     z = True
#     """
#     create_test_file(test_file_name, variable_assign_code)

#     transpiler = Transpiler(test_file_name)
#     transpiler.input()

#     assert transpiler.parser.error_count == 0, "Parser should not report errors for valid variable assignments."

# def test_math_operations(test_file_name):
#     math_operations_code = """
# def my_function():
#     x = 10 + 5
#     y = 2 * (3 + 4)
#     z = 10 // 3
#     """
#     create_test_file(test_file_name, math_operations_code)

#     transpiler = Transpiler(test_file_name)
#     transpiler.input()

#     assert transpiler.parser.error_count == 0, "Parser should not report errors for valid math operations."

# def test_conditional_statements(test_file_name):
#     conditional_code = """
# def check_value(x):
#     if x > 10:
#         return "Greater"
#     elif x == 10:
#         return "Equal"
#     else:
#         return "Smaller"
#     """
#     create_test_file(test_file_name, conditional_code)

#     transpiler = Transpiler(test_file_name)
#     transpiler.input()

#     assert transpiler.parser.error_count == 0, "Parser should not report errors for valid conditional statements."

# def test_loops(test_file_name):
#     loop_code = """
# def loop_example():
#     for i in range(5):
#         print(i)
#     while i < 10:
#         i += 1
#     """
#     create_test_file(test_file_name, loop_code)

#     transpiler = Transpiler(test_file_name)
#     transpiler.input()

#     assert transpiler.parser.error_count == 0, "Parser should not report errors for valid loops."

# def test_nested_functions(test_file_name):
#     nested_function_code = """
# def outer_function():
#     def inner_function():
#         print("Inside inner")
#     inner_function()
#     """
#     create_test_file(test_file_name, nested_function_code)

#     transpiler = Transpiler(test_file_name)
#     transpiler.input()

#     assert transpiler.parser.error_count == 0, "Parser should not report errors for valid nested functions."

# def test_complex_structure(test_file_name):
#     complex_code = """
# def outer_function(x):
#     if x > 5:
#         for i in range(x):
#             def inner_function(y):
#                 if y < 3:
#                     return y * 2
#             print(inner_function(i))
#     """
#     create_test_file(test_file_name, complex_code)

#     transpiler = Transpiler(test_file_name)
#     transpiler.input()

#     assert transpiler.parser.error_count == 0, "Parser should not report errors for valid complex structures."

# def test_unexpected_token_error(test_file_name):
#     unexpected_token_code = """
# def test_unexpected():
#     print("This is correct.")
# @unexpected_symbol  # Unexpected token
#     """
#     create_test_file(test_file_name, unexpected_token_code)

#     transpiler = Transpiler(test_file_name)
#     transpiler.input()

#     assert transpiler.parser.error_count > 0, "Parser should detect unexpected tokens and report an error."

# def test_empty_file(test_file_name):
#     empty_code = ""  # Empty file
#     create_test_file(test_file_name, empty_code)

#     transpiler = Transpiler(test_file_name)
#     transpiler.input()

#     assert transpiler.parser.error_count == 0, "Parser should handle an empty file without errors."

# def test_invalid_characters(test_file_name):
#     invalid_code = """
# def test_invalid():
#     print("Hello!")
# $$InvalidCharacters##
#     """
#     create_test_file(test_file_name, invalid_code)

#     transpiler = Transpiler(test_file_name)
#     transpiler.input()

#     assert transpiler.parser.error_count > 0, "Parser should detect invalid characters and report an error."

# def test_code_with_comments(test_file_name):
#     comment_code = """
# def test_comments():
#     # This is a comment
#     x = 5  # This is another comment
#     print(x)
#     """
#     create_test_file(test_file_name, comment_code)

#     transpiler = Transpiler(test_file_name)
#     transpiler.input()

#     assert transpiler.parser.error_count == 0, "Parser should correctly ignore comments and not report errors."
