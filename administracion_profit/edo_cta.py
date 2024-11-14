from pandas import read_excel, merge_asof, to_datetime, DataFrame, concat
import glob
import os
from accesos.files_excel import datos_estadisticas_tasas as p_est_bcv
from accesos.files_excel import p_data_edo_cta_banesco as p_edo_cta_banesco
from accesos.datos import conjunto_ref_mov_bcrios

def get_edo_cta_bs_y_usd():
    fields_edo_cta = ['Fecha', 'Referencia', 'Descripción', 'Monto', 'USD', 'Comentarios']
    df_edo_cta = read_excel(p_edo_cta_banesco)
    df_data_bcv = p_est_bcv()  # archivo BCV
    df_edo_cta['Fecha'] = to_datetime(df_edo_cta['Fecha']).dt.normalize()  # fecha sin hora, minutos y segundos
    df_edo_cta['Referencia'] = df_edo_cta['Referencia'].astype('Int64')
    # Para trabajar con el estado de cuenta se debe filtrar las referencias vacias
    edo_cta = df_edo_cta[(df_edo_cta['Fecha'].notnull()) & (df_edo_cta['Fecha'] != '')]
    data_bcv_sort = df_data_bcv.sort_values(by=['fecha'],
                                            ascending=[True])  # se debe ordenar el df para poder conbinar
    edo_cta_sort = edo_cta.sort_values(by=['Fecha'],
                                       ascending=[True])  # se debe ordenar el df para poder conbinar
    merge_data = merge_asof(edo_cta_sort, data_bcv_sort, left_on='Fecha', right_on='fecha',
                               direction="nearest")  # Combinar por aproximación
    merge_data['USD'] = merge_data.apply(lambda x: x['Monto'] / x['venta_ask2'], axis=1)
    merge_data['USD'] = merge_data['USD'].apply('${:,.2f}'.format)  # Se aplica formato de $ float
    merge_data['Comentarios'] = merge_data['Comentarios'].str[:60]  # Extrae los primeros 60 caracteres de la izquierda
    merge_data_sort = merge_data.sort_values(by=['Fecha', 'Referencia', 'Monto'], ascending=[False, True, True])
    print(merge_data_sort[fields_edo_cta].to_string())

def conjunto_ref_bcarias_edo_cta():
    # Establece como String-str la columna nro_doc
    df_edo_cta = read_excel(p_edo_cta_banesco, dtype={'Referencia': str})['Referencia']
    referencias_unicas = set(df_edo_cta)
    return referencias_unicas

def get_mov_edo_cta_pdtes_por_regist(str_date):
    mov_sin_registrar = conjunto_ref_bcarias_edo_cta() - conjunto_ref_mov_bcrios(str_date)
    return mov_sin_registrar

def get_mov_bcarios_pdtes_por_identificar(str_date):
    mov_sin_registrar = conjunto_ref_mov_bcrios(str_date) - conjunto_ref_bcarias_edo_cta()
    return mov_sin_registrar



def read_data_estados_de_cuenta(directory, name_pattern):
    # Lista para almacenar los DataFrames
    dataframes = []
    # Recorre todos los subdirectorios y archivos que cumplan con el criterio
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(file)
            if glob.fnmatch.fnmatch(file, name_pattern):
                file_path = os.path.join(root, file)
                df = read_excel(file_path)
                dataframes.append(df)

    # Combina todos los DataFrames en uno solo
    combined_df = concat(dataframes, ignore_index=True)
    return combined_df


