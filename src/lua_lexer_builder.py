import ply.lex as lex

# List of reserved words - Cristhian Muñoz
reserved = {
    'and': 'AND',
    'break': 'BREAK',
    'do': 'DO',
    'else': 'ELSE',
    'elseif': 'ELSEIF',
    'end': 'END',
    'false': 'FALSE',
    'for': 'FOR',
    'function': 'FUNCTION',
    'goto': 'GOTO',
    'if': 'IF',
    'in': 'IN',
    'local': 'LOCAL',
    'nil': 'NIL',
    'not': 'NOT',
    'or': 'OR',
    'repeat': 'REPEAT',
    'return': 'RETURN',
    'then': 'THEN',
    'true': 'TRUE',
    'until': 'UNTIL',
    'while': 'WHILE',
}

# List of token names.   This is always required
tokens = (
    # Cristhian Muñoz
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',

    # Diego Araujo
    'EQUALS', 'NEQUALS', 'LOWER', 'GREATER', 'LOWEREQUALS', 'GREATEREQUALS',
    'CONCAT', 'LEN',
    'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'COMMA', 'DOT',

    # Randy Rivera

) + tuple(reserved.values())

# Regular expression rules for simple tokens
# Cristhian Muñoz
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
# Diego Araujo


# Randy Rivera



# Cristhian Muñoz
# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_identifier(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t

# Diego Araujo
# Comparator Operators Lua
t_EQUALS        = r'=='
t_NEQUALS       = r'~='
t_LOWEREQUALS   = r'<='
t_GREATEREQUALS = r'>='
t_LOWER         = r'<'
t_GREATER       = r'>'

# Operador de concatenación y longitud
t_CONCAT    = r'\.\.'
t_LEN       = r'\#'

# Structurals Delimiters
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_SEMICOLON = r';'
t_COMMA     = r','
t_DOT       = r'\.'



# Randy Rivera


def build_lexer():
    return lex.lex()
