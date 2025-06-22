from ply import lex, yacc

from lua_lex import *

from lua_syntax import *

from utility import *

if __name__ == '__main__':
    lexer = lex.lex()
    parser = yacc.yacc()
    
    file = "tests/algoritmo-cristhian.lua"
    data = read_file(file)
    user = "randyRivera0"

    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
    
    result = parser.parse(data)
    print(result)

    lua_repl(parser)

    save_log(user)
