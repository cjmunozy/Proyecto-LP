import ply.lex as lex
import ply.yacc as yacc

# --- Lexer ---

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

lexer = lex.lex()

# --- Parser ---

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
    '''stat : SEMI
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
              | LT NAME GT'''
    if len(p) == 2:
        p[0] = None
    else:
        p[0] = p[2]

def p_retstat(p):
    '''retstat : RETURN opt_explist opt_semi'''
    p[0] = ('return', p[2])

def p_opt_explist(p):
    '''opt_explist : empty
                   | explist'''
    p[0] = p[1]

def p_opt_semi(p):
    '''opt_semi : empty
                | SEMI'''
    pass

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
           | prefixexp LBRACK exp RBRACK
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

def p_funcbody(p):
    '''funcbody : LPAREN opt_parlist RPAREN block END'''
    p[0] = ('funcbody', p[2], p[4])

def p_opt_parlist(p):
    '''opt_parlist : empty
                   | parlist'''
    p[0] = p[1]

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
    '''tableconstructor : LCURLY opt_fieldlist RCURLY'''
    p[0] = ('table', p[2])

def p_opt_fieldlist(p):
    '''opt_fieldlist : empty
                     | fieldlist'''
    p[0] = p[1]

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

def p_fieldsep(p):
    '''fieldsep : COMMA
                | SEMI'''
    pass

def p_field(p):
    '''field : LBRACK exp RBRACK ASSIGN exp
             | NAME ASSIGN exp
             | exp'''
    if len(p) == 6:
        p[0] = ('key', p[2], p[5])
    elif len(p) == 4:
        p[0] = ('assign', p[1], p[3])
    else:
        p[0] = ('value', p[1])

def p_binop(p):
    '''binop : PLUS
             | MINUS
             | TIMES
             | DIVIDE
             | IDIV
             | POW
             | MOD
             | BITAND
             | BITOR
             | BITXOR
             | SHIFTL
             | SHIFTR
             | CONCAT
             | LT
             | LE
             | GT
             | GE
             | EQ
             | NE
             | AND
             | OR'''
    p[0] = p[1]

def p_unop(p):
    '''unop : MINUS
            | NOT
            | LEN
            | BITNOT'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors

def find_line(input, token):
    return input.count('\n', 0, token.lexpos) + 1

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ({p.value}) at line {p.lineno}")
        """
        # Información sobre la posición y línea
        print(
            f"Error sintáctico en la línea {find_line(p.lexer.lexdata, p)}, "
            f"columna {find_column(p.lexer.lexdata, p)}: "
            f"Token inesperado '{p.value}'"
        )
        """
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# main

def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()
    return data

# --- Example Usage ---
if __name__ == '__main__':
    
    file = "tests/algorithm_randy.lua"  # Reemplaza con tu archivo Lua
    data = read_file(file)
    user = "randyRivera0"  # Reemplaza con tu nombre de usuario de GitHub

    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    
    result = parser.parse(data)
    print(result)

    while True:
        try:
            s = input('lua > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)