from pandas import to_datetime
from pandas import merge
from varios.utilidades import search_df
from datetime import date
from accesos.datos import clientes
from accesos.datos import facturacion_x_cliente as datos_fact_x_clientes
from facturas import diccionario_facturacion_total_por_anio
from re import findall

hoy = date.today()
def search_clients(string_s, **kwargs):
    df = clientes()
    df['co_cli'] = df['co_cli'].str.strip()
    df['fe_us_in'] = to_datetime(df['fe_us_in']).dt.normalize()
    resul = search_df(string_s, df)[['co_cli', 'cli_des', 'rif', 'dir_ent2', 'telefonos', 'respons', 'direc1', 'fe_us_in', 'campo3']]
    if acortar_datos := kwargs.get('resumir_datos', False):
        resul['cli_des'] = resul['cli_des'].str[:30]  # Extrae los primeros 40 caracteres de la izquierda
        resul['direc1'] = resul['direc1'].str[:20]  # Extrae los primeros 40 caracteres de la izquierda
    return resul


def get_top_fact_x_cliente(top=10, anio=2023):
    print(f"\nTOP {top}", "facturación por cliente")
    l_col = ['anio', 'co_cli', 'cli_des', 'monto_base_item', 'monto_base_item$']
    data_fact = datos_fact_x_clientes(anio=anio)
    clients = clientes()
    result = data_fact.nlargest(n=top, columns=['monto_base_item', 'monto_base_item$'], keep='all').reset_index(drop=True)
    result['co_cli'] = result['co_cli'].str.strip()  # Elimina o suprime los espacios de más
    join1 = merge(result, clients, how='left', left_on='co_cli', right_on='co_cli')
    result = join1[l_col].copy()
    result['Porcentaje'] = result['monto_base_item$'].apply(lambda x: x / result['monto_base_item$'].sum()) 
    result['Porcentaje'] = result['Porcentaje'].apply('{:.2%}'.format)
    vtas_total_anio = diccionario_facturacion_total_por_anio(anio=anio, conv_usd=False) 
    vtas_top_usd = result['monto_base_item$'].sum()
    vtas_top_bs = result['monto_base_item'].sum()
    print('Total Bs.:', round(vtas_top_bs, ndigits=2))
    print('Total $:', round(vtas_top_usd, ndigits=2))
    porcent = round(vtas_top_bs / vtas_total_anio, ndigits=7)
    print(f"% sobre total facturación {anio}:","{:.7%}".format(porcent))
    return result

def new_cod_client():
    clients = clientes()[['co_cli']]
    patron = r"[A-Za-z]{2}\d{1,3}$"  # Patron para ubicar los clientes NO AGRUPADOS ejemplo: CL95 sin el guion
    clientes_filtro = clients[clients['co_cli'].str.contains(patron, regex=True)].copy() # Se debe especificar que se está trabajando con expresiones regulares
    clientes_filtro['num_cod_client'] = clientes_filtro.apply(lambda x: findall('[0-9.]+', x['co_cli'])[0], axis=1) # Extrae los números contenidos en la cadena o string
    clientes_filtro['num_cod_client']=clientes_filtro['num_cod_client'].astype("int64") 
    id_new_client= clientes_filtro['num_cod_client'].max() + 1
    return f"CL{id_new_client}"

# Devuelve la suma o conteo (cuenta) de elementos nulos, vacios o faltantes  en cada columna del dataframe.
# print(clientes().isna().sum())