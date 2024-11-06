from os import getenv
from numpy import where
from pandas import merge_asof
from accesos.datos_profit import datos_profit
from accesos.files_excel import datos_estadisticas_tasas as f_est_bcv


object_data =  datos_profit(host=getenv("HOST_PRODUCCION_PROFIT"), 
                            data_base_admin=getenv("DB_NAME_IZQUIERDA_PROFIT"), 
                            data_base_cont='TBANTEL_C')

cxc_clientes = object_data.rep_cobros_x_cliente()
#cxc_clientes = cxc_clientes[(cxc_clientes['fecha_cob'] >= '20240901') & (cxc_clientes['fecha_cob'] <= '20241031')]
cxc_clientes['es_efectivo'] = where(cxc_clientes['forma_pag'] == 'EF', True, False)
cxc_clientes['cod_instr'] = where(cxc_clientes['co_ban'].isnull() , cxc_clientes['cod_caja'], cxc_clientes['co_ban'])
cxc_clientes = cxc_clientes.sort_values(by=['fecha_che'], 
                                        ascending=[True])  # se debe ordenar el df para poder conbinar

tasas_bcv = f_est_bcv()[['fecha', 'venta_ask2']] # archivo BCV
tasas_bcv.rename(columns={'fecha': 'fecha2'}, 
                 inplace=True)

tasas_bcv = tasas_bcv.sort_values(by=['fecha2'], 
                                  ascending=[True])  # se debe ordenar el df para poder conbinar

merge_data = merge_asof(cxc_clientes, tasas_bcv, 
                        left_on='fecha_che', 
                        right_on='fecha2', 
                        direction="nearest")  # Combinar por aproximación

merge_data['mont_doc_bs'] = round(merge_data['mont_doc'] * merge_data['venta_ask2'], 
                                  ndigits=2)

set_ult_cobros = set(merge_data.groupby(['co_cli', 
                                         'cli_des'], 
                                        sort=False, 
                                        as_index=False)[['cob_num']].max()['cob_num'])

merge_data = merge_data[merge_data['cob_num'].isin(set_ult_cobros)][['co_cli', 
                                                                     'cli_des', 
                                                                     'cob_num', 
                                                                     'fecha_cob', 
                                                                     'fecha_che', 
                                                                     'forma_pag', 
                                                                     'co_ban', 
                                                                     'cod_caja', 
                                                                     'mont_doc', 
                                                                     'mont_doc_bs', 
                                                                     'es_efectivo']].reset_index(drop=True)
merge_data.to_excel('rep_cobros_x_cliente Izquierda.xlsx')
