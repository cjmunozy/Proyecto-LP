import sys
import os
import datetime
from lua_lexer_builder import build_lexer

if len(sys.argv) != 2:
    print("Usage: python run_lexer.py <file.lua>")
    sys.exit(1)

input_file = sys.argv[1]
with open(input_file, 'r', encoding='utf-8') as f:
    data = f.read()

lexer = build_lexer()
lexer.input(data)

# Log file
username = "DiegoA00"  # replace with your actual GitHub username
now = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
log_filename = f"lexico-{username}-{now}.txt"
os.makedirs("logs", exist_ok=True)
log_path = os.path.join("logs", log_filename)

with open(log_path, 'w', encoding='utf-8') as log:
    while True:
        tok = lexer.token()
        if not tok:
            break
        log.write(f"Token: {tok.type:<12} Value: {repr(tok.value):<20} Line: {tok.lineno:<4} Pos: {tok.lexpos}\n")

print(f"Lexical analysis completed. Log saved to: {log_path}")