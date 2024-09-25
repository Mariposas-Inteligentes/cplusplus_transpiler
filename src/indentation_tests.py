import pytest
from lexer import Lexer
from common import IndentationError

@pytest.fixture
def lexer():
    lexer = Lexer()
    lexer.build()
    return lexer

def test_correct_indentation(lexer):
    code = '''
if True:
    print("Hello")
    if False:
        print("Nested")
    print("Back to outer")
'''
    lexer.input(code)
    token_types = [token.type for token in lexer.token_stream]

    expected = [
        'IF', 'TRUE', 'COLON', 'NEWLINE', 'INDENT', 'PRINT', 'OPEN_PARENTHESIS', 'STRING', 'CLOSED_PARENTHESIS', 'NEWLINE',
        'IF', 'FALSE', 'COLON', 'NEWLINE', 'INDENT', 'PRINT', 'OPEN_PARENTHESIS', 'STRING', 'CLOSED_PARENTHESIS', 'NEWLINE', 'DEDENT',
        'PRINT', 'OPEN_PARENTHESIS', 'STRING', 'CLOSED_PARENTHESIS', 'NEWLINE', 'DEDENT', 'ENDMARKER'
    ]

    assert token_types == expected



def test_incorrect_indentation(lexer):
    code = '''
if True:
print("Hello")
print("Incorrect indent")
'''
    lexer.input(code)
    assert len(lexer.token_stream) == 0


def test_expected_indentation(lexer):
    code = '''
def func():
    return True
'''
    lexer.input(code)
    token_types = [token.type for token in lexer.token_stream]

    expected = [
        'DEF', 'VAR_FUNC_NAME', 'OPEN_PARENTHESIS', 'CLOSED_PARENTHESIS', 'COLON', 'NEWLINE', 'INDENT', 'RETURN', 'TRUE', 'NEWLINE', 'DEDENT', 'ENDMARKER'
    ]

    assert token_types == expected


def test_unexpected_dedent(lexer):
    code = '''
if True:
    print("Hello")
print("Invalid dedent")
    print("Back to indent")
'''
    lexer.input(code)
    assert len(lexer.token_stream) == 0

def test_blank_line_handling(lexer):
    code = '''
if True:

    print("With blank line")
'''
    lexer.input(code)
    token_types = [token.type for token in lexer.token_stream]

    expected = [
        'IF', 'TRUE', 'COLON', 'NEWLINE', 'INDENT', 'PRINT', 'OPEN_PARENTHESIS', 'STRING', 'CLOSED_PARENTHESIS', 'NEWLINE', 'DEDENT', 'ENDMARKER'
    ]

    assert token_types == expected

def test_nested_indentation(lexer):
    code = '''
def outer():
    if True:
        print("Nested level 1")
        if False:
            print("Nested level 2")
'''
    lexer.input(code)
    token_types = [token.type for token in lexer.token_stream]

    expected = [
        'DEF', 'VAR_FUNC_NAME', 'OPEN_PARENTHESIS', 'CLOSED_PARENTHESIS', 'COLON', 'NEWLINE',
        'INDENT', 'IF', 'TRUE', 'COLON', 'NEWLINE',
        'INDENT', 'PRINT', 'OPEN_PARENTHESIS', 'STRING', 'CLOSED_PARENTHESIS', 'NEWLINE',
        'IF', 'FALSE', 'COLON', 'NEWLINE',
        'INDENT', 'PRINT', 'OPEN_PARENTHESIS', 'STRING', 'CLOSED_PARENTHESIS', 'NEWLINE',
        'DEDENT', 'DEDENT', 'DEDENT', 'ENDMARKER'
    ]


    assert token_types == expected
