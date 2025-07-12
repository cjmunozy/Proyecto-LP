from utility import *
from ply import yacc
from lua_lexer_builder import *

tabla_simbolos = {
        "variables":{},
        "tipos":{
            "str-funciones":["len","to_uppercase", "to_lowercase", "to_str"]
        }
    }

semantic_errors = []
context_stack = []

# Cristhian Muñoz
def p_start(p):
    'start : chunk'
    p[0] = p[1]

# Diego Araujo
# GOTO NAME
# DO block END

def p_chunk(p):
    '''chunk : block'''
    # p[0] = ('chunk', p[1])
    p[0] = p[1]

def p_block(p):
    '''block : stat_list opt_retstat'''
    # p[0] = ('block', p[1], p[2])
    p[0] = (p[1], p[2])
    
def p_stat_list(p):
    '''stat_list : stat
                | stat_list stat'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_opt_retstat(p):
    '''opt_retstat : empty
                | retstat'''
    p[0] = p[1]

def p_multiple_assign(p):
    '''multiple_assign : varlist ASSIGN explist'''
    variables = p[1]  # Lista de nombres de variables
    valores = p[3]    # Lista de tipos o valores

    if len(variables) != len(valores):
        print(f"Error semántico: Se esperaban {len(variables)} valores pero se recibieron {len(valores)}.")
        semantic_errors.append(
            f"Asignación múltiple con desajuste de longitud: {len(variables)} vars vs {len(valores)} exprs"
        )
        return

    for i in range(len(variables)):
        nombre = variables[i]
        tipo = valores[i]
        tabla_simbolos["variables"][nombre] = tipo
        print(f"[INFO] Variable '{nombre}' asignada con tipo '{tipo}'")

    
def p_stat(p):
    '''stat : SEMICOLON
            | multiple_assign
            | functioncall
            | LABEL
            | BREAK
            | GOTO NAME
            | DO block END
            | WHILE exp DO block END
            | REPEAT block UNTIL exp
            | IF exp THEN block elseif_list opt_else END
            | FOR NAME ASSIGN exp COMMA exp opt_third_exp DO block END
            | FOR namelist IN explist DO block END
            | FUNCTION funcname funcbody
            | LOCAL FUNCTION NAME funcbody
            | LOCAL attnamelist opt_assign'''
    if len(p) == 2:
        p[0] = ('stat', p[1])
    elif len(p) == 3:
        p[0] = ('stat', p[1], p[2])
    elif len(p) == 4:
        p[0] = ('stat', p[1], p[2], p[3])
    elif len(p) == 5:
        p[0] = ('stat', p[1], p[2], p[3], p[4])
    else:
        p[0] = ('stat',) + tuple(p[1:])
    if len(p) == 4 and p[2] == '=': #Diego Araujo
        vars = p[1]
        vals = p[3]
        
        if len(vals) < len(vars):
            vals += ['nil'] * (len(vars) - len(vals))  # completar con nil
        elif len(vals) > len(vars):
            vals = vals[:len(vars)]  # descartar valores sobrantes

        p[0] = ('assign', vars, vals)
    elif p[1] == 'WHILE':
        context_stack.append('loop')
        ...
        context_stack.pop()
    elif p[1] == 'REPEAT':
        context_stack.append('loop')
        ...
        context_stack.pop()
    elif p[1] == 'FOR':
        context_stack.append('loop')
        ...
        context_stack.pop()
    elif len(p) == 2 and p[1] == 'BREAK':
        if 'loop' not in context_stack:
            print("Error semántico: 'break' usado fuera de un bucle")
            semantic_errors.append(
                f"Error semántico: 'break' usado fuera de un bucle en la línea {find_line(p.lexer.lexdata, p.slice[1])}"
            )
        p[0] = ('break',)

# Randy Rivera
# WHILE exp DO block END

def p_elseif_list(p):
    '''elseif_list : empty
                | elseif_list ELSEIF exp THEN block'''
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[1] + [('elseif', p[3], p[5])]

def p_opt_else(p):
    '''opt_else : empty
                | ELSE block'''
    if len(p) == 2:
        p[0] = None
    else:
        p[0] = ('else', p[2])

def p_opt_third_exp(p):
    '''opt_third_exp : empty
                    | COMMA exp'''
    if len(p) == 2:
        p[0] = None
    else:
        p[0] = p[2]

def p_opt_assign(p):
    '''opt_assign : empty
                | ASSIGN explist'''
    if len(p) == 2:
        p[0] = None
    else:
        p[0] = p[2]

def p_attnamelist(p):
    '''attnamelist : NAME attrib
                | attnamelist COMMA NAME attrib'''
    if len(p) == 3:
        p[0] = [('name', p[1], p[2])]
    else:
        p[0] = p[1] + [('name', p[3], p[4])]

def p_attrib(p):
    '''attrib : empty
            | LOWER NAME GREATER'''
    if len(p) == 2:
        p[0] = None
    else:
        p[0] = p[2]



def p_opt_explist(p):
    '''opt_explist : empty
                | explist'''
    p[0] = p[1]

def p_opt_semi(p):
    '''opt_semi : empty
                | SEMICOLON'''
    pass

def p_binary_exp(p):
    # Randy Rivera
    # Implementación de la Regla 2: Verificación de Tipos en Operaciones Aritméticas
    # Verificación de tipos para operaciones binarias
    'binary_exp : exp binop exp'
    operator = p[2]
    left = p[1]
    right = p[3]

    if is_numeric(left) and is_numeric(right):
        left = int(left)
        right = int(right)
        try:
            if operator == '+':
                result = left + right
            elif operator == '-':
                result = left - right
            elif operator == '*':
                result = left * right
            elif operator == '/':
                result = left / right
            elif operator == '%':
                result = left % right
            elif operator == '^':
                result = left ** right
            elif operator == '//':
                result = left // right
            else:
                result = (operator, left, right)
            p[0] = result
        except Exception as e:
            print(f"Error en la operación: {e}")
            semantic_errors.append(str(e))
            p[0] = (operator, left, right)
    else:
        print(f"Error semántico: Operación aritmética '{operator}' aplicada a tipos no numéricos")
        semantic_errors.append(
            f"Operación aritmética '{operator}' requiere operandos numéricos"
        )

# Cristhian Muñoz
# Implementación de la Regla : Detección de tipos en expresiones unarias
def p_exp(p):
    '''exp : NIL
        | FALSE
        | TRUE
        | NUMBER
        | STRING
        | DOTDOTDOT
        | functiondef
        | prefixexp
        | tableconstructor
        | arrayconstructor
        | tupleconstructor
        | binary_exp
        | unop exp'''
    if len(p) == 2:
        token_type = p.slice[1].type
        if token_type == "NIL":
            p[0] = None
        elif token_type == "FALSE":
            p[0] = False
        elif token_type == "TRUE":
            p[0] = True
        elif token_type == "DOTDOTDOT":
            p[0] = '...'
        if token_type == "NUMBER":
            p[0] = p[1]  # Retorna el número como está
        elif token_type == "STRING":
            p[0] = "str"
        else:
            p[0] = p[1]

def p_opt_parlist(p):
    '''opt_parlist : empty
                | parlist'''
    p[0] = p[1]

def p_opt_fieldlist(p):
    '''opt_fieldlist : empty
                    | fieldlist'''
    p[0] = p[1]

def p_unop(p):
    '''unop : MINUS
            | NOT
            | LEN
            | BITNOT'''
    p[0] = p[1]

# Diego Araujo
# REPEAT block UNTIL exp
# IF exp THEN block elseif_list opt_else END
# FUNCTION funcname funcbody
# LOCAL FUNCTION NAME funcbody

def p_empty(p):
    'empty :'
    pass

# Diego Araujo
def p_retstat(p):
    '''retstat : RETURN opt_explist opt_semi'''
    # Permitir return si estamos en función o en el chunk principal (stack vacío)
    if 'function' not in context_stack and context_stack != []:
        print("Error semántico: 'return' fuera de una función o chunk")
        semantic_errors.append(
            f"Error semántico: 'return' fuera de una función o chunk en la línea {find_line(p.lexer.lexdata, p.slice[1])}"
        )
    p[0] = ('return', p[2])

def p_funcname(p):
    '''funcname : NAME funcname_tail'''
    p[0] = ('funcname', p[1], p[2])

def p_funcname_tail(p):
    '''funcname_tail : empty
                    | DOT NAME funcname_tail
                    | COLON NAME funcname_tail'''
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [(p[2], p[1])] + p[3]

def p_varlist(p):
    '''varlist : var
            | varlist COMMA var'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# Cristhian Muñoz
