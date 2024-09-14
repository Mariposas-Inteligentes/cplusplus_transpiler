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
        'WHITESPACE'
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
    t_OPEN_PARENTHESIS = r'\('
    t_CLOSED_PARENTHESIS = r'\)'
    t_OPEN_BRACKET = r'\['
    t_CLOSED_BRACKET = r'\]'
    t_OPEN_CURLY_BRACKET = r'\{'
    t_CLOSED_CURLY_BRACKET = r'\}'

    t_COMMENT = r'\#.*'

    NO_INDENT = 0
    MAY_INDENT = 1
    MUST_INDENT = 2

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
        #if t.lexer.at_line_start and t.lexer.paren_count == 0:
        return t

    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = '\t'

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

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
m.build()           # Build the lexer
m.tokenize(data) 