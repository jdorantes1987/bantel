import pandas as pd

pagos = pd.read_excel("RepFormatoPago.xlsx")

print("IMPRIME los Datos del archivo")
print(pagos)

print("Imprime los NOMBRES de las COLUMNAS del archivo")
print(pagos.columns)

print("Imprime los VALORES de una COLUMNA")
print(pagos["co_prov"])

print("Imprime la CANTIDAD de [FILAS y COLUMNAS] del archivo")
print(pagos.shape)

print("Obtiene el TIPO DE DATOS de cada COLUMNAS")
tipo_datos_columnas = pagos.dtypes
print(tipo_datos_columnas)

print("Obtiene las COLUMNAS cuyo tipo de datos es ENTERO")
columnas_entero = pagos.select_dtypes(include="int64")
print(columnas_entero)

print("Obtiene el nombre de las columnas cuyo tipo de datos es string")
columnas_string = pagos.select_dtypes(include="object")
print(columnas_string.columns)

print("Obtiene las columnas cuyo tipo de datos es int64")
columnas_string = pagos.select_dtypes(include="int64")
print(columnas_string)

# FUNCION ILOC
print("Imprime las columnas ubicadas entre la 15 y 18")
cuatro_columnas = pagos.iloc[:, 14:18:1]
print(cuatro_columnas)
print("Imprime los nombres de las columnas ubicadas entre la 15 y 18")
print(cuatro_columnas.columns)


print("Imprime todas las columnas cuyo nombre comienza con num")
columnas_mont = pagos.iloc[:, pagos.columns.str.startswith("num")]
print(columnas_mont)

print(
    "\n" * 2,
    "Imprime la cantidad de valores no nulos, esto aplica tambien para los valores no nulos",
)
nulos_x_columnas = pagos.notnull().sum()
print(nulos_x_columnas)

print(
    "\n" * 2,
    "Separa los String de la columna en caracteres individuales, si se desea separar por palabras debe colocar un espacio como caracter separador",
)
seperar_cadena = pagos["prov_des"].str.split("", expand=True)
print(seperar_cadena)

print("\n" * 2, "Largo cantidad de caracteres")
largo_cadena = pagos["prov_des"].str.len()
print(largo_cadena)

print("\n" * 2, "Cadena de caracteres mas larga")
largo_cadena = pagos["prov_des"].str.len().max()
print(largo_cadena)
