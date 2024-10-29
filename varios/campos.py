import pandas as pd

pagos = pd.read_excel("RepFormatoPago.xlsx")

print('\n' * 2, 'Convertir campos en mayúsculas')
camposInMayus = pagos.rename(columns=str.upper)
print(camposInMayus)

print('\n' * 2, 'Agregue un prefijo a los nombres de los campos')
campos_con_prefi = pagos.add_prefix('pgos_')
print(campos_con_prefi)

print('\n' * 2, 'Agregue un sufijo a los nombres de los campos')
campos_con_sufi = pagos.add_suffix('_X')
print(campos_con_sufi)

camposConGuinesBajos = pagos.columns.str.lower().str.replace('[^0-9a-zA-Z]+', '_', regex=True)
print(camposConGuinesBajos)