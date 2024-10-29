from datetime import date
import numpy as np
from pandas import read_excel, DataFrame, merge, to_datetime, concat
import contabilidad_profit.comprob as cbte
import varios.utilidades
from accesos.files_excel import p_data_edo_cta_banesco as p_edo_cta_banesco

l_ctas_gasto = ['6.2.01.01.0004', '6.2.01.01.0003']

def get_mov_igtf_comisiones():
    data_edo_cta = read_excel(p_edo_cta_banesco, dtype={'Referencia': str}).replace(np.nan, '')
    f_edo_cta_sin_nulos = data_edo_cta[(data_edo_cta['Fecha'].notnull()) & (data_edo_cta['Fecha'] != '')]  # filtra los valores no nulos
    edo_cta_ref_counts =DataFrame(f_edo_cta_sin_nulos['Referencia'].value_counts())
    # Cambia el nombre de la columna
    edo_cta_ref_counts.rename(columns={'count': 'repeticiones'}, inplace=True)
    # Une los DataFrame a traves de la clausula LeftJoint
    f_edo_cta_ref_repet = merge(f_edo_cta_sin_nulos, edo_cta_ref_counts, left_on='Referencia', right_on='Referencia')
    f_edo_cta_ref_repet['Monto'] = f_edo_cta_ref_repet['Monto'].astype('float64')
    f_edo_cta_ref_repet['Fecha'] = to_datetime(f_edo_cta_ref_repet['Fecha'])
    # -----------------------------OBTENER IGTF DE PAGOS CON 4 REPETICIONES EN REFERENCIAS--------------------------------->
    f_edo_cta_ref_repet['Cuenta_contable'] = l_ctas_gasto[1]
    filtrar_solo_igtf_sort = f_edo_cta_ref_repet.sort_values(by=['Fecha', 'Referencia', 'Monto'], ascending=[True, True, True])
    igtf_huerf = filtrar_solo_igtf_sort[filtrar_solo_igtf_sort['repeticiones'] >= 2].copy()  # Se hace una copia del dataframe para que no me arroje advertencia
    igtf_huerf['Monto_Ant'] = igtf_huerf['Monto'].shift(1)  # Obtiene el elemento anterior en relacion al elemento actual
    # Obtiene el porcentaje que representa el monto del elemento actual respecto al anterior
    igtf_huerf['porcentaje'] = igtf_huerf.apply(lambda x: round(x['Monto'] / x['Monto_Ant'], ndigits=2), axis=1)
    solo_igtf_sort2 = igtf_huerf[(igtf_huerf['porcentaje'] <= 0.02)]  # | (edo_cta_igtf_huerf['porcentaje'] == 0.01)
    # Recuerda que al trabajar con números negativos los valores máximos son los que estan más cerca del cero
    # Obtiene los valores máximos de cada grupo de referencias
    igtf_group = solo_igtf_sort2.loc[solo_igtf_sort2.groupby('Referencia', sort=False).Monto.idxmax()].reset_index(drop=True)  # sort=False para que no ordene los grupos
    igtf_pagos = igtf_group[(igtf_group['repeticiones'] == 4) & (igtf_group['Monto'] < 0)]
    # print("IGTF de pagos con 4 repeticiones en las referencias bancarias \n", igtf_pagos.to_string())
    # -----------------------------OBTENER IGTF DE COBROS CON 3 REPETICIONES EN REFERENCIAS--------------------->
    igtf_cob_rep_3 = solo_igtf_sort2[(solo_igtf_sort2['repeticiones'] == 3) & (solo_igtf_sort2['Monto'] > 0)]
    # Intersección de dos columnas en dos marcos de datos
    igtf_cob_rep_3_inters = solo_igtf_sort2[solo_igtf_sort2['Referencia'].isin(igtf_cob_rep_3['Referencia'])].copy()
    igtf_cob_rep_3_inters['Cuenta_contable'] = l_ctas_gasto[1]
    filtrar_igtf_rep_3 = igtf_cob_rep_3_inters[(igtf_cob_rep_3_inters['porcentaje'] == 0.02) &
                                               (igtf_cob_rep_3_inters['repeticiones'] == 3)]
    # print("IGTF de cobros con 3 repeticiones en las referencias bancarias\n",
    #       filtrar_igtf_rep_3.reset_index(drop=True).to_string())
    # ----------------------------------------OBTENER COMISIONES DE PAGOS-------------------------------------------------->
    igtf_huerf['Cuenta_contable'] = l_ctas_gasto[0]
    edo_cta_sin_igtf = igtf_huerf[igtf_huerf['porcentaje'] != 0.02].copy()
    edo_cta_sin_igtf['Monto_Ant'] = edo_cta_sin_igtf['Monto'].shift(1)
    edo_cta_sin_igtf['porcentaje'] = edo_cta_sin_igtf.apply(lambda x: round(x['Monto'] / x['Monto_Ant'], ndigits=3), axis=1)
    com_de_pagos = edo_cta_sin_igtf[(edo_cta_sin_igtf['porcentaje'] == 0.003) |
                                    (edo_cta_sin_igtf['porcentaje'] == 0.004)]
    # print("Comisiones de pagos\n", com_de_pagos.to_string())
    # ----------------------------------------OBTENER COMISIONES DE COBROS------------------------------------------------->
    edo_cta_sin_igtf['Cuenta_contable'] = l_ctas_gasto[0]
    edo_cta_sin_com_pag = edo_cta_sin_igtf[(edo_cta_sin_igtf['porcentaje'] != 0.003)].copy()
    comisiones = edo_cta_sin_com_pag.sort_values(by=['Fecha', 'Referencia', 'Monto'], ascending=[True, True, False])
    comisiones['Monto_Ant'] = comisiones['Monto'].shift(1)
    comisiones['porcentaje'] = comisiones.apply(lambda x: round(x['Monto'] / x['Monto_Ant'], ndigits=3), axis=1)
    com_de_cobros = comisiones[(comisiones['porcentaje'] == -0.015)]
    # print("Comisiones de cobros\n", com_de_cobros.to_string())

    df_union_query = [igtf_pagos, filtrar_igtf_rep_3, com_de_pagos, com_de_cobros]
    return concat(df_union_query).reset_index(drop=True)


