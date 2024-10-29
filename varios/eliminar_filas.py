import pandas as pd
import numpy as np

#Lee un archivo .xlsx
pagos = pd.read_excel("RepFormatoPago.xlsx")

print('\n' * 2)
print('Elimina las filas de una columna en especifico que contengan valores vacios')
print('\n' * 1)
print('Data Antes del reemplazo')
primeros_3_registros=pagos['mont_cob'].iloc[0:3]
print(primeros_3_registros)

print('\n' * 2)
print('Data despues del reemplazo')
registros_sin_vacios=primeros_3_registros.dropna(how='any', inplace=False)
print(registros_sin_vacios)
