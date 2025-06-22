def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read()
    return data

def create_log_filename(username):
    now = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
    return f"sintactico-{username}-{now}.txt"

def save_log(username):
    nombre_log = create_log_filename(username)
    ruta_log = f"./logs/{nombre_log}"
    # Escribe tokens y errores en el log
    with open(ruta_log, 'w', encoding='utf-8') as log:
        for error in errors:
            log.write(f"{error}\n")
    print(f"Log guardado en: {ruta_log}")

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