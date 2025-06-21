import ply.lex as lex
import datetime

valid = []
errors = []

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
    'print': 'PRINT',
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
    'FLOAT',
    'INTEGER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'IDENTIFIER',

    # Diego Araujo
    'EQUALS', 'NEQUALS', 'LOWER', 'GREATER', 'LOWEREQUALS', 'GREATEREQUALS',
    'CONCAT', 'LEN',
    'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'COMMA', 'DOT',
    'STRING',

    # Randy Rivera
    'POWER', 'MOD',
    'ASSIGN', 'PLUSASSIGN', 'MINUSASSIGN', 'TIMESASSIGN', 
    'DIVIDEASSIGN', 'MODASSIGN', 'POWERASSIGN',
    'COLON', 'DOUBLECOLON',

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

def t_STRING(t):
    r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''
    # Eliminar las comillas del valor
    t.value = t.value
    return t


# Randy Rivera
# Expresión regular para números (enteros, flotantes y notación científica)
# Operadores aritméticos adicionales (algunos ya están definidos por Cristhian)
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

def t_FLOAT(t):
    r'\d+\.\d?'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Cristhian Muñoz
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    errors.append(
        f"[Error Léxico] Línea {t.lineno}, "
        f"Columna {find_column(t.lexer.lexdata, t)}: "
        f"Carácter no reconocido '{t.value[0]}'"
    )
    t.lexer.skip(1)

def t_multiline_comment(t):
    r'--\[\[(.|\n)*?\]\]'
    t.lexer.lineno += t.value.count('\n')  # Count newlines
    pass  # No action needed for multiline comments

def t_comment(t):
    r'--.*'
    pass  # No action needed for comments

def t_identifier(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t

# Ejecución del lexer
# Cristian Muñoz
def build_lexer():
    return lex.lex()

def leer_archivo(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    return contenido

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


lexer = build_lexer()

archivo = "tests/algoritmo-cristhian.lua"  # Reemplaza con tu archivo Lua
contenido = leer_archivo(archivo)
usuario = "cjmunozy"  # Reemplaza con tu nombre de usuario de GitHub
lexer.input(contenido)

for tok in lexer:
    valid.append(
        (
            f"Token: {tok.type:<12} "
            f"Valor: {repr(tok.value):<20} "
            f"Línea: {tok.lineno:<4} "
            f"Columna: {find_column(contenido, tok):<4} "
        )
    )

# guardar_log(valid, errors, usuario)
