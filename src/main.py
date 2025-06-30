from ply import lex, yacc

from lua_lexer_builder import *

from lua_yacc_builder import *

from utility import *

valid, errors =  [], []
semantic_errors = []

if __name__ == '__main__':
    lexer = lex.lex()
    parser = yacc.yacc()
    
    username = "randyRivera0"
    file = "tests/semantic_errors_copy.lua"
    data = read_file(file)

    lexer.input(data)

    for tok in lexer:
        valid.append(
            (
                f"Token: {tok.type:<12} "
                f"Value: {repr(tok.value):<20} "
                f"Line: {tok.lineno:<4} "
                f"Column: {find_column(data, tok):<4} "
            )
        )
        print(f"""Token: {tok.type:<12} Value: {repr(tok.value):<20} Line: {tok.lineno:<4} Column: {find_column(data, tok):<4} """)
    
    parser.semantic_errors = semantic_errors
    result = parser.parse(data)
    print(result)

    save_log(valid, errors, username)
    save_semantic_log(semantic_errors, username)
    lua_repl(parser)
