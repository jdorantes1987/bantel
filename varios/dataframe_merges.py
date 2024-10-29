from pandas import read_excel
from pandas import merge_asof
from accesos.files_excel import p_data_estadisticas_bcv as p_est_bcv

ruta = './varios/RepFormatoPago.xlsx'
l_campos = ['cob_num', 'fecha', 'co_prov', 'prov_des', 'descrip', 'co_tipo_doc', 'nro_doc', 'nro_fact', 'mont_doc', 'monto_usd']
l_campos_sin_espacios = ['cob_num', 'co_prov', 'co_tipo_doc', 'nro_doc']
l_campos_a_recortar = ['prov_des', 'descrip']
ruta2 = p_est_bcv  # ruta relativa, regresa a la carpeta anterior
pagos = read_excel(ruta)
tasas_cambio = read_excel(ruta2)
pagos_s = pagos.sort_values(by=['fecha'], ascending=[True])
tasas_cambio_s = tasas_cambio.sort_values(by=['fecha'], ascending=[True])
join1 = merge_asof(pagos_s, tasas_cambio_s, left_on='fecha', right_on='fecha',  direction="nearest")  # Combinar por aproximación
merge_data = join1.sort_values(by=['cob_num', 'reng_doc'], ascending=[True, True])
merge_data[l_campos_sin_espacios] = merge_data[l_campos_sin_espacios].apply(lambda x: x[l_campos_sin_espacios].str.strip(), axis=1)
merge_data[l_campos_a_recortar] = merge_data[l_campos_a_recortar].apply(lambda x: x[l_campos_a_recortar].str[:40], axis=1)
merge_data['monto_usd'] = merge_data.apply(lambda x: round(x['mont_doc'] / x['venta_ask2'], ndigits=2), axis=1)
print(merge_data[l_campos].reset_index(drop=True).to_string())
print('Cantidad de nombres únicos:', len(merge_data['prov_des'].unique().tolist()))  # lista de unicos



