-- Regla 5: asignación múltiple mal ajustada
a, b = 1  -- falta un valor, b debería recibir nil (advertencia)

c = 1, 2, 3  -- hay más valores que variables (advertencia)

-- Regla 6: break fuera de un bucle (error)
break

-- Regla 7: return fuera de función (error)
return 42

-- Regla 7: return válido dentro de una función (debe pasar)
function f()
  return "ok"
end

-- Regla 6: break válido dentro de bucle (debe pasar)
for i = 1, 5 do
  break
end

local a = 5 + 4

local a = 5 + "4"

local a = 5 + "a"