# Implementación de la Regla: Detección de variables no definidas
def p_var(p):
    '''var : NAME
        | prefixexp LBRACKET exp RBRACKET
        | prefixexp DOT NAME'''
    if len(p) == 2:
        nombre = p[1]
        if not check_reserved_word_usage(nombre, p):
            return  # Si es una palabra reservada, no continuar
        if nombre not in tabla_simbolos["variables"]:
            error = (
                    f"Error semántico en la línea {find_line(p.lexer.lexdata, p.slice[1])}, "
                    f"columna {find_column(p.lexer.lexdata, p.slice[1])}: "
                    f"la variable '{nombre}' no ha sido definida."
                )
            print(error)
            semantic_errors.append(error)
            p[0] = ("var", nombre, "undef")
        else:
            p[0] = ("var", nombre, tabla_simbolos["variables"][nombre])
    elif len(p) == 5:
        if p[2] == '[':
            p[0] = ('index', p[1], p[3])
        else:
            p[0] = ('dot', p[1], p[3])

# Implementación de la Regla: Verificación de uso de palabras reservadas
def check_reserved_word_usage(nombre, token):
    """Verifica que no se usen palabras reservadas como nombres de variables"""
    if nombre.lower() in reserved:
        error = (
            f"Error semántico en la línea {find_line(token.lexer.lexdata, token.slice[1])}, "
            f"columna {find_column(token.lexer.lexdata, token.slice[1])}: "
            f"{nombre} es una palabra reservada y no puede usarse como identificador"
        )
        semantic_errors.append(error)
        return False
    return True

