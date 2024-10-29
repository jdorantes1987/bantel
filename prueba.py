from pandas import merge_asof
from pandas import read_excel
from accesos.files_excel import datos_estadisticas_tasas as f_est_bcv

ruta_file = 'C:/Users/jdorantes/Desktop/Auxiliar Caja Divisas 2022.xlsx'
df = read_excel(ruta_file, dtype={'Entrada_USD': float, 'Salida_USD': float, 'Entrada_BS': float, 'Salida_BS': float})
df_sort = df.sort_values(by=['fecha'], ascending=[True])  # se debe ordenar el df para poder conbinar
file_bcv = f_est_bcv()[['fecha', 'venta_ask2']] # archivo BCV
file_bcv.rename(columns={'fecha': 'fecha2'}, inplace=True)
tasas_cambio_s = file_bcv.sort_values(by=['fecha2'], ascending=[True])  # se debe ordenar el df para poder conbinar
merge_data = merge_asof(df_sort, tasas_cambio_s, left_on='fecha', right_on='fecha2', direction="nearest")  # Combinar por aproximación
merge_data['Entrada_BS_BCV'] = merge_data.apply(lambda x: x['Entrada_USD'] * x['venta_ask2'], axis=1)
merge_data['Salida_BS_BCV'] = merge_data.apply(lambda x: x['Salida_USD'] * x['venta_ask2'], axis=1)
# merge_data[['Entrada_USD', 'Salida_USD', 'Saldos_USD', 'Entrada_BS', 'Salida_BS', 'Saldo_BS']] = merge_data[['Entrada_USD', 'Salida_USD', 'Saldos_USD', 'Entrada_BS', 'Salida_BS', 'Saldo_BS']].apply(
#         lambda x: x[['Entrada_USD', 'Salida_USD', 'Saldos_USD', 'Entrada_BS', 'Salida_BS', 'Saldo_BS']].apply('{:,.2f}'.format), axis=1)  # Formato $ en varias columnas
merge_data.to_excel('Auxiliar Caja Divisas.xlsx')