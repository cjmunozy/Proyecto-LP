import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from ply import lex, yacc
from lua_lexer_builder import *
from lua_yacc_builder import *
from utility import *

valid, errors = [], []

def analizar():
    entrada = texto_entrada.get("1.0", tk.END)
    try:
        tokens = lex_analyzer.obtener_tokens(entrada)
        resultado_sintactico = syntactic_analyzer.analizar_sintactico(entrada)
        resultado_semantico = syntactic_analyzer.analizar_semantico()

        # Mostrar resultados en pestañas
        salida_lexico.config(state='normal')
        salida_lexico.delete("1.0", tk.END)
        salida_lexico.insert(tk.END, "\n".join([str(tok) for tok in tokens]))
        salida_lexico.config(state='disabled')

        salida_sintactico.config(state='normal')
        salida_sintactico.delete("1.0", tk.END)
        salida_sintactico.insert(tk.END, str(resultado_sintactico))
        salida_sintactico.config(state='disabled')

        salida_semantico.config(state='normal')
        salida_semantico.delete("1.0", tk.END)
        salida_semantico.insert(tk.END, str(resultado_semantico))
        salida_semantico.config(state='disabled')

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
    username = "DiegoA00"
    lex_analyzer = lex_analyzer()
    syntactic_analyzer = syntactic_analyzer()

    # Ventana principal
    ventana = tk.Tk()
    ventana.title("Analizador Lua")
    ventana.geometry("1000x750")
    ventana.configure(bg="#181c24")

    # Frame para el label y los botones (en la misma línea)
    frame_superior = tk.Frame(ventana, bg="#181c24")
    frame_superior.pack(fill="x", padx=30, pady=(20, 0))

    # Label a la izquierda
    tk.Label(frame_superior, text="main.lua", font=("Consolas", 12, "bold"), bg="#181c24", fg="#7ec3fa").pack(side="left", pady=(0, 5))

    # Frame para los botones a la derecha
    frame_botones = tk.Frame(frame_superior, bg="#181c24")
    frame_botones.pack(side="right")
    tk.Button(frame_botones, text="Cargar Archivo", command=cargar_archivo, bg="#2d3748", fg="#7ec3fa", font=("Arial", 10, "bold")).pack(side="left", padx=5)
    tk.Button(frame_botones, text="Analizar", command=analizar, bg="#38b000", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

    # Frame para el editor de código con margen
    frame_editor = tk.Frame(ventana, bg="#181c24")
    frame_editor.pack(fill="both", expand=False, padx=30, pady=(0, 15))
    texto_entrada = scrolledtext.ScrolledText(frame_editor, width=120, height=20, bg="#232936", fg="#e6e6e6", insertbackground="#e6e6e6", font=("Consolas", 12), borderwidth=0, relief="flat")
    texto_entrada.pack(fill="both", expand=True)

    # Frame para las pestañas de resultados con margen
    frame_resultados = tk.Frame(ventana, bg="#181c24")
    frame_resultados.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    notebook = ttk.Notebook(frame_resultados)
    notebook.pack(expand=1, fill="both")

    style = ttk.Style()
    style.theme_use('default')
    style.configure('TNotebook', background='#232936', borderwidth=0)
    style.configure('TNotebook.Tab', background='#232936', foreground='#7ec3fa', font=('Arial', 10, 'bold'))
    style.map('TNotebook.Tab', background=[('selected', '#181c24')])

    salida_lexico = scrolledtext.ScrolledText(notebook, width=120, height=10, bg="#232936", fg="#e6e6e6", font=("Consolas", 11), borderwidth=0, relief="flat")
    salida_sintactico = scrolledtext.ScrolledText(notebook, width=120, height=10, bg="#232936", fg="#e6e6e6", font=("Consolas", 11), borderwidth=0, relief="flat")
    salida_semantico = scrolledtext.ScrolledText(notebook, width=120, height=10, bg="#232936", fg="#e6e6e6", font=("Consolas", 11), borderwidth=0, relief="flat")

    for widget in [salida_lexico, salida_sintactico, salida_semantico]:
        widget.config(state='disabled')

    notebook.add(salida_lexico, text="Léxico")
    notebook.add(salida_sintactico, text="Sintáctico")
    notebook.add(salida_semantico, text="Semántico")

    ventana.mainloop()