def p_namelist(p):
    '''namelist : NAME
                | namelist COMMA NAME'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_explist(p):
    '''explist : exp
            | explist COMMA exp'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_prefixexp(p):
    '''prefixexp : var
                | functioncall
                | LPAREN exp RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_functioncall(p):
    '''functioncall : prefixexp args
                    | prefixexp COLON NAME args'''
    if len(p) == 3:
        p[0] = ('call', p[1], p[2])
    else:
        p[0] = ('method', p[1], p[3], p[4])

def p_args(p):
    '''args : LPAREN opt_explist RPAREN
            | tableconstructor
            | STRING'''
    if len(p) == 4:
        p[0] = ('args', p[2])
    else:
        p[0] = ('args', p[1])

def p_functiondef(p):
    '''functiondef : FUNCTION funcbody'''
    p[0] = ('function', p[2])

# Diego Araujo
def p_funcbody(p):
    '''funcbody : LPAREN opt_parlist RPAREN block END'''
    context_stack.append('function')
    p[0] = ('funcbody', p[2], p[4])
    context_stack.pop()

def p_parlist(p):
    '''parlist : namelist COMMA DOTDOTDOT
            | namelist
            | DOTDOTDOT'''
    if len(p) == 4:
        p[0] = ('parlist', p[1], True)
    elif len(p) == 2:
        if p[1] == '...':
            p[0] = ('parlist', [], True)
        else:
            p[0] = ('parlist', p[1], False)

def p_tableconstructor(p):
    '''tableconstructor : LBRACE opt_fieldlist RBRACE'''
    p[0] = ('table', p[3])

def p_tupleconstructor(p):
    '''tupleconstructor : LPAREN opt_fieldlist RPAREN''' # bug porque no p[2]
    p[0] = ('tuple')

def p_arrayconstructor(p):
    '''arrayconstructor : LBRACKET opt_fieldlist RBRACKET''' # bug porque no p[2]
    p[0] = ('array')

def p_fieldlist(p):
    '''fieldlist : field
                | fieldlist fieldsep field
                | fieldlist fieldsep'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = p[1] + [p[3]]

def p_field(p):
    '''field : LBRACKET exp RBRACKET ASSIGN exp
            | NAME ASSIGN exp
            | exp'''
    if len(p) == 6:
        p[0] = ('key', p[2], p[5])
    elif len(p) == 4:
        p[0] = ('assign', p[1], p[3])
    else:
        p[0] = ('value', p[1])
    
def p_fieldsep(p):
    '''fieldsep : COMMA
                | SEMICOLON'''
    pass

# Cristhian Muñoz
# FOR NAME ASSIGN exp COMMA exp opt_third_exp DO block END
# FOR namelist IN explist DO block END
# def p_functioncall_print(p):
#     '''functioncall : PRINT LPAREN expression RPAREN
#                     | PRINT LPAREN STRING RPAREN'''
#     p[0] = p[3] if isinstance(p[3], (int, float)) else p[3].strip(r'\'|\"')

# def p_functioncall_input(p):
#     '''functioncall : INPUT LPAREN RPAREN'''
#     p[0] = input("Input: ")

def p_binop(p):
    '''binop : PLUS
            | MINUS
            | TIMES
            | DIVIDE
            | IDIV
            | POWER
            | MOD
            | BITAND
            | BITOR
            | BITXOR
            | SHIFTL
            | SHIFTR
            | CONCAT
            | LOWER
            | LOWEREQUALS
            | GREATER
            | GREATEREQUALS
            | EQUALS
            | NEQUALS
            | AND
            | OR'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(
            f"Error sintáctico en la línea {find_line(p.lexer.lexdata, p)}, "
            f"columna {find_column(p.lexer.lexdata, p)}: "
            f"Token inesperado '{p.value}'"
        )
    else:
        print(
            "Error sintáctico: Fin de archivo inesperado"
        )

class syntactic_analyzer:

    def __init__(self):
        self.parser = yacc.yacc()
        self.semantic_errors = semantic_errors
        self.context_stack = context_stack
        # 1. Agregar mi tabla de símbolos
        self.tabla_simbolos = tabla_simbolos

    def analizar_sintactico(self, codigo):
        return self.parser.parse(codigo)
    
    def analizar_semantico(self):
        return "\n".join(semantic_errors)
