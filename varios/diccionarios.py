'''
 Los diccionarios en Python son una estructura de datos
 que permite almacenar su contenido en forma de llave y valor.
'''
d1 = {
  "Nombre": "Sara",
  "Edad": 27,
  "Documento": 1003882
}
print(d1)

d2 = dict([('Nombre', 'Sara'), ('Edad', 27), ('Documento', 1003882)])
print(d2)

d3 = dict(Nombre='Sara',
          Edad=27,
          Documento=1003882)
print(d3)

print(d1['Nombre'])     #Sara
print(d1.get('Nombre')) #Sara

d1['Nombre'] = "Laura"
print(d1)
#{'Nombre': Laura', 'Edad': 27, 'Documento': 1003882}

d1['Direccion'] = "Calle 123"
print(d1)

# Imprime los key del diccionario
for x in d1:
    print(x)

# Impre los value del diccionario
for x in d1:
    print(d1[x])

# Imprime los key y value del diccionario
for x, y in d1.items():
    print(x, y, sep=':')

anidado1 = {"a": 1, "b": 2}
anidado2 = {"a": 1, "b": 2}
d = {
  "anidado1" : anidado1,
  "anidado2" : anidado2
}
print(d)

'''
 clear()
 El método clear() elimina todo el contenido del diccionario.
'''
d = {'a': 1, 'b': 2}
d.clear()

'''
 get(<key>[,<default>])
 El método get() nos permite consultar el value para un key determinado.
 El segundo parámetro es opcional, y en el caso de proporcionarlo es el valor a devolver si no se encuentra la key.
'''
d = {'a': 1, 'b': 2}
print(d.get('b')) #1
print(d.get('z', 'No encontrado')) #No encontrado

'''
 items()
 El método items() devuelve una lista con los keys y values del diccionario.
 Si se convierte en list se puede indexar como si de una lista normal se tratase,
 siendo los primeros elementos las key y los segundos los value.
'''
d = {'a': 1, 'b': 2}
it = d.items()
print(it)             #dict_items([('a', 1), ('b', 2)])
print(list(it))       #[('a', 1), ('b', 2)]
print(list(it)[0][0]) #a

# keys()
# El método keys() devuelve una lista con todas las keys del diccionario.
d = {'a': 1, 'b': 2}
k = d.keys()
print(k)       #dict_keys(['a', 'b'])
print(list(k)) #['a', 'b']

d = {'a': 1, 'b': 2}
print(list(d.values())) #[1, 2]
'''
 pop(<key>[,<default>])
 El método pop() busca y elimina la key que se pasa como parámetro y devuelve su valor asociado.
 Daría un error si se intenta eliminar una key que no existe.
'''
d = {'a': 1, 'b': 2}
d.pop('a')
print(d) #{'b': 2}

# También se puede pasar un segundo parámetro que es el valor a devolver
# si la key no se ha encontrado. En este caso si no se encuentra no habría error.

d = {'a': 1, 'b': 2}
d.pop('c', -1)
print(d) #{'a': 1, 'b': 2}

# El método popitem() elimina de manera aleatoria un elemento del diccionario.
d = {'a': 1, 'c': 3, 'b': 2}
d.popitem()
print(d)
#{'a': 1}
'''
 El método update() se llama sobre un diccionario y tiene como entrada otro diccionario.
 Los value son actualizados y si alguna key del nuevo diccionario no esta, es añadida.
 update(<obj>)
'''
d1 = {'a': 1, 'b': 2}
d2 = {'a': 0, 'd': 400}
d1.update(d2)
print(d1)
#{'a': 0, 'b': 2, 'd': 400}

f_usd_year = {'2023': ['2_1_2d23_smc.xls', '2_1_2c23_smc.xls', '2_1_2b23_smc.xls', '2_1_2a23_smc.xls'],
              '2022': ['2_1_2d22_smc.xls', '2_1_2c22_smc.xls', '2_1_2b22_smc.xls', '2_1_2a22_smc.xls'],
              '2021': ['2_1_2d21_smc.xls', '2_1_2c21_smc.xls', '2_1_2b21_smc.xls', '2_1_2a21_smc.xls'],
              '2020': ['2_1_2d20_smc.xls', '2_1_2c20_smc.xls', '2_1_2b20_smc.xls', '2_1_2a20_smc.xls']
              }


f_usd_year['2023']=["prueba"]

# Imprime los value del diccionario
for x in f_usd_year:
    print(f_usd_year[x][0])


l_files = list(f_usd_year.values())
l_files_join = [x for y in l_files for x in y]  # Unifica todas las listas del diccionario
print(len(l_files_join))
for elem in range(len(l_files_join)):
    print(l_files_join[elem])
