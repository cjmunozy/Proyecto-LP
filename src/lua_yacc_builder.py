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

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_factor_power(p):
    'factor : factor POWER factor'
    p[0] = p[1] ** p[3]

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
    'print : PRINT factor'
    p[0] = p[2]

def p_print_string(p):
    'print : PRINT LPAREN STRING RPAREN'
    p[0] = p[3]

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
        print("Error sintáctico en el final de la entrada")

# 
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

# Build the parser
parser = yacc.yacc()

archivo = "tests/algoritmo-cristhian.lua"  # Reemplaza con tu archivo Lua
contenido = leer_archivo(archivo)
usuario = "cjmunozy"  # Reemplaza con tu nombre de usuario de GitHub
result = parser.parse(contenido)
guardar_log(usuario)
