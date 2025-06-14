-- Author: Diego Araujo

--[[ This is a test 
    algorithm written in Lua
]]--

-- Variable declaration
local x = 10
local y = 3.14
local z = 2.5e10
local nombre = "Juan"
local activo = true
local datos = {1, 2, 3}
local config = {modo = "auto", estado = false}

-- Arithmetic and logical operations
x = x + y * z
y = y + 1
z = z - 5
activo = not activo

if x > 1000 then
    print("Valor grande")
elseif x == 0 then
    print("Cero")
else
    print("Valor pequeño")
end

-- Loop while
local contador = 0
while contador < 10 do
    contador = contador + 1
end

-- Simple function
function saludar(nombre)
    print("Hola, " .. nombre)
    return true
end

saludar("Ana")

-- Data structures and access
local persona = {
    nombre = "Luis",
    edad = 25,
    habilidades = {"Python", "Lua", "JavaScript"}
}

print(persona.nombre)
print(persona.habilidades[1])

