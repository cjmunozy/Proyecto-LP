# Analizador Lua - Proyecto de Lenguajes de Programación

## Descripción

Este proyecto es un analizador léxico, sintáctico y semántico para el lenguaje Lua, desarrollado en Python utilizando la biblioteca [PLY](https://www.dabeaz.com/ply/). Incluye una interfaz gráfica construida con Tkinter para facilitar la carga y análisis de archivos `.lua`.

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.8 o superior

### Librerías necesarias

Instala las siguientes librerías con pip:

```bash
pip install ply
```

> **Nota:** Tkinter viene incluido con la mayoría de las instalaciones de Python estándar. Si tienes problemas, revisa la documentación de tu sistema operativo para instalarlo.

## Estructura del proyecto

- `src/`  
  - `main.py` — Interfaz gráfica y punto de entrada principal.
  - `lua_lexer_builder.py` — Analizador léxico.
  - `lua_yacc_builder.py` — Analizador sintáctico y semántico.
  - `utility.py` — Funciones auxiliares.
- `tests/`  
  - Archivos `.lua` de prueba.
- `logs/`  
  - Carpeta donde se guardan los logs de análisis.

## Ejecución

Desde la raíz del proyecto, ejecuta:

```bash
python src/main.py
```
