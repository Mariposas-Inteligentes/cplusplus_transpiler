import pytest
from context import lexer
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


def test_correct_class_and_try_code(lexer):
    code = '''
class Triangle:
    def __init__(self, side_a, side_b, side_c):
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c
        self.triangle_type = None
        self.invalid = False
    def classify_triangle(self):
        if not(self.side_a >= 0 and self.side_b >= 0 and self.side_c >= 0):
            raise ValueError("Sides must be greater than zero.")
        if (self.side_a + self.side_b <= self.side_c or
            self.side_a + self.side_c <= self.side_b or
            self.side_b + self.side_c <= self.side_a):
            self.invalid = True
            self.triangle_type = "Not a triangle"
        elif self.side_a == self.side_b and self.side_b == self.side_c:
            self.triangle_type = "Equilateral"
        elif (self.side_a == self.side_b or 
              self.side_b == self.side_c or 
              self.side_a == self.side_c):
            self.triangle_type = "Isosceles"
        else:
            self.triangle_type = "Scalene"
        return self.triangle_type
try:
    sides = [3, 4, 5]
    results = {'Scalene': 0, 'Equilateral': 0, 'Isosceles': 0}
    while(True):
        triangle = Triangle(sides[0], sides[1], sides[2])
        result = triangle.classify_triangle()
        if (result != "Not a triangle"):
            results[result] += 1
            if results[result] > 2:
                break
        sides[0] += 1
        sides[1] += 1
        sides[2] += 1
except ValueError as e:
    print("Error:", e)
'''
    lexer.input(code)
    token_types = [token.type for token in lexer.token_stream]

    expected = ['CLASS', 'VAR_FUNC_NAME', 'COLON', 'NEWLINE', 'INDENT', 'DEF', 'VAR_FUNC_NAME', 
    'OPEN_PARENTHESIS', 'VAR_FUNC_NAME', 'COMMA', 'VAR_FUNC_NAME', 'COMMA', 'VAR_FUNC_NAME', 'COMMA', 
    'VAR_FUNC_NAME', 'CLOSED_PARENTHESIS', 'COLON', 'NEWLINE', 'INDENT', 'VAR_FUNC_NAME', 'PERIOD', 
    'VAR_FUNC_NAME', 'ASSIGN', 'VAR_FUNC_NAME', 'NEWLINE', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 
    'ASSIGN', 'VAR_FUNC_NAME', 'NEWLINE', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'ASSIGN', 
    'VAR_FUNC_NAME', 'NEWLINE', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'ASSIGN', 'NONE', 'NEWLINE', 
    'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'ASSIGN', 'FALSE', 'NEWLINE', 'DEDENT', 'DEF', 
    'VAR_FUNC_NAME', 'OPEN_PARENTHESIS', 'VAR_FUNC_NAME', 'CLOSED_PARENTHESIS', 'COLON', 'NEWLINE', 
    'INDENT', 'IF', 'NOT', 'OPEN_PARENTHESIS', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'MORE_EQUALS', 
    'INT', 'AND', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'MORE_EQUALS', 'INT', 'AND', 'VAR_FUNC_NAME', 
    'PERIOD', 'VAR_FUNC_NAME', 'MORE_EQUALS', 'INT', 'CLOSED_PARENTHESIS', 'COLON', 'NEWLINE', 'INDENT', 
    'VAR_FUNC_NAME', 'VAR_FUNC_NAME', 'OPEN_PARENTHESIS', 'STRING', 'CLOSED_PARENTHESIS', 'NEWLINE', 
    'DEDENT', 'IF', 'OPEN_PARENTHESIS', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'PLUS', 
    'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'LESS_EQUALS', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 
    'OR', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'PLUS', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 
    'LESS_EQUALS', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'OR', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 
    'PLUS', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'LESS_EQUALS', 'VAR_FUNC_NAME', 'PERIOD', 
    'VAR_FUNC_NAME', 'CLOSED_PARENTHESIS', 'COLON', 'NEWLINE', 'INDENT', 'VAR_FUNC_NAME', 'PERIOD', 
    'VAR_FUNC_NAME', 'ASSIGN', 'TRUE', 'NEWLINE', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'ASSIGN', 'STRING', 
    'NEWLINE', 'DEDENT', 'ELIF', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'EQUALS', 'VAR_FUNC_NAME', 'PERIOD', 
    'VAR_FUNC_NAME', 'AND', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'EQUALS', 'VAR_FUNC_NAME', 'PERIOD', 
    'VAR_FUNC_NAME', 'COLON', 'NEWLINE', 'INDENT', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'ASSIGN', 'STRING', 
    'NEWLINE', 'DEDENT', 'ELIF', 'OPEN_PARENTHESIS', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'EQUALS', 
    'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'OR', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'EQUALS', 
    'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'OR', 'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'EQUALS', 
    'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'CLOSED_PARENTHESIS', 'COLON', 'NEWLINE', 'INDENT', 'VAR_FUNC_NAME', 
    'PERIOD', 'VAR_FUNC_NAME', 'ASSIGN', 'STRING', 'NEWLINE', 'DEDENT', 'ELSE', 'COLON', 'NEWLINE', 'INDENT', 
    'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'ASSIGN', 'STRING', 'NEWLINE', 'DEDENT', 'RETURN', 'VAR_FUNC_NAME', 
    'PERIOD', 'VAR_FUNC_NAME', 'NEWLINE', 'DEDENT', 'DEDENT', 'TRY', 'COLON', 'NEWLINE', 'INDENT', 'VAR_FUNC_NAME', 
    'ASSIGN', 'OPEN_BRACKET', 'INT', 'COMMA', 'INT', 'COMMA', 'INT', 'CLOSED_BRACKET', 'NEWLINE', 'VAR_FUNC_NAME', 
    'ASSIGN', 'OPEN_CURLY_BRACKET', 'STRING', 'COLON', 'INT', 'COMMA', 'STRING', 'COLON', 'INT', 'COMMA', 'STRING', 
    'COLON', 'INT', 'CLOSED_CURLY_BRACKET', 'NEWLINE', 'WHILE', 'OPEN_PARENTHESIS', 'TRUE', 'CLOSED_PARENTHESIS', 
    'COLON', 'NEWLINE', 'INDENT', 'VAR_FUNC_NAME', 'ASSIGN', 'VAR_FUNC_NAME', 'OPEN_PARENTHESIS', 'VAR_FUNC_NAME', 
    'OPEN_BRACKET', 'INT', 'CLOSED_BRACKET', 'COMMA', 'VAR_FUNC_NAME', 'OPEN_BRACKET', 'INT', 'CLOSED_BRACKET', 'COMMA', 
    'VAR_FUNC_NAME', 'OPEN_BRACKET', 'INT', 'CLOSED_BRACKET', 'CLOSED_PARENTHESIS', 'NEWLINE', 'VAR_FUNC_NAME', 'ASSIGN', 
    'VAR_FUNC_NAME', 'PERIOD', 'VAR_FUNC_NAME', 'OPEN_PARENTHESIS', 'CLOSED_PARENTHESIS', 'NEWLINE', 'IF', 
    'OPEN_PARENTHESIS', 'VAR_FUNC_NAME', 'DIFFERENT', 'STRING', 'CLOSED_PARENTHESIS', 'COLON', 'NEWLINE', 'INDENT', 
    'VAR_FUNC_NAME', 'OPEN_BRACKET', 'VAR_FUNC_NAME', 'CLOSED_BRACKET', 'PLUS_EQUALS', 'INT', 'NEWLINE', 'IF', 
    'VAR_FUNC_NAME', 'OPEN_BRACKET', 'VAR_FUNC_NAME', 'CLOSED_BRACKET', 'MORE', 'INT', 'COLON', 'NEWLINE', 'INDENT', 
    'BREAK', 'NEWLINE', 'DEDENT', 'DEDENT', 'VAR_FUNC_NAME', 'OPEN_BRACKET', 'INT', 'CLOSED_BRACKET', 'PLUS_EQUALS', 
    'INT', 'NEWLINE', 'VAR_FUNC_NAME', 'OPEN_BRACKET', 'INT', 'CLOSED_BRACKET', 'PLUS_EQUALS', 'INT', 'NEWLINE', 
    'VAR_FUNC_NAME', 'OPEN_BRACKET', 'INT', 'CLOSED_BRACKET', 'PLUS_EQUALS', 'INT', 'NEWLINE', 'DEDENT', 'DEDENT', 
    'EXCEPT', 'VAR_FUNC_NAME', 'VAR_FUNC_NAME', 'VAR_FUNC_NAME', 'COLON', 'NEWLINE', 'INDENT', 'PRINT', 'OPEN_PARENTHESIS', 
    'STRING', 'COMMA', 'VAR_FUNC_NAME', 'CLOSED_PARENTHESIS', 'NEWLINE', 'DEDENT', 'ENDMARKER']

    assert token_types == expected

