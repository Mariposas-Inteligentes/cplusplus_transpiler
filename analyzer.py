import ply.lex as lex

class MyLexer(object):
    tokens = (
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
        'IS',
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
        'COMMENT',
        'INDENT',
        'DEDENT',
        'NEWLINE',
        'VAR_FUNC_NAME',
        'INT',
        'FLOAT',
        'STRING',
        'WHITESPACE',
        'ENDMARKER',
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
        "is": "IS",
        "None": "NONE",
    }

    t_STRING = r'(\'(\w| |\\\'|\t|\.|,|\!|\?|@|\#|\$|%|\^|&|\*|\(|\)|\[|\]|\{|\}|-|=|\+|;|:|~|`|<|>|/|\\|\\n|\\t|\\\")*\')|(\"(\w| |\\\'|\t|\.|,|\!|\?|@|\#|\$|%|\^|&|\|\(|\)|\[|\]|\{|\}|-|=|\+|;|:|~|`|<|>|/|\\|\\n|\\t|\\\")\")'

    t_EQUALS = r'=='
    t_DIFFERENT = r'!='
    t_LESS_EQUALS = r'<='
    t_MORE_EQUALS = r'>='
    t_LESS = r'<'
    t_MORE = r'>'

    t_ASSIGN = r'='
    t_PLUS_EQUALS = r'\+='
    t_MINUS_EQUALS = r'-='
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
    t_COLON = r'\:'

    t_ignore_COMMENT = r'\#.*'

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

    def t_FLOAT(self, t):
        r'[0-9]+\.[0-9]+'
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
    
    def t_WHITESPACE(self, t):
        r'[ ]+'

        if self.line_start == True and self.count_curly_brackets == 0 and self.count_brackets == 0 and self.count_parenthesis == 0:
            return t
        
        return None

    # Define a rule so we can track line numbers
    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.type = "NEWLINE"
        if self.count_curly_brackets == 0 and self.count_brackets == 0 and self.count_parenthesis == 0:
            return t

        return None

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = '\t'

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def __init__(self):
        self.line_start = True
        self.count_parenthesis = 0
        self.count_brackets = 0
        self.count_curly_brackets = 0
        self.NO_INDENT = 0
        self.MAY_INDENT = 1
        self.MUST_INDENT = 2

    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def track_tokens_filter(self, tokens):
        self.line_start = True
        line_start = True
        indentation = self.NO_INDENT
        colon = False

        for current_token in tokens:
            current_token.line_start = line_start
            if current_token.type == "COLON":
                line_start = False
                indentation = self.MAY_INDENT
                current_token.must_indent = False
                
            elif current_token.type == "NEWLINE":
                line_start = True
                if indentation == self.MAY_INDENT:
                    indentaton = self.MUST_INDENT
                current_token.must_indent = False

            elif current_token == "WHITESPACE":
                assert current_token.line_start == True
                line_start = True

            else:
                if indentation == self.MUST_INDENT:
                    current_token.must_indent = True
                else:
                    current_token.must_indent = False
                self.line_start = False
                indentation = self.NO_INDENT
        
            yield current_token
            self.at_line_start = line_start

    def new_token(self, type, lineno):
        tok = lex.LexToken()
        tok.type = type
        tok.value = None
        tok.lineno = lineno
        return tok

    # Synthesize a DEDENT tag
    def DEDENT(self, lineno):
        return self.new_token("DEDENT", lineno)

    # Synthesize an INDENT tag
    def INDENT(self, lineno):
        return self.new_token("INDENT", lineno)
        
    def indentation_filter(self, tokens):
        indentation_levels = [0]  # TODO(nosotros): [0]
        token = None
        depth = 0
        previous_was_ws = False

        for token in tokens:
            if token.type == "WHITESPACE":
                assert depth == 0
                depth = len(token.value)
                previous_was_ws = True
                continue
            elif token.type == "NEWLINE":
                depth = 0
                if previous_was_ws or token.line_start:  # Ignore blank lines
                    continue
                yield token
                continue
            previous_was_ws = False
            
            if token.must_indent:
                if not (depth > indentation_levels[-1]):
                    raise IndentationError("Expected an indented block")
                indentation_levels.append(depth)
                yield self.INDENT(token.lineno)

            elif token.line_start:
                if depth > indentation_levels[-1]:
                    raise IndentationError("Invalid indentation increase")
                elif depth < indentation_levels[-1]:  # Check if previous level matches
                    try:
                        i = indentation_levels.index(depth)
                    except ValueError:
                        raise IndentationError("inconsistent indentation")
                    for _ in range(i+1, len(indentation_levels)):
                        yield self.DEDENT(token.lineno)
                        indentation_levels.pop()
                        
            yield token
        if len(indentation_levels) > 1:  # Dedent remaining levels
            assert token is not None
            for _ in range(1, len(indentation_levels)):
                yield self.DEDENT(token.lineno)
             
    def filter(self):
        current_token = None
        tokens = iter(self.lexer.token, None)
        tokens = self.track_tokens_filter(tokens)
        for currrent_token in self.indentation_filter(tokens):
            yield currrent_token
        lineno = 1
        if current_token is not None:
            lineno = current_token.lineno
        yield self.new_token("ENDMARKER", lineno)

    def input(self, source_code):
        self.count_parenthesis = 0
        self.count_brackets = 0
        self.count_curly_brackets = 0
        self.lexer.input(source_code)
        self.token_stream = self.filter()

    # Test it output
    def tokenize(self,data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

# Build the lexer and try it out
file_name = "prueba.py"
file = open(file_name, 'r', encoding='utf-8')
data = file.read()
file.close()
m = MyLexer()
m.build()
m.input(data) 
print(type(m.token_stream))

for _ in m.token_stream:
    print(next(m.token_stream))
