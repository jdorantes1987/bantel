import pandas as pd

pagos = pd.read_excel("./varios/RepFormatoPago.xlsx")

print('REORDENA las columnas')
pagos = pagos[['fecha', 'co_prov', 'prov_des', 'rif', 'nit', 'telefonos',
       'fax', 'direc1', 'dir_entrega', 'cob_num', 'co_mone', 'descrip',
       'reng_doc', 'co_tipo_doc', 'nro_doc', 'nro_fact', 'mont_cob',
       'forma_pag', 'num_doc', 'num_cta', 'fecha_che', 'mont_doc', 'codigo',
       'descripcion', 'co_ban', 'des_ban', 'tipo_mov','numero']]
print(pagos)

print('\n' * 2)
print('Columnas reordenadas')
print(pagos.columns)


print('\n' * 2)
print('Ordena por una columna en especifico')
ordenadoPorColumna = pagos.sort_values(by='prov_des', ascending=True)
print(ordenadoPorColumna['prov_des'])

print('\n' * 2)
print('Ordena por multiples columnas')
ordenado_Mult_Columnas = pagos.sort_values(by=['prov_des', 'reng_doc'], ascending=True)
print(ordenado_Mult_Columnas['prov_des'])