def test_correct_pass_token(lexer):
    code = "pass"
    lexer.input(code)
    token_types = [token.type for token in lexer.token_stream]

    expected = ['PASS', 'ENDMARKER']

    assert token_types == expected

def test_correct_tokens_1(lexer):
    code = '''
def test_none(test):
    if test is None:
        val /= 1
        val *= 1
'''

    lexer.input(code)
    token_types = [token.type for token in lexer.token_stream]

    expected = ['DEF', 'VAR_FUNC_NAME', 'OPEN_PARENTHESIS', 'VAR_FUNC_NAME', 'CLOSED_PARENTHESIS', 
    'COLON', 'NEWLINE', 'INDENT', 'IF', 'VAR_FUNC_NAME', 'IS', 'NONE', 'COLON', 'NEWLINE', 'INDENT', 
    'VAR_FUNC_NAME', 'DIV_EQUALS', 'INT', 'NEWLINE', 'VAR_FUNC_NAME', 'MUL_EQUALS', 'INT', 'NEWLINE', 
    'DEDENT', 'DEDENT', 'ENDMARKER']

    assert token_types == expected

def test_correct_tokens_2(lexer):
    code = '''
while True:
    if value < 10 and value > 20:
        continue
    else:
        break
    counter -= 2
n *= -1.0
n1 - n2
n1 // n2
n1 //= n2
n1 % n2
n1 %= n2
'''

    lexer.input(code)
    token_types = [token.type for token in lexer.token_stream]

    expected = ['WHILE', 'TRUE', 'COLON', 'NEWLINE', 'INDENT', 'IF', 'VAR_FUNC_NAME', 
    'LESS', 'INT', 'AND', 'VAR_FUNC_NAME', 'MORE', 'INT', 'COLON', 'NEWLINE', 'INDENT', 
    'CONTINUE', 'NEWLINE', 'DEDENT', 'ELSE', 'COLON', 'NEWLINE', 'INDENT', 'BREAK', 
    'NEWLINE', 'DEDENT', 'VAR_FUNC_NAME', 'MINUS', 'ASSIGN', 'INT', 'NEWLINE', 'DEDENT', 
    'VAR_FUNC_NAME', 'MUL_EQUALS', 'MINUS', 'FLOAT', 'NEWLINE', 'VAR_FUNC_NAME', 'MINUS', 
    'VAR_FUNC_NAME', 'NEWLINE', 'VAR_FUNC_NAME', 'FLOOR_DIV', 'VAR_FUNC_NAME', 'NEWLINE', 
    'VAR_FUNC_NAME', 'FLOOR_DIV_EQUALS', 'VAR_FUNC_NAME', 'NEWLINE', 'VAR_FUNC_NAME', 'MODULO', 
    'VAR_FUNC_NAME', 'NEWLINE', 'VAR_FUNC_NAME', 'MODULO_EQUALS', 'VAR_FUNC_NAME', 'NEWLINE',
    'ENDMARKER']

    assert token_types == expected


def test_invalid_character(lexer):
    code = '''
@
def test():
    pass
'''
    lexer.input(code)
    assert lexer.error_count == 1

def test_invalid_string(lexer):
    code = '''
string = "\\""
string = """
'''
    lexer.input(code)
    assert lexer.error_count == 1

def test_invalid_string(lexer):
    code = '''
string = '\\''
string = \'\'\'
'''
    lexer.input(code)
    assert lexer.error_count == 1

def test_valid_float(lexer):
    code = '''
float = .9
float = 9.
float = 0.9
'''
    lexer.input(code)
    assert lexer.error_count == 0