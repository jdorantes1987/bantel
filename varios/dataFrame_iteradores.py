import pandas as pd

print('\n' * 2, 'Usar el atributo de índice del marco de datos.')
# Definir un diccionario que contenga datos de estudiantes
data3 = {'Name': ['Jackson', 'Amit', 'Aishwarya', 'Priyanka'],
         'Age': [21, 19, 20, 18],
         'Carrera': ['Math', 'Commerce', 'Arts', 'Biology'],
         'Percentage': [88, 92, 95, 70]}

# Convert the dictionary into DataFrame
df1 = pd.DataFrame(data3)
print("Marco del Dataframe :\n", df1)

print("\nIterando sobre filas usando el atributo de índice :\n")
# iterar a través de cada fila y seleccionar
# Columnas 'Nombre' y 'Transmisión' respectivamente.
for ind in df1.index:
    print(df1['Name'][ind], df1['Carrera'][ind], sep='->')

print('\n' * 2, 'Usar la función loc[] del Dataframe.')
# Definir un diccionario que contenga datos de estudiantes
data2 = {'Name': ['Jakson', 'Amit', 'Aishwarya', 'Priyanka'],
         'Age': [21, 19, 20, 18],
         'Stream': ['Math', 'Commerce', 'Arts', 'Biology'],
         'Percentage': [100, 95, 95, 95]}

# Convertir el diccionario en DataFrame
df2 = pd.DataFrame(data2)
print(df2)
print('\nUnicos', df2[~df2['Percentage'].duplicated(
    keep=False)])  # keep=False permite identificar todos los duplicados, ~ niega los valores boleanos.
print('\nDuplicados', df2[df2['Percentage'].duplicated(
    keep=False)])  # keep=False permite identificar todos los duplicados, tiene varias opciones, leer documentación.
print("\nMarco del Dataframe :", df2)
print("\nIterando sobre filas usando la función loc :\n")

# iterar a través de cada fila
# Columnas 'Nombre' y 'Edad' respectivamente.
for i in range(len(df2)):
    print(df2.loc[i, "Name"], df2.loc[i, "Age"], sep='->')

print('\n' * 2, 'Usar la función iloc[] del DataFrame.')
# Define a dictionary containing students data
data3 = {'Name': ['Ankit', 'Amit', 'Aishwarya', 'Priyanka'],
         'Age': [21, 19, 20, 18],
         'Stream': ['Math', 'Commerce', 'Arts', 'Biology'],
         'Percentage': [88, 92, 95, 70]}

# Convertir el diccionario en DataFrame
df3 = pd.DataFrame(data3, columns=['Name', 'Age', 'Stream', 'Percentage'])

print("marco del Dataframe :\n", df3)
print("\nIterando sobre filas usando la función iloc :\n")
# iterar a través de cada fila y seleccionar
# 0ª y 2ª columna de índice respectivamente.
for i in range(len(df3)):
    print(df3.iloc[i, 0], df3.iloc[i, 2], sep='->')

print('\n' * 2, 'Usar el método iterrows() del marco de datos.')

# Define a dictionary containing students data
data4 = {'Name': ['Ankit', 'Amit', 'Aishwarya', 'Priyanka'],
         'Age': [21, 19, 20, 18],
         'Stream': ['Math', 'Commerce', 'Arts', 'Biology'],
         'Percentage': [88, 92, 95, 70]}

# Convert the dictionary into DataFrame
df4 = pd.DataFrame(data4, columns=['Name', 'Age', 'Stream', 'Percentage'])

print("marco del Dataframe :\n", df4)
print("\nIterando sobre filas usando el método iterrows():\n")
# iterar a través de cada fila y selecciona
# Columnas 'Nombre' y 'Edad' respectivamente.
for index, row in df4.iterrows():
    print(row.index, row["Name"], row["Age"], sep='->')

print('\n' * 2, 'Usar el método itertuples() del marco de datos.')
# Definir un diccionario que contenga datos de estudiantes
data5 = {'Name': ['Ankit', 'Amit', 'Aishwarya', 'Priyanka'],
         'Age': [21, 19, 20, 18],
         'Stream': ['Math', 'Commerce', 'Arts', 'Biology'],
         'Percentage': [88, 92, 95, 70]}

# Convertir el diccionario en DataFrame
df5 = pd.DataFrame(data5, columns=['Name', 'Age', 'Stream', 'Percentage'])

print("Marco del Dataframe :\n", df5)
print("\nIterando sobre filas usando el método itertuples() :\n")

# iterar a través de cada fila y seleccionar
# Columnas 'Nombre' y 'Porcentaje' respectivamente.
for row in df5.itertuples(index=True, name='Pandas'):
    print(getattr(row, "Name"), getattr(row, "Percentage"), sep='->')

print('\n' * 2, 'Usar el método apply() del marco de datos.')
# Define a dictionary containing students data
data6 = {'Name': ['Ankit', 'Amit', 'Aishwarya', 'Priyanka'],
         'Age': [21, 19, 20, 18],
         'Stream': ['Math', 'Commerce', 'Arts', 'Biology'],
         'Percentage': [88, 92, 95, 70]}

# Convertir el diccionario en DataFrame
df6 = pd.DataFrame(data6, columns=['Name', 'Age', 'Stream', 'Percentage'])

print("Marco del Dataframe :\n", df6)
print("\nIterando sobre filas usando la función de aplicación :\n")

# iterar a través de cada fila y concatenar
# Columnas 'Nombre' y 'Porcentaje' respectivamente.
df6['prueba'] = df6.apply(lambda df_row: df_row["Name"] + " " + str(df_row["Percentage"]), axis=1)
print(df6)
