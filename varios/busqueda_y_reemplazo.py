import numpy as np
import pandas as pd

# Lee un archivo .xlsx
pagos = pd.read_excel("RepFormatoPago.xlsx")

print("\n" * 2)
print(">Reemplazar valores en 0")
print("Data Antes del reemplazo")
print(pagos)

print("\n" * 2)
print(">Data despues del reemplazo")
sin_Ceros = pagos.replace(np.nan, 0)
print(sin_Ceros)

print("\n" * 2)
print('>Reemplazar valores en 0 con comando "fillna"')
print("Data Antes del reemplazo")
print(pagos)

print("\n" * 2)
print(">Rellena con ceros todos los datos que esten vacios")
sin_Ceros2 = pagos.fillna(0, inplace=False)
print(sin_Ceros2)

print("\n" * 2)
print(">Reemplaza el valor de una columna o varias columnas")
cambiar_descrip = pagos["prov_des"].replace(
    ["GLOBAL IT SYSTEM.C.A.", "EDC NETWORK COMUNICACIONES SCS"], ["*GLOBAL*", "*EDC*"]
)
print(cambiar_descrip)

print("\n" * 2)
print('>Busca y reempleza todas las cadenas que empiezan con la letra "A" ')
cambiar_por_A = pagos["prov_des"].replace([r"^A.*"], ["ANONIMO"], regex=True)
print(cambiar_por_A)

print("\n" * 2)
print('>Busca y reempleza todas los caracteres "A" por "O" ')
cambiar_A_por_O = pagos["prov_des"].str.replace("A", "O")
print(cambiar_A_por_O)
