import ply.lex as lex

class analyzer:
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
    'CLOSED_PARENTHESIS ',
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
    'STRING'
  )

  t_STRING = r'(\'(\w| |\\\'|\t|\.|,|\!|\?|@|#|\$|%|\^|&|\*|\(|\)|\[|\]|\{|\}|-|=|\+|;|:|~|`|<|>|/|\\|\\n|\\t|\\\")*\')|(\"(\w| |\\\'|\t|\.|,|\!|\?|@|#|\$|%|\^|&|\|\(|\)|\[|\]|\{|\}|-|=|\+|;|:|~|`|<|>|/|\\|\\n|\\t|\\\")\")'

  t_EQUALS = r'=='
  t_DIFFERENT = r'!='
  t_LESS_EQUALS = r'<='
  t_MORE_EQUALS = r'>='
  t_LESS = r'<'
  t_MORE = r'>'

  t_ASSIGN = r'='
  t_PLUS_EQUALS = r'+='
  t_MINUS_EQUALS = r'-='
  t_MUL_EQUALS = r'*='
  t_DIV_EQUALS = r'/='
  t_MODULO_EQUALS = r'%='
  t_FLOOR_DIV_EQUALS = r'//='
  t_POWER_EQUALS = r'**='

  t_PLUS = r'+'
  t_MINUS = r'-'
  t_MUL = r'*'
  t_DIV = r'/'
  t_FLOOR_DIV = r'//'
  t_MODULO = r'%'
  t_POWER = r'**'

  t_COMMA = r','
  t_PERIOD = r'.'
  t_COLON = r':'
  t_OPEN_PARENTHESIS = r'('
  t_CLOSED_PARENTHESIS = r')'
  t_OPEN_BRACKET = r'['
  t_CLOSED_BRACKET = r']'
  t_OPEN_CURLY_BRACKET = r'{'
  t_CLOSED_CURLY_BRACKET = r'}'

  t_COMMENT = r'#.*'

  #t_INDENT
  #t_DEDENT
  #t_NEWLINE

  t_VAR_FUNC_NAME = r'[a-z|A-Z|_][a-z|A-Z|_|0-9]*'
  t_FLOAT = r'[0-9]+\.[0-9]+'
  t_INT = r'[0-9]+'
  

