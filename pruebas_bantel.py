from os import getenv
from numpy import where
from pandas import merge_asof, merge
from accesos.datos_profit import datos_profit
from accesos.files_excel import datos_estadisticas_tasas as f_est_bcv




object_data =  datos_profit(host=getenv("HOST_PRODUCCION_PROFIT"), 
                            data_base_admin=getenv("DB_NAME_DERECHA_PROFIT"), 
                            data_base_cont='TBANTEL_C')

cxc_clientes = object_data.rep_cobros_x_cliente()
cxc_clientes = cxc_clientes[cxc_clientes['mont_doc'] > 0]
cxc_clientes['es_efectivo'] = where(cxc_clientes['cod_caja'] == '002', True, False)
#cxc_clientes['es_efectivo'] = where(cxc_clientes['co_ban'] != '0108', True, False)
cxc_clientes['cod_instr'] = where(cxc_clientes['co_ban'].isnull() , cxc_clientes['cod_caja'], cxc_clientes['co_ban'])
cxc_clientes = cxc_clientes.sort_values(by=['fecha_che'], 
                                        ascending=[True])  # se debe ordenar el df para poder conbinar

tasas_bcv = f_est_bcv()[['fecha', 'venta_ask2']] # archivo BCV
tasas_bcv.rename(columns={'fecha': 'fecha2'}, 
                 inplace=True)

tasas_bcv = tasas_bcv.sort_values(by=['fecha2'], 
                                  ascending=[True])

merge_data = merge_asof(cxc_clientes, tasas_bcv, 
                        left_on='fecha_che', 
                        right_on='fecha2', 
                        direction="nearest")

merge_data['mont_doc_bs'] = round(merge_data['mont_doc'] / merge_data['venta_ask2'], 
                                  ndigits=2)
#merge_data['mont_doc_bs'] = round(merge_data['mont_doc'] * merge_data['venta_ask2'], 
#                                  ndigits=2)

set_ult_cobros = set(merge_data.groupby(['co_cli', 
                                         'cli_des'], 
                                        sort=False, 
                                        as_index=False)[['cob_num']].max()['cob_num'])

ultimo_cobro = merge_data[merge_data['cob_num'].isin(set_ult_cobros)]

ultimo_cobro = ultimo_cobro.groupby(['co_cli', 
                                     'cli_des', 
                                     'cob_num', 
                                     'fecha_cob', 
                                     'fecha_che', 
                                     'forma_pag', 
                                     'es_efectivo']).agg({'mont_doc':'sum', 'mont_doc_bs':'sum'}).reset_index()

facturas_ventas = object_data.resumen_facturas(fecha_ini='20241001', fecha_fin='20241031')
facturas_ventas = merge_asof(facturas_ventas, tasas_bcv, 
                        left_on='fec_emis', 
                        right_on='fecha2', 
                        direction="nearest")


facturas_ventas = facturas_ventas.groupby(['co_cli', 'cli_des', 'venta_ask2']).agg({'total_bruto':'sum', 'monto_desc_glob':'sum'}).reset_index()
facturas_ventas['total_neto'] = (facturas_ventas['total_bruto'] - facturas_ventas['monto_desc_glob'])
#facturas_ventas['total_neto_usd'] = facturas_ventas['total_bruto'] - facturas_ventas['monto_desc_glob']
facturas_ventas['total_neto_usd'] = round((facturas_ventas['total_bruto'] - facturas_ventas['monto_desc_glob']) / facturas_ventas['venta_ask2'], ndigits=2)
ingresos_con_ultimo_cobro = merge(facturas_ventas, ultimo_cobro, how='left')


ingresos_con_ultimo_cobro.to_excel('rep_cobros_x_cliente Derecha.xlsx')
