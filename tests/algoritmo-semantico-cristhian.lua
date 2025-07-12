-- Caso 1: Uso de variable no definida (ERROR)
print(x)

-- Caso 2: Declaración válida de variable local
local a = 10

-- Caso 3: Redeclaración de variable local en el mismo bloque (ERROR)
local a = 20

-- Caso 4: Uso de palabra reservada como nombre de variable (ERROR)
local function end()  -- 'end' es palabra reservada
end

-- Caso 5: Asignación de múltiples valores
local x, y = 1, 2

-- Caso 6: Operación aritmética válida
local z = x + y

-- Caso 7: Operación aritmética inválida (ERROR: tipos incompatibles)
local resultado = z + "cadena"

-- Caso 8: Uso válido de nil y booleanos
local v = nil
local b = true
local f = false