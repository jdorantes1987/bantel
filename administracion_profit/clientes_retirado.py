from accesos.datos import factura_venta_con_su_detalle_en_usd
from accesos.datos import clientes
from pandas import to_datetime
from pandas import merge
# import seaborn as sns 
from seaborn import barplot
from matplotlib import pyplot as plt 
from matplotlib.text import OffsetFrom
import numpy as np
import datetime

def clientes_retirados():
    df = factura_venta_con_su_detalle_en_usd(anio='all')
    df2 = df[df['co_tipo_doc'] == 'FACT']
    ult_fact_df = df2.groupby(['co_cli']).agg({'fec_reg': 'max', 'anio': 'count', 'doc_num': 'max'}).reset_index()
    group_fact_df = df2.groupby(['doc_num']).agg({'monto_base_item$': 'sum'}).reset_index()

    today = to_datetime(datetime.datetime.now().date())
    ult_fact_df['fecha_final'] = today
    # devuelve la cantidad de meses transcurridos entre dos fecha
    ult_fact_df['meses_sin_fact'] = ult_fact_df['fecha_final'].dt.to_period('M').astype('int64') - ult_fact_df['fec_reg'].dt.to_period('M').astype('int64')
    # filtra aquellas facturas cuyos meses sin facturas estén entre 3 y 12 mese y por lo menos se le emitieron dos facturas
    segm_mes = ult_fact_df[(ult_fact_df['meses_sin_fact'] >= 1) & (ult_fact_df['meses_sin_fact'] <= 12) & (ult_fact_df['anio'] > 1)]
    merge_fact = merge(segm_mes, group_fact_df, how='left', on='doc_num')
    cliente = clientes()[['co_cli', 'cli_des', 'inactivo']]
    merge_fact2 = merge(merge_fact, cliente, how='left', on='co_cli')[['co_cli', 'cli_des', 'fec_reg', 'anio', 'doc_num', 'fecha_final', 'meses_sin_fact',
       'monto_base_item$', 'inactivo']]
    clientes_inactivos = merge_fact2[merge_fact2['inactivo'] == True].copy()
    clientes_inactivos['monto_base_item$'] = round(clientes_inactivos['monto_base_item$'], 2)  
    merge_sort = clientes_inactivos.sort_values(by='monto_base_item$', ascending=False)
    print('Total base imponible: $ {:,.2f}'.format(merge_sort['monto_base_item$'].sum()))
    return merge_sort


def graf1():
    df = clientes_retirados()
    plt.figure(figsize=(9, 9)) 
    plots = barplot(x="cli_des", y="monto_base_item$", data=df) 
    
    for bar in plots.patches: 
        offset_from = OffsetFrom(bar, (0.5, 1.0))
        plots.annotate('$' + format(bar.get_height(), ',.0f'),  
                   (bar.get_x() + bar.get_width() / 2,  
                    bar.get_height()), ha='center', va='center', 
                   size=9, xytext=(0, 8), 
                   textcoords=offset_from) 
    plots.tick_params(axis='x', labelrotation = 90, labelsize=7.0) # Rotación eje de las x     
    plt.xlabel("Clientes", size=12) 
    plt.ylabel("Monto facturación mes", size=12) 
    plt.title("Impacto de los clientes retirados sobre la facturación \n Total impacto: $ {:,.2f}".format(df['monto_base_item$'].sum()))
    plt.tight_layout() # Ajusta automáticamente los parámetros de la subtrama para proporcionar un relleno específico.
    plt.show() 
    
    
print(clientes_retirados().to_string())
graf1()