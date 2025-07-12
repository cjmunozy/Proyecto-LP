import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from ply import lex, yacc
from lua_lexer_builder import *
from lua_yacc_builder import *
from utility import *

valid, errors =  [], []

def analizar():
    entrada = texto_entrada.get("1.0", tk.END)
       
    try:
        # Análisis léxico
        tokens = lex_analyzer.obtener_tokens(entrada)
        salida_lexico = "\n".join([str(tok) for tok in tokens])

        # Análisis sintáctico
        resultado_sintactico = syntactic_analyzer.analizar_sintactico(entrada)

        # Análisis semántico
        resultado_semantico = syntactic_analyzer.analizar_semantico()

        # Mostrar resultados
        texto_salida.delete("1.0", tk.END)
        texto_salida.insert(tk.END, "✅ Análisis Léxico:\n" + salida_lexico + "\n\n")
        texto_salida.insert(tk.END, "✅ Análisis Sintáctico:\n" + str(resultado_sintactico) + "\n\n")
        texto_salida.insert(tk.END, "✅ Análisis Semántico:\n" + str(resultado_semantico))

    except Exception as e:
        messagebox.showerror("Error durante el análisis", str(e))

def cargar_archivo():
    ruta = filedialog.askopenfilename(filetypes=[("Archivos Lua", "*.lua"), ("Todos los archivos", "*.*")])
    if ruta:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            texto_entrada.delete("1.0", tk.END)
            texto_entrada.insert(tk.END, contenido)

if __name__ == '__main__':
    
    username = "randyRivera0"

    lex_analyzer = lex_analyzer()
    syntactic_analyzer = syntactic_analyzer()

    # for tok in lexer:
    #     valid.append(
    #         (
    #             f"Token: {tok.type:<12} "
    #             f"Value: {repr(tok.value):<20} "
    #             f"Line: {tok.lineno:<4} "
    #             f"Column: {find_column(data, tok):<4} "
    #         )
    #     )
    #     print(f"""Token: {tok.type:<12} Value: {repr(tok.value):<20} Line: {tok.lineno:<4} Column: {find_column(data, tok):<4} """)
    
    # parser.semantic_errors = semantic_errors
    # result = parser.parse(data)
    # print(result)

    # save_log(valid, errors, username)
    # save_semantic_log(semantic_errors, username)
    # lua_repl(parser)

    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("Analizador Lua")
    ventana.geometry("900x600")

    # Widgets
    tk.Label(ventana, text="Código Fuente:", font=("Arial", 12, "bold")).pack()
    texto_entrada = scrolledtext.ScrolledText(ventana, width=100, height=15)
    texto_entrada.pack()

    tk.Button(ventana, text="Cargar Archivo", command=cargar_archivo, bg="lightblue").pack(pady=5)
    tk.Button(ventana, text="Analizar", command=analizar, bg="lightgreen").pack(pady=5)

    tk.Label(ventana, text="Resultados:", font=("Arial", 12, "bold")).pack()
    texto_salida = scrolledtext.ScrolledText(ventana, width=100, height=15)
    texto_salida.pack()

    ventana.mainloop()
