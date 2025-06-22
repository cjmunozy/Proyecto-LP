errors = []

tokens = (
    'NAME', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'IDIV', 'MOD', 'POW',
    'CONCAT', 'LEN', 'BITNOT', 'BITAND', 'BITOR', 'BITXOR', 'SHIFTL', 'SHIFTR',
    'EQ', 'NE', 'LE', 'GE', 'LT', 'GT',
    'ASSIGN', 'LPAREN', 'RPAREN', 'LBRACK', 'RBRACK', 'LCURLY', 'RCURLY',
    'COMMA', 'SEMI', 'COLON', 'DOT', 'DOTDOT', 'DOTDOTDOT',
    'BREAK', 'DO', 'ELSE', 'ELSEIF', 'END', 'FALSE', 'FOR', 'FUNCTION', 'GOTO',
    'IF', 'IN', 'LOCAL', 'NIL', 'NOT', 'OR', 'AND', 'REPEAT', 'RETURN', 'THEN',
    'TRUE', 'UNTIL', 'WHILE', 'LABEL'
)

# Operators
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_IDIV     = r'//'
t_MOD      = r'%'
t_POW      = r'\^'
t_CONCAT   = r'\.\.'
t_LEN      = r'\#'
t_BITNOT   = r'~'
t_BITAND   = r'&'
t_BITOR    = r'\|'
t_BITXOR   = r'\~'
t_SHIFTL   = r'<<'
t_SHIFTR   = r'>>'
t_EQ       = r'=='
t_NE       = r'~='
t_LE       = r'<='
t_GE       = r'>='
t_LT       = r'<'
t_GT       = r'>'
t_ASSIGN   = r'='
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACK   = r'\['
t_RBRACK   = r'\]'
t_LCURLY   = r'\{'
t_RCURLY   = r'\}'
t_COMMA    = r','
t_SEMI     = r';'
t_COLON    = r':'
t_DOT      = r'\.'
t_DOTDOT   = r'\.\.'
t_DOTDOTDOT = r'\.\.\.'

# Keywords
reserved = {
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
    'and': 'AND',
    'repeat': 'REPEAT',
    'return': 'RETURN',
    'then': 'THEN',
    'true': 'TRUE',
    'until': 'UNTIL',
    'while': 'WHILE',
}

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_NUMBER(t):
    r'\d+\.?\d*([eE][+-]?\d+)?|0[xX][0-9a-fA-F]+'
    try:
        if 'x' in t.value or 'X' in t.value:
            t.value = int(t.value, 16)
        elif '.' in t.value or 'e' in t.value or 'E' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
    except ValueError:
        print(f"Integer value too large: {t.value}")
        t.value = 0
    return t

def t_STRING(t):
    r'(\'([^\\\n]|(\\.))*?\')|(\"([^\\\n]|(\\.))*?\")'
    t.value = t.value[1:-1]  # Remove quotes
    return t

def t_LABEL(t):
    r'::[a-zA-Z_][a-zA-Z0-9_]*::'
    t.value = t.value[2:-2]  # Remove ::
    return t

def t_multiline_comment(t):
    r'--\[\[(.|\n)*?\]\]'
    t.lexer.lineno += t.value.count('\n')  # Update line count
    pass  # Discard multiline comments

def t_comment(t):
    r'--[^\n]*'
    pass  # Discard single-line comments

t_ignore = ' \t\n\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)
