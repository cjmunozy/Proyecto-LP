from lua_lexer_builder import tokens, leer_archivo
from ply import yacc
import datetime

errors = []

# Cristhian Muñoz
def p_start(p):
    'start : expression'
    p[0] = p[1]

def p_start_input(p):
    'start : input'
    p[0] = p[1]

def p_start_print(p):
    'start : print'
    p[0] = p[1]

def p_binary_operators(p):
    '''expression : expression PLUS term
                  | expression MINUS term
       term       : term TIMES factor
                  | term DIVIDE factor
                  | term POWER factor'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '^':
        p[0] = p[1] ** p[3]

def multiple_operators(p):
    '''expression : expression PLUS LPAREN term RPAREN
                  | expression MINUS LPAREN term RPAREN
       term       : term TIMES LPAREN expression RPAREN
                  | term DIVIDE LPAREN expression RPAREN
                  | term POWER LPAREN expression RPAREN'''
    if p[2] == '+=':
        p[0] = p[1] + p[4]
    elif p[2] == '-=':
        p[0] = p[1] - p[4]
    elif p[2] == '*=':
        p[0] = p[1] * p[4]
    elif p[2] == '/=':
        p[0] = p[1] / p[4]
    elif p[2] == '^=':
        p[0] = p[1] ** p[4]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : INTEGER'
    p[0] = int(p[1])

def p_factor_float(p):
    'factor : FLOAT'
    p[0] = float(p[1])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_print(p):
    '''print : PRINT LPAREN expression RPAREN
             | PRINT LPAREN STRING RPAREN'''
    p[0] = p[3] if isinstance(p[3], (int, float)) else p[3].strip(r'\'|\"')

def p_input(p):
    'input : INPUT LPAREN RPAREN'
    p[0] = input("Input: ")

# Diego Araujo


# Randy Rivera



# Cristhian Muñoz
def find_line(input, token):
    return input.count('\n', 0, token.lexpos) + 1

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Error rule for syntax errors
def p_error(p):
    if p:
        # Información sobre la posición y línea
        errors.append(
            f"Error sintáctico en la línea {find_line(p.lexer.lexdata, p)}, "
            f"columna {find_column(p.lexer.lexdata, p)}: "
            f"Token inesperado '{p.value}'"
        )
    else:
        errors.append(
            "Error sintáctico: Fin de archivo inesperado"
        )

def crear_log_filename(username):
    now = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
    return f"sintactico-{username}-{now}.txt"

def guardar_log(username):
    nombre_log = crear_log_filename(username)
    ruta_log = f"./logs/{nombre_log}"
    # Escribe tokens y errores en el log
    with open(ruta_log, 'w', encoding='utf-8') as log:
        for error in errors:
            log.write(f"{error}\n")
    print(f"Log guardado en: {ruta_log}")

def probar_salida():
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)

# Build the parser
parser = yacc.yacc()

archivo = "tests/algoritmo-cristhian.lua"  # Reemplaza con tu archivo Lua
contenido = leer_archivo(archivo)
usuario = "cjmunozy"  # Reemplaza con tu nombre de usuario de GitHub
result = parser.parse(contenido)

# Descomentar para guardar el log
guardar_log(usuario)

# Descomentar para probar con entrada por consola
# probar_salida()
