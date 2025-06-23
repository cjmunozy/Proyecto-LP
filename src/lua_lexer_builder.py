# Cristhian Muñoz
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
    # 'input': 'INPUT',
    'local': 'LOCAL',
    'nil': 'NIL',
    'not': 'NOT',
    'or': 'OR',
    # 'print': 'PRINT',
    'repeat': 'REPEAT',
    'return': 'RETURN',
    'then': 'THEN',
    'true': 'TRUE',
    'until': 'UNTIL',
    'while': 'WHILE',
}

tokens = (
    # Cristhian Muñoz
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'NAME',

    # Diego Araujo
    'EQUALS', 'NEQUALS', 'LOWER', 'GREATER', 'LOWEREQUALS', 'GREATEREQUALS',
    'CONCAT', 'LEN',
    'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'COMMA', 'DOT',
    'STRING', 'DOTDOT',

    # Randy Rivera
    'POWER', 'MOD',
    'ASSIGN', 'PLUSASSIGN', 'MINUSASSIGN', 'TIMESASSIGN', 
    'DIVIDEASSIGN', 'MODASSIGN', 'POWERASSIGN',
    'COLON', 'DOUBLECOLON', 'NUMBER', 'LABEL', 'DOTDOTDOT', 
    'BITNOT', 'BITAND', 'BITOR', 'BITXOR', 'IDIV', 'SHIFTL', 'SHIFTR',

) + tuple(reserved.values())

# Cristhian Muñoz
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

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
t_DOTDOTDOT = r'\.\.\.'

def t_STRING(t):
    r'(\'([^\\\n]|(\\.))*?\')|(\"([^\\\n]|(\\.))*?\")'
    t.value = t.value[1:-1]
    return t


# Randy Rivera
# Operadores aritméticos
t_POWER = r'\^'  # Operador de potencia
t_MOD = r'%'     # Operador módulo

# Operadores de asignación
t_ASSIGN = r'='   # Asignación simple
t_PLUSASSIGN = r'\+='
t_MINUSASSIGN = r'-='
t_TIMESASSIGN = r'\*='
t_DIVIDEASSIGN = r'/='
t_MODASSIGN = r'%='
t_POWERASSIGN = r'\^='

# Delimitadores y separadores adicionales
t_COLON = r':'    # Dos puntos
t_DOUBLECOLON = r'::'  # Dos puntos dobles (usado en Lua para etiquetas)

t_BITNOT   = r'~'
t_BITAND   = r'&'
t_BITOR    = r'\|'
t_BITXOR   = r'\~'
t_IDIV     = r'//'
t_SHIFTL   = r'<<'
t_SHIFTR   = r'>>'
t_DOTDOT   = r'\.\.'

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

def t_LABEL(t):
    r'::[a-zA-Z_][a-zA-Z0-9_]*::'
    t.value = t.value[2:-2]  # Remove ::
    return t

# Cristhian Muñoz
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

t_ignore = ' \t\n\r'

def t_error(t):
    print(
        f"[Error Léxico] Línea {t.lineno}, "
        f"Columna {find_column(t.lexer.lexdata, t)}: "
        f"Carácter no reconocido '{t.value[0]}'"
    )
    t.lexer.skip(1)

def t_multiline_comment(t):
    r'--\[\[(.|\n)*?\]\]'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_comment(t):
    r'--.*'
    pass

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t

# Cristian Muñoz
def crear_log_filename(username):
    now = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
    return f"lexico-{username}-{now}.txt"

def guardar_log(tokens, errores, usuario):
    nombre_log = crear_log_filename(usuario)
    ruta_log = f"./logs/{nombre_log}"
    # Escribe tokens y errores en el log
    with open(ruta_log, 'w', encoding='utf-8') as log:
        log.write("TOKENS RECONOCIDOS:\n")
        for token in tokens:
            log.write(f"{token}\n")
        log.write("\nERRORES:\n")
        for error in errores:
            log.write(f"{error}\n")
    print(f"Log guardado en: {ruta_log}")
