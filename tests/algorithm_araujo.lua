-- Author: Diego Araujo

--[[ Algoritmo de prueba variado y extenso para análisis léxico, sintáctico y semántico en Lua usando PLY ]]--

-- Declaración de variables con diferentes formatos numéricos y booleanos
local a = 42
local b = 0.5
local c = 6.022e23
local d = -15
local e = 0
local f = true
local g = false

-- Cadenas de texto con comillas simples y dobles
local saludo1 = "Hola"
local saludo2 = 'Mundo'
local multilinea = [[
Esto es
una cadena
multilinea
]]

-- Tablas: listas, diccionarios, mixtas y anidadas
local lista = {1, 2, 3, 4}
local diccionario = {nombre = "Diego", edad = 20}
local mixta = {"uno", 2, true, {x=1, y=2}}
local matriz = {
    {1,2,3},
    {4,5,6},
    {7,8,9}
}
local vacia = {}

-- Operaciones aritméticas y lógicas variadas
a = a + b * 2 - d / 5
b = b ^ 2
f = not f
g = f or g and true

-- Concatenación de cadenas
local frase = saludo1 .. ", " .. saludo2 .. "!"

-- Comentarios de línea
-- Esto es un comentario de línea

-- Comentarios multilínea
--[[
    Esto es un comentario
    de varias líneas
]]--

-- Condicionales con diferentes formatos y operadores
if a > 50 then print("a es mayor que 50") end

if b < 1 then
    print("b es menor que 1")
elseif b == 1 then
    print("b es igual a 1")
else
    print("b es mayor que 1")
end

if not g then
    print("g es falso")
end

-- Condicional en una línea
if f then print("f es verdadero") end

-- Bucles while, for y repeat-until
local i = 1
while i <= #lista do
    print("Elemento de lista:", lista[i])
    i = i + 1
end

for j = 1, #matriz do
    for k = 1, #matriz[j] do
        print("Matriz["..j.."]["..k.."]:", matriz[j][k])
    end
end

local suma = 0
local n = 1
repeat
    suma = suma + n
    n = n + 1
until n > 5
print("Suma de 1 a 5:", suma)

-- Funciones con diferentes formatos
function cuadrado(x)
    return x * x
end

local function cubo(x)
    return x * x * x
end

function imprimir_tabla(t)
    for k, v in pairs(t) do
        print("Clave:", k, "Valor:", v)
    end
end

-- Función anónima y asignación a variable
local doble = function(x) return x * 2 end

-- Llamadas a funciones
print("Cuadrado de 4:", cuadrado(4))
print("Cubo de 3:", cubo(3))
print("Doble de 7:", doble(7))
imprimir_tabla(diccionario)

-- Acceso y modificación de tablas
diccionario.edad = diccionario.edad + 1
print("Edad actualizada:", diccionario.edad)
lista[2] = 99
print("Nuevo valor en lista[2]:", lista[2])

-- Uso de booleanos y operadores lógicos
if diccionario.edad > 18 and f or g then
    print("Mayor de edad y condición lógica cumplida")
end

-- Ejemplo de shadowing de variables
local x = 10
do
    local x = 20
    print("x dentro del bloque:", x)
end
print("x fuera del bloque:", x)

-- Simulación de input
local color = input("¿Cuál es tu color favorito? ")
print("Tu color favorito es:", color)

-- Fin del algoritmo de prueba variado

