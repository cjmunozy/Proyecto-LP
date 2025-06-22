from lua_lexer_builder import tokens, leer_archivo
from ply import yacc
import datetime

errors = []

# Cristhian Muñoz
def p_start(p):
    'start : chunk'
    p[0] = p[1]


# Diego Araujo
def p_chunk(p):
    'chunk : block'
    pass

def p_block(p):
    '''block : stat_list retstat_opt'''
    pass
    
def p_stat_list(p):
    '''stat_list : stat_list stat
                 | empty'''
    pass

def p_retstat_opt(p):
    '''retstat_opt : retstat
                   | empty'''
    pass
    
def p_stat(p):
    '''stat : SEMICOLON
            | varlist ASSIGN explist
            | functioncall
            | BREAK'''
    pass

def p_goto(p):
    '''stat : GOTO IDENTIFIER'''
    pass

def p_do(p):
    '''stat : DO block END'''
    pass

# Randy Rivera
def p_stat_while(p):
    '''stat : WHILE expression DO block END'''
    pass

# Diego Araujo
def p_stat_repeat(p):
    '''stat : REPEAT block UNTIL expression'''
    pass

def p_stat_if(p):
    '''stat : IF expression THEN block elseif_blocks else_block END'''
    pass

def p_elseif_blocks(p):
    '''elseif_blocks : ELSEIF expression THEN block
                     | elseif_blocks ELSEIF expression THEN block
                     | empty'''
    pass

def p_else_block(p):
    '''else_block : ELSE block
                  | empty'''
    pass

# Cristhian Muñoz
def p_stat_for(p):
    '''stat : FOR IDENTIFIER ASSIGN expression COMMA expression DO block END'''
    pass

def p_stat_for_in(p):
    '''stat : FOR namelist IN explist DO block END'''
    pass


# Diego Araujo
def p_stat_function(p):
    '''stat : FUNCTION funcname funcbody'''
    pass

def p_stat_local_function(p):
    '''stat : LOCAL FUNCTION IDENTIFIER funcbody'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_retstat(p):
    '''retstat : RETURN explist SEMICOLON
               | RETURN explist
               | RETURN SEMICOLON
               | RETURN'''
    pass

def p_label(p):
    '''stat : DOUBLECOLON IDENTIFIER DOUBLECOLON'''
    pass

def p_funcname(p):
    '''funcname : IDENTIFIER funcname_tail method_opt''' 
    pass

def p_funcname_tail(p):
    '''funcname_tail : funcname_tail DOT IDENTIFIER
                     | empty'''
    pass

def p_method_opt(p):
    '''method_opt : COLON IDENTIFIER
                  | empty'''
    pass

def p_varlist(p):
    '''varlist : var
               | varlist COMMA var'''
    pass

def p_var(p):
    '''var : IDENTIFIER
           | prefixexp LBRACKET expression RBRACKET
           | prefixexp DOT IDENTIFIER'''
    pass

def p_namelist(p):
    '''namelist : IDENTIFIER
                | namelist COMMA IDENTIFIER'''
    pass

def p_explist(p):
    '''explist : expression
               | explist COMMA expression'''
    pass

# def p_exp_prefixexp(p):
#     '''expression : prefixexp'''
#     pass

def p_prefixexp(p):
    '''prefixexp : var
                 | functioncall
                 | LPAREN expression RPAREN'''
    pass

def p_functioncall(p):
    '''functioncall : prefixexp args
                    | prefixexp COLON IDENTIFIER args'''
    pass

def p_args(p):
    '''args : LPAREN RPAREN
            | LPAREN explist RPAREN
            | STRING
            | tableconstructor'''
    pass

def p_functiondef(p):
    '''expression : FUNCTION funcbody'''
    pass

def p_funcbody(p):
    '''funcbody : LPAREN RPAREN block END
                | LPAREN parlist RPAREN block END'''
    pass

def p_parlist(p):
    '''parlist : namelist vararg_tail
               | VARARG'''
    pass

def p_vararg_tail(p):
    '''vararg_tail : COMMA VARARG
                   | empty'''
    pass

def p_tableconstructor(p):
    '''tableconstructor : LBRACE RBRACE
                        | LBRACE fieldlist RBRACE'''
    pass

def p_fieldlist(p):
    '''fieldlist : field fieldsep_tail'''
    pass

def p_fieldsep_tail(p):
    '''fieldsep_tail : fieldsep fieldfield_tail_opt
                     | empty'''
    pass

def p_fieldfield_tail_opt(p):
    '''fieldfield_tail_opt : fieldlist
                           | empty'''
    pass

def p_field(p):
    '''field : LBRACKET expression RBRACKET ASSIGN expression
             | IDENTIFIER ASSIGN expression
             | expression'''
    
def p_fieldsep(p):
    '''fieldsep : COMMA
                | SEMICOLON'''
    pass

#Cristhian Muñoz
def p_functioncall_print(p):
    '''functioncall : PRINT LPAREN expression RPAREN
                    | PRINT LPAREN STRING RPAREN'''
    p[0] = p[3] if isinstance(p[3], (int, float)) else p[3].strip(r'\'|\"')

def p_functioncall_input(p):
    '''functioncall : INPUT LPAREN RPAREN'''
    p[0] = input("Input: ")

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
