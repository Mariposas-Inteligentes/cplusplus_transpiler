import ply.lex as lex
import sys

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
  'WS'
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

# t_VAR_FUNC_NAME = r'_*[a-zA-Z][a-z|A-Z|_|0-9]*'
t_FLOAT = r'[0-9]+\.[0-9]+'
t_INT = r'[0-9]+'

class analyzer(object):  
  def __init__(self):
    self.lexer = lex.lex()
    self.NO_INDENT = 0
    self.MAY_INDENT = 1
    self.MUST_INDENT = 2
    self.errors = 0
    self.token_stream = None

  def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

  def t_WS(self, t):
    r' [ ]+ '
    if t.lexer.at_line_start and t.lexer.paren_count == 0:
      return t

  def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)


  def t_VAR_FUNC_NAME(self, t):
    r'_*[a-zA-Z][a-z|A-Z|_|0-9]*'
    t.type = RESERVED.get(t.value, "VAR_FUNC_NAME")
    return t

  def new_token(self, type, lineno):
    tok = lex.LexToken()
    tok.type = type
    tok.value = None
    tok.lineno = lineno
    return tok

  def dedent(self, lineno):
    return self.new_token("DEDENT", lineno)

  def indent(self, lineno):
    return self.new_token("INDENT", lineno)

  def identify_indenations(self, token_stream):
    self.lexer.atLineStart = atLineStart = True
    indent = self.NO_INDENT
    for token in token_stream:
      token.atLineStart = atLineStart
      if token.type == "COLON":
        atLineStart = False
        indent = self.MAY_INDENT
        token.must_indent = False
      elif token.type == "NEWLINE": 
        atLineStart = True 
        if indent == self.MAY_INDENT: 
          indent = self.MUST_INDENT
        token.must_indent = False
      elif token.type == "WS":
        assert token.atLineStart == True
        atLineStart = True
        token.must_indent = False
      else:
        if indent == self.MUST_INDENT:
          token.must_indent = True
        else:
          token.must_indent = False
          atLineStart = False
          indent = self.NO_INDENT
      yield token
    self.lexer.atLineStart = atLineStart
 
  def assign_indentations(self, token_stream): 
    levels = [0] 
    depth = 0 
    lastSeenWhitespace = False 
    for token in token_stream: 
      if token.type == "WS": 
        depth = len(token.value) 
        lastSeenWhitespace = True 
        continue
      if token.type == "NEWLINE": 
          depth = 0 
          if lastSeenWhitespace or token.atLineStart: 
            continue
          yield token 
          continue
      lastSeenWhitespace = False 
      if token.must_indent: 
        if not (depth > levels[-1]): 
          print ("Indentation Error in line no " + str(token.lineno))
          sys.exit() 
        levels.append(depth) 
        yield self.indent(token.lineno) 
      elif token.atLineStart: 
        if depth == levels[-1]: 
          pass 
        elif depth > levels[-1]: 
          print ("Indentation Error in line no " + str(token.lineno))
          sys.exit() 
        else: 
          try: 
            i = levels.index(depth) 
          except ValueError: 
            print ("Indentation Error in line no " + str(token.lineno))
            sys.exit() 
          for z in range(i+1, len(levels)): 
            yield self.dedent(token.lineno) 
            levels.pop() 
        yield token 
    if len(levels) > 1: 
      assert token is not None 
      for z in range(1, len(levels)): 
        yield self.dedent(token.lineno) 

  def filter(self, addEndMarker=True):
    token_stream = iter(self.lexer.token, None)
    token_stream = self.identify_indenations(token_stream)
    token_stream = self.assign_indentations(token_stream)
    tok = None
    for tok in token_stream:
        yield tok
    if addEndMarker:
        lineno = 1
        if tok is not None:
            lineno = tok.lineno
        yield self.new_token("ENDMARKER", lineno)

  def input(self, data, addEndMarker = True): 
    self.lexer.parenthesisCount = 0 
    data += "\n" 
    self.lexer.input(data) 
    self.token_stream = self.filter(addEndMarker) 

  # def token(self): 
  #   try: 
  #     return self.token_stream.next() 
  #   except StopIteration: 
  #     return None

  def tokenize(self):
    while True:
      tok = self.lexer.token()
      if not tok: 
        break      # No more input
      print(tok)
    # print("\nIn the file, there were %d errors found" % self.errors)


# TODO(nosotros): borrar:
file_name = "prueba.py"
file = open(file_name, 'r', encoding='utf-8')
data = file.read()
file.close()
analyzer_lexer = analyzer()
analyzer_lexer.input(data)
analyzer_lexer.tokenize()

