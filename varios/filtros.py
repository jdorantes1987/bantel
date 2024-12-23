import pandas as pd

pagos = pd.read_excel("./varios/RepFormatoPago.xlsx")

print('FILTRA la columna "num_cta" cuyos valores no sean nulos')
cta_no_vacias = pagos[pagos["num_cta"].notnull()]
print(cta_no_vacias["num_cta"])

print("\n" * 2, 'Filtrar dato por una columna "co_tipo_doc"')
docCompras_filtrado = pagos[pagos["co_tipo_doc"] == "FACT  "]
print(docCompras_filtrado["nro_doc"])

print(
    "\n" * 2,
    'Filtrar dato por una columna "co_tipo_doc" y busca cual es el ultimo registro',
)
docCompras_filtrado = pagos[pagos["co_tipo_doc"] == "FACT  "]
print(docCompras_filtrado["nro_doc"].tail().max())


print("\n" * 2, "Verifique los valores PG en la columna Posición")
# Creando el marco de datos con dictado de listas
df1 = pd.DataFrame(
    {
        "Name": ["Geeks", "Peter", "James", "Jack", "Lisa"],
        "Team": ["Boston", "Boston", "Boston", "Chele", "Barse"],
        "Position": ["PG", "PG", "UG", "PG", "UG"],
        "Number": [3, 4, 7, 11, 5],
        "Age": [33, 25, 34, 35, 28],
        "Height": ["6-2", "6-4", "5-9", "6-1", "5-8"],
        "Weight": [89, 79, 113, 78, 84],
        "College": ["MIT", "MIT", "MIT", "Stanford", "Stanford"],
        "Salary": [99999, 99994, 89999, 78889, 87779],
    },
    index=["ind1", "ind2", "ind3", "ind4", "ind5"],
)
print(df1, "\n")

print("Check PG values in Position column:\n")
df1 = df1["Position"].str.contains("PG")
print(df1)


print("\n" * 2, "Obtener las filas que cumplen la condicion")
df2 = pd.DataFrame(
    {
        "Name": ["Geeks", "Peter", "James", "Jack", "Lisa"],
        "Team": ["Boston", "Boston", "Boston", "Chele", "Barse"],
        "Position": ["PG", "PG", "UG", "PG", "UG"],
        "Number": [3, 4, 7, 11, 5],
        "Age": [33, 25, 34, 35, 28],
        "Height": ["6-2", "6-4", "5-9", "6-1", "5-8"],
        "Weight": [89, 79, 113, 78, 84],
        "College": ["MIT", "MIT", "MIT", "Stanford", "Stanford"],
        "Salary": [99999, 99994, 89999, 78889, 87779],
    },
    index=["ind1", "ind2", "ind3", "ind4", "ind5"],
)

df3 = df2[df2["Position"].str.contains("PG")]
print(df3)


print(
    "\n" * 2,
    "filtre todas las filas en las que Equipo contenga 'Boston' o Universidad contenga 'MIT'",
)
df4 = pd.DataFrame(
    {
        "Name": ["Geeks", "Peter", "James", "Jack", "Lisa"],
        "Team": ["Boston", "Boston", "Boston", "Chele", "Barse"],
        "Position": ["PG", "PG", "UG", "PG", "UG"],
        "Number": [3, 4, 7, 11, 5],
        "Age": [33, 25, 34, 35, 28],
        "Height": ["6-2", "6-4", "5-9", "6-1", "5-8"],
        "Weight": [89, 79, 113, 78, 84],
        "College": ["MIT", "MIT", "MIT", "Stanford", "Stanford"],
        "Salary": [99999, 99994, 89999, 78889, 87779],
    },
    index=["ind1", "ind2", "ind3", "ind4", "ind5"],
)

df5 = df4[df4["Team"].str.contains("Boston") | df4["College"].str.contains("MIT")]
print(df5)


print(
    "\n" * 2,
    "las filas de filtro que verifican el nombre del equipo contienen 'Boston' y la posición debe ser P'G'",
)
# haciendo marco de datos
df6 = pd.read_csv("https://media.geeksforgeeks.org/wp-content/uploads/nba.csv")

df7 = df6[df6["Team"].str.contains("Boston") & df6["Position"].str.contains("PG")]
print(df7)


print(
    "\n" * 2,
    "las filas de filtro que verifican que la posición contiene PG y la universidad debe contener como UC.",
)
# haciendo marco de datos
df8 = pd.read_csv("https://media.geeksforgeeks.org/wp-content/uploads/nba.csv")

df9 = df8[df8["Position"].str.contains("PG") & df8["College"].str.contains("UC")]
print(df9)
