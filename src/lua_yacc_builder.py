from utility import find_line, find_column

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
    p[0] = ('chunk', p[1])

def p_block(p):
    '''block : stat_list opt_retstat'''
    p[0] = ('block', p[1], p[2])
    
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
    
def p_stat(p):
    '''stat : SEMICOLON
            | varlist ASSIGN explist
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
            p.parser.semantic_errors.append(
                f"Error semántico: 'break' usado fuera de un bucle en la línea {find_line(p.lexer.lexdata, p)}"
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
           | exp binop exp
           | unop exp'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = (p[2], p[1], p[3])







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
    if 'function' not in context_stack:
        print("Error semántico: 'return' fuera de una función o chunk")
        p.parser.semantic_errors.append(
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

def p_var(p):
    '''var : NAME
           | prefixexp LBRACKET exp RBRACKET
           | prefixexp DOT NAME'''
    if len(p) == 2:
        p[0] = ('var', p[1])
    elif len(p) == 5:
        if p[2] == '[':
            p[0] = ('index', p[1], p[3])
        else:
            p[0] = ('dot', p[1], p[3])

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
    p[0] = ('table', p[2])

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
