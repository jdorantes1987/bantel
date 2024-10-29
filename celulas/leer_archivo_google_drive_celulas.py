import datetime
import urllib.request
import pandas as pd
from pandas import to_datetime
# ----------------------------------------------------------------------------------------------------------------------
ruta = "https://onedrive.live.com/download?resid=4B273DC2C3014B9E%2119214&authkey=!ABmYCecJnODTBkI&em=2"
file_name, headers = urllib.request.urlretrieve(ruta)
# file_name = 'F:/Registro Ofrendas_Python.xlsx'
today = datetime.datetime.now()
df1 = pd.read_excel(file_name, sheet_name="H_Celulas")
df2 = pd.read_excel(file_name, sheet_name="T_Celulas")
df3 = pd.read_excel(file_name, sheet_name="T_Codigos")
df4 = pd.read_excel(file_name, sheet_name="T_Sub_Codigos")
# ----------------------------------------------------------------------------------------------------------------------
#  FILTROS
celulas_historico = df1[df1['FECHA_CELULA'].notnull()] # Filtra los valores no nulos
celulas = df2[df2['T_CELULA_ESTATUS'] == 'ACTIVA'].copy()  # Filtra los codigos activos de cada celula
celulas['T_CELULA_DIRECCION'] = celulas['T_CELULA_DIRECCION'].str[:50]
codigos = df3[df3['T_COD_ESTATUS'] == 'ACTIVO']  # Filtra los codigos activos
sub_codigos = df4[df4['T_SUB_COD_ESTATUS'] == 'ACTIVO']  # Filtra los sub-codigos activos

# UNION ENTRE TABLAS
# Union tabla Historico de celulas con tabla Celulas
merg1 = pd.merge(celulas_historico, celulas, left_on='COD_CELULA', right_on='T_CELULA_COD')
# Union tabla Historico de celulas con tabla Redes
merg2 = pd.merge(merg1, codigos, left_on='T_CELULA_COD_RED', right_on='T_COD_CODIGO_RED')
# Union tabla Historico de celulas con tabla Sub Redes
merg3 = pd.merge(merg2, sub_codigos, left_on='T_CELULA_COD', right_on='T_SUB_COD_COD_CELULA')
merg3['DIAS_EN_ENTREGAR'] = (merg3['FECHA_RECIBIDO'] - merg3["FECHA_CELULA"]).dt.days
# print(merg3.info())
# ----------------------------------------------------------------------------------------------------------------------
# REPORTES
# ->CANTIDAD DE CELULAS ACTIVAS
print('\n' * 2, '>Cantidad de celulas activas por código y sub-código')
n_celulas = merg3.groupby(['T_COD_CODIGO_RED',
                           'T_SUB_SUB_COD_RED',
                           'COD_CELULA',
                           'T_SUB_COD_APELLIDO_LIDERES',
                           'T_CELULA_DIRECCION'])[['ASISTENCIA']].mean()
n_celulas['ASISTENCIA'] = n_celulas['ASISTENCIA'].apply('{:,.0f}'.format)
print(n_celulas)
# ----------------------------------------------------------------------------------------------------------------------
# ->CANTIDAD DE CASAS DE BENDICIÓN POR CODIGOS Y SUB-CODIGOS
print('\n' * 2, '>Cantidad de celulas activas por Códigos', '\n' * 1)
celulas_x_matrim = merg3.groupby(['T_COD_CODIGO_RED', 'T_COD_MATRIMONIO', 'T_CELULA_DIRECCION']).size()
print(celulas_x_matrim.groupby(level=[0, 1]).count())
celulas_x_matrim_total = celulas_x_matrim.groupby(level=[0, 1]).count().sum()
print('Total casas de bendición por código:', celulas_x_matrim_total, '\n' * 2)
# ----------------------------------------------------------------------------------------------------------------------
# ->CANTIDAD DE CASAS DE BENDICIÓN POR CODIGOS Y SUB-CODIGOS
print('Total sobres por entregar:', '\n' * 2)
sobres_x_entregar = merg3[merg3['SOBRE_ENTREG'] == 'NO']
t_monto_x_redes = sobres_x_entregar.groupby(['T_COD_CODIGO_RED',
                                             'T_COD_MATRIMONIO'])[['MONTO_BS', 'MONTO_USD']].sum().reset_index()
t_monto_x_redes.loc['Total'] = t_monto_x_redes[['MONTO_BS', 'MONTO_USD']].sum()
print(t_monto_x_redes.fillna('->').to_string())
# ----------------------------------------------------------------------------------------------------------------------
# ->ULTIMA ACTIVIDAD DEL MES
celula_con_activ = merg3[merg3['ASISTENCIA'] > 0]
grouped = celula_con_activ.groupby([celula_con_activ['T_COD_CODIGO_RED'],
                                   celula_con_activ['T_COD_MATRIMONIO'],
                                   celula_con_activ['T_CELULA_COD'],
                                   celula_con_activ['T_CELULA_DIRECCION']])
last_day_of_month = grouped['FECHA_CELULA'].max().reset_index()
last_day_of_month["DIAS_TRANSC"] = (today - last_day_of_month['FECHA_CELULA']).dt.days  # Dias transcurridos entre la ultima fecha al dia de hoy
print('\n' * 1, 'Última actividad del mes:')
grouped2 = last_day_of_month.groupby(['T_COD_CODIGO_RED',
                                      'T_COD_MATRIMONIO',
                                      'T_CELULA_COD',
                                      'T_CELULA_DIRECCION'])[['FECHA_CELULA', 'DIAS_TRANSC']].max()
print(grouped2.to_string())
# ----------------------------------------------------------------------------------------------------------------------
# -> TOP 10 DE ASISTENCIA A CASAS DE BENDICIÓN
print('\n' * 1, 'Top 10 de ASISTENCIA a las Casas de Bendición')
top_asistecia_prom = pd.DataFrame(n_celulas.reset_index())
top_asistecia_prom['ASISTENCIA'] = top_asistecia_prom['ASISTENCIA'].astype('int64')
print('\n' * 1, top_asistecia_prom.nlargest(n=10, columns=['ASISTENCIA'], keep='all').reset_index(drop=True).to_string())
# EXPORTAR A EXCEL
merg3.to_excel('Reporte Detallado de Casas de Bendicion.xlsx')
