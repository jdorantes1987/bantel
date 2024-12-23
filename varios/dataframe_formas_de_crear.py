import pandas as pd

data7 = [10, 20, 30, 40, 50, 60]

print(
    "\n" * 2, "Crea DataFrame con el nombre de la columna se proporciona explícitamente"
)

df9 = pd.DataFrame(data7, columns=["Numbers"])

print(df9)


print("\n" * 2, "Crea DataFrame a partir de listas de listas.")

data2 = [["tom", 10], ["nick", 15], ["juli", 14]]

df8 = pd.DataFrame(data2, columns=["Name", "Age"])

print(df8)


print("\n" * 2, "Crea DataFrame a partir de dict of array/lists")

data3 = {"Name": ["Tom", "nick", "krish", "jack"], "Age": [20, 21, 19, 18]}

df3 = pd.DataFrame(data3)

print(df3)


print("\n" * 2, "Crea DataFrame probando explícitamente la etiqueta de índice")

data4 = {"Name": ["Tom", "Jack", "nick", "juli"], "marks": [99, 98, 95, 90]}

df4 = pd.DataFrame(data4, index=["rank1", "rank2", "rank3", "rank4"])

print(df4)


print("\n" * 2, "Crea un marco de datos a partir de una lista de dictados")

data5 = [{"a": 1, "b": 2, "c": 3}, {"a": 10, "b": 20, "c": 30}]

df5 = pd.DataFrame(data5)

print(df5)


print("\n" * 2, "crea DataFrame pasando listas de diccionarios e índices de fila")

data6 = [{"b": 2, "c": 3}, {"a": 10, "b": 20, "c": 30}]

# Crea DataFrame pasando
# Listas de diccionarios e índice de filas.
df6 = pd.DataFrame(data6, index=["first", "second"])
print(df6)


print(
    "\n" * 2,
    "Crea DataFrame a partir de listas de diccionarios tanto con índice de fila como con índice de columna.",
)
data7 = [{"a": 1, "b": 2}, {"a": 5, "b": 10, "c": 20}]

# Con índices de dos columnas, valores iguales
# como teclas de diccionario
df7 = pd.DataFrame(data7, index=["first", "second"], columns=["a", "b"])

# Con índices de dos columnas con
# un índice con otro nombre
df8 = pd.DataFrame(data7, index=["first", "second"], columns=["a", "b1"])

# imprimir para el primer marco de datos
print(df7, "\n")

# Imprimir para el segundo DataFrame.
print(df8)


print("\n" * 2, "Crea DataFrame usando la función zip()")

# List1
Name = ["tom", "krish", "nick", "juli"]

# List2
Age = [25, 30, 26, 22]

# obtener la lista de tuplas de dos listas.
# y fusionarlos usando zip().
print("list_of_tuples")
list_of_tuples = list(zip(Name, Age))


# Convertir listas de tuplas en
# Marco de datos de pandas.
df9 = pd.DataFrame(list_of_tuples, columns=["Name", "Age"])

print(df9)


print("\n" * 2, "crear marcos de datos a partir de series")
d = pd.Series([10, 20, 30, 40])

df10 = pd.DataFrame(d)

print(df10)

ser1 = pd.Series(["Jackson", "Jhoan", "Alejandro"], index=[1, 2, 3])
ser2 = pd.Series(["programador", "IT", "Lenguaje"], index=[1, 2, 3])
ser3 = pd.Series([35, 34, 30], index=[1, 2, 3])

o_dict = {"nombres": ser1, "Trabajo": ser2, "Edad": ser3}


df_d = pd.DataFrame(o_dict, index=[1, 2, 3])
print(df_d)

# Agregar nueva fila al dataframe
df_d.loc[4] = ["Maite", "Costurera", 49]
print("\n" * 1, df_d)

print("\n" * 2, "crear tramas de datos a partir del diccionario de series.")

# Initialize data to Dicts of series.
d2 = {
    "one": pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"]),
    "two": pd.Series([100, 200, 300, 400], index=["a", "b", "c", "d"]),
}

# creates Dataframe.
df11 = pd.DataFrame(d2)

print(df11)

a_dict = {
    "Nombres": ["Jackson", "Mirtha", "Samira", "Mafer"],
    "Apellidos": ["Dorantes", "Graterol", "Dorantes", "Alarcon"],
    "Cedula": ["18329114", "15152791", "32018007", "no la sé"],
}
df_Dict = pd.DataFrame(a_dict, index=["Padre", "Esposa", "Hija", "Hija"])
print(df_Dict)
print(df_Dict.columns)
print(type(df_Dict.values))


colnames = ["Name", "Time", "Course"]
df = pd.DataFrame(
    [["Jay", 10, "B.Tech"], ["Raj", 12, "BBA"], ["Jack", 11, "B.Sc"]], columns=colnames
)

# Establecer varias columnas como indice
df.set_index(["Name", "Course"], inplace=True)
print(df)
# Acceder a los indices mediante la función loc
print(df.loc[("Jack", "B.Sc")])
