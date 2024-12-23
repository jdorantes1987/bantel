import pandas as pd

serpList = ["Boa", "Pitón", "Culebra venenosa", "Víbora Rayada"]
serpList2 = list(("Boa", "Pitón", "Culebra venenosa", "Víbora Rayada"))
serpList3 = {
    "Boa": "Serpiente Constrictora",
    "Pitón": "Serpiente Constrictora",
    "Cobra": "Culebra venenosa",
    "Víbora Rayada": "Culebra Inofensiva",
}
print(type(serpList2))
print(type(serpList3))
serpList4 = [
    {"Boa", "Pitón", "Víbora Rayada"},
    {"Serpiente ConstrictoraA", "Serpiente ConstrictoraB", "Culebra Inofensiva"},
    "Serps y sus niveles de riesgo",
]

print("Indice")
print(serpList4[0:2])

mi_lista = ["Juan", "Pedro", "Laura", "Carmen", "Susana"]
print(mi_lista[0])  # Muestra Juan (la primera posición es la 0)
print(mi_lista[-1])  # Muestra Susana
print(mi_lista[1])  # Muestra Pedro
print(mi_lista[2])  # Muestra Laura
print(mi_lista[-2])  # Muestra Carmen


edades = [20, 41, 6, 18, 23]
# Si queremos agregar nuevos elementos en una lista debemos usar extend en vez de append
edades.extend([60, 80, 90])
print("ejemplo extend")
print(edades)
# Recorriendo los elementos
for edad in edades:
    print(edad)

# Recorriendo los índices
for i in range(len(edades)):
    print(edades[i])

# Con while y los índices
indice = 0

while indice < len(edades):
    print(edades[indice])
    indice += 1

# Agregado elementos a una lista con append() en Python
números = []
números.append(10)
números.append(5)
números.append(3)

print(números)
# Mostrará [10, 5, 3]

# Uniendo listas en Python
números = []

# Unimos la lista anterior con una nueva
números = números + [10, 5, 3]

print(números)
# Mostrará [10, 5, 3]

# Removiendo un elemento de una lista con pop() en Python

palabras = ["hola", "hello", "ola"]

palabras.pop(1)

print(palabras)
# Mostrará ['hola', 'ola']

# Removiendo un elemento de una lista con remove() en Python
palabras = ["hola", "hello", "hello moto", "ola"]


palabras.remove("hello")

print(palabras)
# Mostrará ['hola', 'hello', 'ola']

# Hay cosas interesantes acá. Primero, remove buscará por ti el elemento y lo borrará.
# Sin embargo, solo borrará el primero que encuentra, no todos ellos.
# Por lo tanto, dado que "hello" estaba dos veces en nuestra lista, solo removió el primero.

# método agregar .apend()
serpLis5 = ["Boa", "Pitón", "Víbora Rayada"]
serpLis5.append("Cobra")
print(serpLis5)

# método de índice .index()
print(serpLis5.index("Cobra"))

serpLis5.sort()
print(serpLis5)

print("Ana añora estar con Emma y Carla".split())

print(sorted("Ana añora estar con Emma y Carla".split(), key=str.lower))

# Compartimos contigo una lista de otros métodos que puedes probar para experimentar con los resultados.
#
# .clear(): elimina todos los elementos de la lista.
# .copy(): arroja una copia de la lista.
# .count(): arroja el número de elementos con el valor indicado.
# .extend(): añade los elementos de una lista (o cualquier iterador) al final de la lista actual.
# .insert(): añade un elemento en la posición que se indica.
# .pop(): elimina el elemento de la posición que se indica.
# .reverse(): invierte el orden de la lista.
