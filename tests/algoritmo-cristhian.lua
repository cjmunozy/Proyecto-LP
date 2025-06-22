-- Ejemplo de código Lua para probar el analizador léxico

-- Declaración de variables
local a = 10
local b = 20
local c = a + b * 2

-- Función para imprimir el resultado
local function calcular()
    if c > 30 then
        print("El resultado es mayor que 30")
    elseif c == 30 then
        print("El resultado es igual a 30")
    else
        print("El resultado es menor que 30")
    end
end

-- Llamada a la función
calcular()

-- Operaciones adicionales
local d = 2 ^ 3    -- Potencia
local e = d % 5    -- Módulo

-- Comentario de una sola línea
-- Este es un comentario

-- Comentario multilinea
--[[
    Este es un comentario
    que ocupa varias líneas.
]]

-- Concatenación de cadenas
local saludo = "Hola" .. " " .. "Mundo"
print(saludo)

-- Uso de tabla (estructura de datos)
local persona = { nombre = "Juan", edad = 25 }
print(persona.nombre, persona.edad)

-- Uso de while loop
local i = 1
while i <= 5 do
    print("Iteración: " .. i)
    i = i + 1
end

-- Uso de for loop
for j = 1, 5 do
    print("Número: " .. j)
end

-- Código con errores léxicos (intencionales)
local @error = 5.2     -- Error léxico: símbolo inválido '@'
local otro = #$5     -- Error léxico: símbolo inválido '$'

-- Operaciones con múltiples operadores
local resultado = (a + b) * (c - d) / e
local resultado2 = (a + b) * c /(a - (d + e))

-- Imprimir el resultado final
print("Resultado final: " .. resultado)
