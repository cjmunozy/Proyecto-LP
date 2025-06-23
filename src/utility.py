import datetime

def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()
    return data

def create_log_filename(username, tipo):
    now = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
    return f"{tipo}-{username}-{now}.txt"

def save_log(tokens, errors, username):
    nombre_log = create_log_filename(username, 'sintactico')
    ruta_log = f"./logs/{nombre_log}"
    with open(ruta_log, 'w', encoding='utf-8') as log:
        log.write("RECOGNIZED TOKENS:\n")
        for token in tokens:
            log.write(f"{token}\n")
        log.write("\nERRORS:\n")
        for error in errors:
            log.write(f"{error}\n")
    print(f"Log saved at: {ruta_log}")      

def lua_repl(parser):
    while True:
        try:
            s = input('lua > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)

# Cristhian Muñoz
def find_line(input, token):
    return input.count('\n', 0, token.lexpos) + 1

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1 