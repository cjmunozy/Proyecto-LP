from lua_lexer_builder import tokens
from ply import yacc

# Cristhian Muñoz
def p_start(p):
    'start : expression'
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
        print(
            f"Error sintáctico en la línea {find_line(p.lexer.lexdata, p)}, "
            f"columna {find_column(p.lexer.lexdata, p)}: "
            f"Token inesperado '{p.value}'"
        )
    else:
        print("Error sintáctico en el final de la entrada")

# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('lua > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)
