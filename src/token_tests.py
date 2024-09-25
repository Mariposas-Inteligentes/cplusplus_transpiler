import pytest
from lexer import Lexer

@pytest.fixture
def lexer():
    lexer = Lexer()
    lexer.build()
    return lexer

def test_correct_basic_code(lexer):
    code = '''
# Approximation of pi using Gregory-Leibniz series
def approximate_pi(n_terms):
    pi_approx = 0
    for n in range(n_terms):
        term = (-1)**n / (2 * n + 1)
        pi_approx += term
    pi_approx *= 4
    return pi_approx  # Result

n_terms = 4
pi_value = approximate_pi(n_terms)
print("Approximation of pi = " + str(pi_value))
'''
    lexer.input(code)
    token_types = [token.type for token in lexer.token_stream]

    expected = ['DEF', 'VAR_FUNC_NAME', 'OPEN_PARENTHESIS', 'VAR_FUNC_NAME', 'CLOSED_PARENTHESIS', 
    'COLON', 'NEWLINE', 'INDENT', 'VAR_FUNC_NAME', 'ASSIGN', 'INT', 'NEWLINE', 'FOR', 'VAR_FUNC_NAME', 
    'VAR_FUNC_NAME', 'VAR_FUNC_NAME', 'OPEN_PARENTHESIS', 'VAR_FUNC_NAME', 'CLOSED_PARENTHESIS', 
    'COLON', 'NEWLINE', 'INDENT', 'VAR_FUNC_NAME', 'ASSIGN', 'OPEN_PARENTHESIS', 'MINUS', 'INT', 
    'CLOSED_PARENTHESIS', 'POWER', 'VAR_FUNC_NAME', 'DIV', 'OPEN_PARENTHESIS', 'INT', 'MUL', 
    'VAR_FUNC_NAME', 'PLUS', 'INT', 'CLOSED_PARENTHESIS', 'NEWLINE', 'VAR_FUNC_NAME', 'PLUS_EQUALS', 
    'VAR_FUNC_NAME', 'NEWLINE', 'DEDENT', 'VAR_FUNC_NAME', 'MUL_EQUALS', 'INT', 'NEWLINE', 'RETURN', 
    'VAR_FUNC_NAME', 'NEWLINE', 'DEDENT', 'VAR_FUNC_NAME', 'ASSIGN', 'INT', 'NEWLINE', 'VAR_FUNC_NAME', 
    'ASSIGN', 'VAR_FUNC_NAME', 'OPEN_PARENTHESIS', 'VAR_FUNC_NAME', 'CLOSED_PARENTHESIS', 'NEWLINE', 'PRINT', 
    'OPEN_PARENTHESIS', 'STRING', 'PLUS', 'VAR_FUNC_NAME', 'OPEN_PARENTHESIS', 'VAR_FUNC_NAME', 'CLOSED_PARENTHESIS', 
    'CLOSED_PARENTHESIS', 'NEWLINE', 'ENDMARKER']

    assert token_types == expected