def __get_asiento_contable(descripcion_asiento):
    d_igtf_and_com = get_mov_igtf_comisiones()
    ctas_gto = d_igtf_and_com.groupby('Cuenta_contable')[['Monto']].sum().reset_index()
    d_igtf_and_com['Cuenta_contable'] = '1.1.02.01.0003'
    ctas_bco = d_igtf_and_com
    df_lt = [ctas_gto, ctas_bco]
    union = concat(df_lt).reset_index(drop=True)
    # Saber si un valor o elemento se encuentra en una lista, es decir si la cuenta contable está dentro del listado de
    # cuentas de gasto
    union['Debe'] = union.apply(lambda x: abs(x['Monto']) if x['Cuenta_contable'] in set(l_ctas_gasto) else 0.0, axis=1)
    union['Haber'] = union.apply(
        lambda x: (
            abs(x['Monto'])
            if x['Cuenta_contable'] not in set(l_ctas_gasto)
            else 0.0
        ),
        axis=1,
    )
    union['Descripcion'] = descripcion_asiento
    union['Referencia'] = union['Referencia'].astype('Int64')
    union[['Cuenta_contable', 'Referencia', 'Descripcion', 'Debe', 'Haber']].to_excel('union.xlsx')
    return union[['Cuenta_contable', 'Referencia', 'Descripcion', 'Debe', 'Haber']]


def contabilizar_comisiones_e_igtf(id_cbte, fecha_cbte, descripcion_cbte):
    date_cbte = to_datetime(date(to_datetime(fecha_cbte).year, to_datetime(fecha_cbte).month,
                                    to_datetime(fecha_cbte).day),
                               format='%d%m%Y').strftime('%Y-%m-%d')
    date_current = varios.utilidades.date_today()
    data_asiento = __get_asiento_contable(descripcion_cbte)
    cbte.new_encab_comprobante(id_cbte,
                               descripcion_cbte,
                               date_cbte,
                               date_current,
                               date_current)
    print('Insertando...')
    for index, row in data_asiento.iterrows():
        index += 1
        cbte.new_line_comprobante(id_cbte,
                                  date_cbte,
                                  index,
                                  row["Debe"],
                                  row["Haber"],
                                  row["Descripcion"],
                                  row["Cuenta_contable"],
                                  '',
                                  date_current,
                                  date_current,
                                  'NULL')


# print(get_mov_igtf_comisiones().to_string())
