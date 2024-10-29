import urllib.request

import numpy
import xlrd
import pandas as pd
ruta = "https://docs.google.com/spreadsheets/d/1BHI0mjidySPkKXD5Xz-c3JMI1yotG0Yt/export?format=xlsx"
file_name, headers = urllib.request.urlretrieve(ruta)
df = pd.concat(pd.read_excel(file_name, sheet_name=['ENCUENTRISTAS', 'SERVIDORES', 'JOVENES']), ignore_index=True)
df = df[df['NOMBRE'].notnull()]  # FILTRO DE NO NULOS
df2 = df.reset_index(drop=True)
# Cambia el tipo de dato de la columna
df2['EDAD'] = df2['EDAD'].astype('Int64')
print(df2.to_string())


print('Participantes por:')
p_x_tipo = df.groupby(['TIPO'])[['NOMBRE']].count().reset_index()
p_x_tipo.rename(columns={'NOMBRE': 'CANTIDAD'}, inplace=True)
print(p_x_tipo, '\n' * 1)

print('Participantes por:')
p_x_tipo = df.groupby(['SEXO', 'TIPO'])[['NOMBRE']].count().reset_index()
p_x_tipo.rename(columns={'NOMBRE': 'CANTIDAD'}, inplace=True)
print(p_x_tipo, '\n' * 1)

print('Abonos:')
p_x_tipo = df.groupby(['SEXO', 'TIPO'])['MONTO ABONADO'].aggregate(['sum']).reset_index()
p_x_tipo.rename(columns={'NOMBRE': 'CANTIDAD'}, inplace=True)
p_x_tipo['sum'] = p_x_tipo['sum'].apply('$ {:,.2f}'.format)

print(p_x_tipo, '\n' * 1)