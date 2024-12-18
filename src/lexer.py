import ply.lex as lex
from common import IndentationError

class Lexer(object):
    tokens = (
        'START_MARKER',
        'IF',
        'ELSE',
        'ELIF',
        'WHILE',
        'FOR',
        'BREAK',
        'CONTINUE',
        'PASS',
        'DEF',
        'RETURN',
        'CLASS',
        'TRUE',
        'FALSE',
        'AND',
        'OR',
        'NOT',
        'PRINT',
        'NONE',
        'PLUS',
        'MINUS',
        'MUL',
        'DIV',
        'FLOOR_DIV',
        'MODULO',
        'POWER',
        'EQUALS',
        'DIFFERENT',
        'LESS',
        'MORE',
        'LESS_EQUALS',
        'MORE_EQUALS',
        'ASSIGN',
        'PLUS_EQUALS',
        'MINUS_EQUALS',
        'MUL_EQUALS',
        'DIV_EQUALS',
        'MODULO_EQUALS',
        'FLOOR_DIV_EQUALS',
        'POWER_EQUALS',
        'COMMA',
        'PERIOD',
        'COLON',
        'OPEN_PARENTHESIS',
        'CLOSED_PARENTHESIS',
        'OPEN_BRACKET',
        'CLOSED_BRACKET',
        'OPEN_CURLY_BRACKET',
        'CLOSED_CURLY_BRACKET',
        'INDENT',
        'DEDENT',
        'NEWLINE',
        'VAR_FUNC_NAME',
        'INT',
        'FLOAT',
        'STRING',
        'WHITESPACE',        
        'TRY',
        'EXCEPT',
        'IN',
        'END_MARKER',
        'FAKE_NEWLINE'
    )

    RESERVED = {
        "if": "IF",
        "else": "ELSE",
        "elif": "ELIF",
        "while": "WHILE",
        "for": "FOR",
        "break": "BREAK",
        "continue": "CONTINUE",
        "pass": "PASS",
        "def": "DEF",
        "return": "RETURN",
        "class": "CLASS",
        "True": "TRUE",
        "False": "FALSE",
        "and": "AND",
        "or": "OR",
        "not": "NOT",
        "print": "PRINT",
        "None": "NONE",
        "try" : "TRY",
        "except" : "EXCEPT",
        "in" : "IN"
    }

    t_STRING = r'(\"(\\.|[^\"\n]|(\\\n))*\")|(\'(\\.|[^\'\n]|(\\\n))*\')'

    t_EQUALS = r'=='
    t_DIFFERENT = r'!='
    t_LESS_EQUALS = r'<='
    t_MORE_EQUALS = r'>='
    t_LESS = r'<'
    t_MORE = r'>'

    t_ASSIGN = r'='
    t_PLUS_EQUALS = r'\+='
    t_MINUS_EQUALS = r'\-='
    t_MUL_EQUALS = r'\*='
    t_DIV_EQUALS = r'\/='
    t_MODULO_EQUALS = r'\%='
    t_FLOOR_DIV_EQUALS = r'\/\/='
    t_POWER_EQUALS = r'\*\*\='

    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_FLOOR_DIV = r'\/\/'
    t_MODULO = r'\%'
    t_POWER = r'\*\*'

    t_COMMA = r'\,'
    t_PERIOD = r'\.'

    t_ignore_COMMENT = r'\#[^\n]*'
    
    def t_COLON(self, t):
        r':\ *'
        t.value = ':'
        t.type = 'COLON'
        return t

    def t_FLOAT(self, t):
        r'([0-9]*\.[0-9]+)|([0-9]+\.[0-9]*)'
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    def t_VAR_FUNC_NAME(self, t):
        r'_*[a-zA-Z][a-z|A-Z|_|0-9]*'
        t.type = self.RESERVED.get(t.value, "VAR_FUNC_NAME")
        return t

    def t_OPEN_PARENTHESIS(self, t):
        r'\('
        self.count_parenthesis += 1
        return t
    
    def t_CLOSED_PARENTHESIS(self, t):
        r'\)'
        self.count_parenthesis -= 1
        return t
    
    def t_OPEN_BRACKET(self, t):
        r'\['
        self.count_brackets += 1
        return t
    
    def t_CLOSED_BRACKET(self, t):
        r'\]'
        self.count_brackets -= 1
        return t
 
    def t_OPEN_CURLY_BRACKET(self, t):
        r'\{'
        self.count_curly_brackets += 1
        return t
    
    def t_CLOSED_CURLY_BRACKET(self, t):
        r'\}'
        self.count_curly_brackets -= 1
        return t
    
    def t_WHITESPACE(self, t):
        r'[ ]+'
        if self.line_start == True and self.count_curly_brackets == 0 and self.count_brackets == 0 and self.count_parenthesis == 0:
            return t

    def t_NEWLINE(self, t):
        r'\n'
        self.actual_line_no += 1
        t.lexer.lineno = self.actual_line_no
        t.lineno = self.actual_line_no
        t.type = "NEWLINE"
        if self.count_curly_brackets == 0 and self.count_brackets == 0 and self.count_parenthesis == 0:
            return t
        else:
            t.type = "FAKE_NEWLINE"
            return t

    t_ignore  = '\t'

    def t_error(self,t):
        t.lexer.skip(1)
        self.error_count += 1
        print(f"ERROR {self.error_count}. Illegal character '{t.value[0]}' at line {t.lineno}")        
        # Do not process indentation in the faulty line
        self.line_start = False 

    def __init__(self):
        self.line_start = True
        self.count_parenthesis = 0
        self.count_brackets = 0
        self.count_curly_brackets = 0
        self.error_count = 0
        self.count_token = 0
        self.actual_line_no = 1

        # Consts used to track indentation
        self.NO_INDENT = 0
        self.MAY_INDENT = 1
        self.MUST_INDENT = 2

    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def track_tokens_filter(self, tokens):
        # Track when to indent
        self.line_start = True
        line_start = True
        indentation = self.NO_INDENT
        new_tokens = []
        for current_token in tokens:
            current_token.line_start = line_start

            if current_token.type == "COLON":
                line_start = False
                indentation = self.MAY_INDENT
                current_token.must_indent = False
                
            elif current_token.type == "NEWLINE":
                line_start = True
                # If there was a colon beforehand, we must indent
                if indentation == self.MAY_INDENT:
                    indentation = self.MUST_INDENT
                current_token.must_indent = False

            elif current_token == "WHITESPACE":
                # If there was a whitspace elswhere, there is an error
                assert current_token.line_start == True
                line_start = True

            else:
                if indentation == self.MUST_INDENT:
                    current_token.must_indent = True
                else:
                    current_token.must_indent = False
                line_start = False
                indentation = self.NO_INDENT
        
            new_tokens.append(current_token)
            self.at_line_start = line_start

        return new_tokens

    def new_token(self, type, lineno, lexpos=-1):
        # Generate a synthetic token
        tok = lex.LexToken()
        tok.type = type
        tok.value = None
        tok.lineno = lineno
        tok.lexpos = lexpos
        return tok

    def DEDENT(self, lineno):
        return self.new_token("DEDENT", lineno)

    def INDENT(self, lineno):
        return self.new_token("INDENT", lineno)
        
    def indentation_filter(self, tokens):
        # Generate indent and dedent tokens
        indentation_levels = [0]
        token = None
        depth = 0
        previous_was_ws = False
        new_tokens = []

        for token in tokens:
            if token.type == "WHITESPACE":
                if depth == 0:
                    depth = len(token.value)
                    previous_was_ws = True
            
            if token.type == "NEWLINE":
                depth = 0
                # Ignore blank lines
                if previous_was_ws or token.line_start:
                    continue

                new_tokens.append(token)
                continue

            previous_was_ws = False
            if token.must_indent:
                if not (depth > indentation_levels[-1]):
                    raise IndentationError("Expected an indented block", token.lineno)
                indentation_levels.append(depth)
                new_tokens.append(self.INDENT(token.lineno))

            elif token.line_start:
                if depth == indentation_levels[-1]:
                    pass
                elif depth > indentation_levels[-1]:
                    raise IndentationError("Invalid indentation increase", token.lineno)
                else:
                    # Check if previous level matches
                    try:
                        i = indentation_levels.index(depth)
                    except ValueError:
                        raise IndentationError("Inconsistent indentation", token.lineno)
                    for _ in range(i+1, len(indentation_levels)):
                        new_tokens.append(self.DEDENT(token.lineno))
                        indentation_levels.pop()
                        
            if(token.type != "WHITESPACE"):
                new_tokens.append(token)

        if len(indentation_levels) > 1:
            # Dedent remaining levels
            assert token is not None
            for _ in range(1, len(indentation_levels)):
                new_tokens.append(self.DEDENT(token.lineno))

        return new_tokens


    def filter_ws(self, tokens):
        new_tokens = []
        i = 0
        for token in tokens:
            if (i-1 < 0 or i+1 >= len(tokens)):  # first or last token
                new_tokens.append(tokens[i])
            elif (token.type == "WHITESPACE" and tokens[i-1].type == "NEWLINE" and tokens[i+1].type == "NEWLINE"):  # I am whitespace and before and after is a newline
                pass
            else: # before and after was not a whitespace
                new_tokens.append(tokens[i])
            i +=1
        return new_tokens
       
    def filter(self):
        # Filter through the original tokens to create the new ones
        tokens = iter(self.lexer.token, None)

        new_tokens = []
        self.actual_line_no = 1
        for token in tokens:
            token.lineno = self.actual_line_no
            if token.type != 'FAKE_NEWLINE':
                new_tokens.append(token)

        new_tokens = self.filter_ws(new_tokens)       
        new_tokens = self.track_tokens_filter(new_tokens)
        new_tokens = self.indentation_filter(new_tokens)

        
        new_tokens.insert(0, self.new_token("START_MARKER", 0))
        new_tokens.append(self.new_token("NEWLINE", self.actual_line_no ))
        new_tokens.append(self.new_token("END_MARKER", self.actual_line_no))
        return new_tokens


    def input(self, source_code):
        # Attempt to lex the data with PLY to add INDENT and DEDENT tokens
        try:
            self.count_parenthesis = 0
            self.count_brackets = 0
            self.count_curly_brackets = 0
            self.lexer.input(source_code)
            self.token_stream = self.filter()
            self.count_token = 0
        except IndentationError as e:
            self.error_count += 1
            print(f"Error in input: {e.message} at line {e.lineno}")
            self.token_stream = []

    def tokenize(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

    def token(self):
        if self.count_token < len(self.token_stream):
            self.count_token += 1
            return self.token_stream[self.count_token-1]
        return None
        