-- Este es un comentario de una línea

--[[
   Este es un comentario de múltiples líneas
   que debería ser ignorado por el analizador léxico
]]

local function factorial(n)  -- palabra reservada: local, function
  if n == 0 then             -- palabras reservadas: if, then
    return 1                 -- palabra reservada: return
  else                       -- palabra reservada: else
    return n * factorial(n - 1)
  end                        -- palabra reservada: end
end

-- Llamar a la función con un valor válido
local resultado = factorial(5)
print("Resultado:", resultado)

-- Código con errores léxicos (intencionales)
local @error = 5     -- Error léxico: símbolo inválido '@'
local otro = #$5     -- Error léxico: símbolo inválido '$'
