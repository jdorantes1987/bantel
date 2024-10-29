import urllib.request
import pandas as pd

ruta = "https://docs.google.com/spreadsheets/d/1BHI0mjidySPkKXD5Xz-c3JMI1yotG0Yt/export?format=xlsx"
file_name, headers = urllib.request.urlretrieve(ruta)
df = pd.concat(pd.read_excel(file_name, sheet_name=['ENCUENTRISTAS', 'SERVIDORES']), ignore_index=True)
df = df[df['NOMBRE'].notnull()]  # FILTRO DE NO NULOS
df2 = df.reset_index(drop=True)
# Cambia el tipo de dato de la columna
df2[['EDAD', 'TELÉFONO']] = df2[['EDAD', 'TELÉFONO']].astype('Int64')
df2.to_excel('Encuentro data.xlsx')
print('Participantes por:')
p_x_tipo = df.groupby(['TIPO'])[['NOMBRE']].count().reset_index()
p_x_tipo.rename(columns={'NOMBRE': 'CANTIDAD'}, inplace=True)
p_x_tipo.loc['T'] = ['TOTAL',  p_x_tipo['CANTIDAD'].sum()]
print(p_x_tipo, '\n' * 1)

print('Participantes por:')
p_x_tipo = df.groupby(['SEXO', 'TIPO'])[['NOMBRE']].count().reset_index()
p_x_tipo.rename(columns={'NOMBRE': 'CANTIDAD'}, inplace=True)
p_x_tipo.loc['T'] = ['TOTAL', '', p_x_tipo['CANTIDAD'].sum()]
print(p_x_tipo, '\n' * 1)

print('Abonos:')
p_x_tipo = df.groupby(['SEXO', 'TIPO']).agg({'MONTO ABONADO': 'sum', 'MONTO X ABONAR': 'sum'}).reset_index()
p_x_tipo.loc['T'] = ['TOTAL', '', p_x_tipo['MONTO ABONADO'].sum(), p_x_tipo['MONTO X ABONAR'].sum()]
list_montos = ['MONTO ABONADO', 'MONTO X ABONAR']
p_x_tipo[list_montos] = p_x_tipo[list_montos].applymap('$ {:,.2f}'.format)
print(p_x_tipo, '\n' * 1)

campos_file = [['NOMBRE', 'TIPO', 'SEXO', 'RED', 'MONTO ABONADO', 'MONTO X ABONAR', 'ENVIADO POR'], ['TIPO', 'SEXO', 'RED'], [True, True, True]]
print('\n' * 1, 'Archivo de solventes generado!')
solv = df[(df['MONTO ABONADO'] >= 0.0) & (df['MONTO X ABONAR'] == 0.0)]
solv_l = solv[campos_file[0]]
solv_s = solv_l.sort_values(by=campos_file[1], ascending=campos_file[2]).reset_index(drop=True)
solv_s.to_excel('Encuentro solventes de pago.xlsx')

print('\n' * 1, 'Archivo abonos generado!')
abonos = df[(df['MONTO ABONADO'] > 0.0) & (df['MONTO X ABONAR'] != 0.0)]
abonos_l = abonos[campos_file[0]]
abonos_s = abonos_l.sort_values(by=campos_file[1], ascending=campos_file[2]).reset_index(drop=True)
abonos_s.to_excel('Encuentro abonos.xlsx')
print('\n' * 1, 'Archivo sin pago generado!')
s_pagos = df[(df['MONTO ABONADO'] == 0.0) & (df['MONTO X ABONAR'] < 0.0)]
s_pagos_l = s_pagos[campos_file[0]]
s_pagos_s = s_pagos_l.sort_values(by=campos_file[1], ascending=campos_file[2]).reset_index(drop=True)
s_pagos_s.to_excel('Encuentro sin pago.xlsx')
