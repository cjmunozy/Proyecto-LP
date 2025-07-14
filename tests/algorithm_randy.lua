-- Author Randy Rivera
-- Comentario de línea

--[[
    Comentario
    multilineas
]]--

-- Simple condition
if a == 1 then
    x = 5;
    x = x + 5
    print(x)
    -- Prueba de las 3 estructuras de datos
    local table = {1, 2, 3, 4, 5}
    local array = [1, 2, 3, 4, 5]
    local tuple = (1, 2, 3, 4, 5)
    -- Ajuste de asignacion multiple
    a, b, c = 4, 5, 6
    -- a, b, c = 3, 2
elseif a == 1 and not true or a < 5 then
    local a = "Hello World"
    dict = {name = "Alice", age = 30, active = true}
else
    j = 1 * 1 ^ 3.5 / 7
    local nested = {
        person = {
            name = "Bob",
            address = {
                street = "Main St",
                number = 123
            }
        },
        scores = {90, 85, 95}
    }
end

-- Bucles while
local i = 1
while i <= lista do
    print("Elemento de lista:", lista[i])
    i = i + 1
end

-- Operaciones aritméticas y lógicas variadas
a = 1 + 2 * 3 - 4 / 5
b = 1 ^ 2
f = not false
g = true or false and true