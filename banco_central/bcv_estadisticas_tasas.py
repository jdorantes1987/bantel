from pandas import DataFrame
from pandas import concat
from pandas import to_datetime
import locale
import time
# import urllib.request
from urllib.request import build_opener, install_opener, urlretrieve, urlcleanup
from xlrd import open_workbook
from matplotlib.pyplot import subplots, title, show, tight_layout, xticks
from seaborn import heatmap, set_style, lineplot
from banco_central.dolar_paralelo import datos_estadisticas_tasas
from accesos.files_excel import p_data_estadisticas_bcv as p_est_bcv, p_data_estadisticas_bcv_datapy as p_est_bcv_datapy
from accesos.files_excel import datos_estadisticas_tasas as datos_estad_bcv
from ssl import create_default_context

context = create_default_context()
url_base = 'https://www.bcv.org.ve/sites/default/files/EstadisticasGeneral'
dic_f_usd_year = {'2024': ['2_1_2d24_smc.xls', '2_1_2c24_smc.xls','2_1_2b24_smc.xls', '2_1_2a24_smc.xls'],
                  '2023': ['2_1_2d23_smc.xls', '2_1_2c23_smc.xls', '2_1_2c23_smc_60.xls', '2_1_2a23_smc.xls'],
                  '2022': ['2_1_2d22_smc.xls', '2_1_2c22_smc.xls', '2_1_2b22_smc.xls', '2_1_2a22_smc.xls'],
                  '2021': ['2_1_2d21_smc.xls', '2_1_2c21_smc.xls', '2_1_2b21_smc.xls', '2_1_2a21_smc_58.xls'],
                  '2020': ['2_1_2d20_smc.xls', '2_1_2c20_smc.xls', '2_1_2b20_smc.xls', '2_1_2a20_smc.xls']
                  }

def get_data_usd_bcv_web():
    df_union = DataFrame()
    df_arr_wb = []
    l_files = list(dic_f_usd_year.values())

    l_files_join = [x for y in l_files for x in y]
    for item in l_files_join:
        url = url_base + f'/{item}'
        # file_name, headers = urllib.request.urlretrieve(url) #  Este era el código antes de agregarle el 'User-Agent'
        opener = build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')]
        install_opener(opener)
        file_name =urlretrieve(url)
        wb = open_workbook(file_name[0], on_demand=True)  # Abre el libro de trabajo con el indicador "on_demand=True", para que las hojas no se carguen automáticamente.
        sheets = wb.sheet_names()
        cols = ['cod_mon', 'mon_pais', 'compra_bid', 'venta_ask', 'compra_bid2', 'venta_ask2']
        df_arr_sh = []
        for i in range(len(sheets)):
            sh = wb.sheet_by_index(i)
            # Creamos las listas
            filas = []
            for fila in range(11, 33):
                columnas = [sh.cell_value(fila, columna + 1) for columna in range(0, 6)]
                filas.append(columnas)
            df_base = DataFrame(filas, columns=cols)
            # extrae la fecha valor de la celda D5, hay que remover los espacios
            df_base['fecha'] = str(sh.cell_value(4, 3))[13:].replace('/', '').strip()
            # df_base['fecha'] = sh.name
            df_base['fecha'] = to_datetime(df_base['fecha'], format='%d%m%Y')
            df_base['archivo'] = item
            df_arr_sh.append(df_base)
        data = concat(df_arr_sh, axis=0, ignore_index=True)
        data = data[data['cod_mon'] == 'USD']
        df_arr_wb.append(data)
        df_union = concat(df_arr_wb, axis=0, ignore_index=True)
        print('Se descargó archivo de la ruta:', url)
        wb.release_resources()
        del wb
        time.sleep(10)
    # Convertir la columna de fechas a formato datetime
    df_union['fecha'] = to_datetime(df_union['fecha'])
    return df_union.sort_values(by=['fecha'], ascending=False).reset_index(
        drop=True
    )


'''
RECUERDA HACER LA RECONVERSIÓN MONETARIA DEL 27/3/2020 AL 28/9/2021 ENTRE 100.000 (5 CEROS) DESPUES DE GENERAR EL ARCHIVO
'''
def generar_file_usd_bcv():
    get_data_usd_bcv_web().to_excel('tasas_BCV.xlsx')

# ACTUALIZA EL HISTÓRICO DE TASAS CON LA ÚLTIMA PUBLICACIÓN
def get_data_usd_bcv_web_last_qt():
    name_file_tasa_download = list(dic_f_usd_year.values())[0][0]  # Convierte el diccionario en una lista y obtiene el primer elemento
    url = url_base + f'/{name_file_tasa_download}'
    #  cambiar el encabezado del agente de usuario
    opener = build_opener()
    #  agregar el encabezado de solicitud de agente de usuario
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')]
    file_name = urlretrieve(url)
    print('Se descargó archivo de la ruta:', url)
    # Como el resultado de la descarga es una tuple con la información del archivo y el recurso de la web se coloca el indice [0] que es la del archivo
    wb = open_workbook(file_name[0], 
                       on_demand=True)  # Abre el libro de trabajo con el indicador "on_demand=True", para que las hojas no se carguen automáticamente.
    sheets = wb.sheet_names()
    cols = ['cod_mon', 'mon_pais', 'compra_bid', 'venta_ask', 'compra_bid2', 'venta_ask2']
    df_arr_sh = []
    for i in range(len(sheets)):
        sh = wb.sheet_by_index(i)
        # Creamos las listas
        filas = []
        for fila in range(11, 33):
            columnas = [sh.cell_value(fila, columna + 1) for columna in range(0, 6)]
            filas.append(columnas)
        df_base = DataFrame(filas, columns=cols)
        # extrae la fecha valor de la celda D5, hay que remover los espacios
        df_base['fecha'] = str(sh.cell_value(4, 3))[13:].replace('/', '').strip()
        # df_base['fecha'] = sh.name  # Anteriormente extraía la fecha del nombre de la hoja lo cual es incorrecto, ya que se debe tomar la fecha valor.
        df_base['fecha'] = to_datetime(df_base['fecha'], format='%d%m%Y')
        df_base['archivo'] = name_file_tasa_download
        df_arr_sh.append(df_base)
    data = concat(df_arr_sh, axis=0, ignore_index=True)
    data = data[data['cod_mon'] == 'USD']
    urlcleanup()
    # wb.release_resources()
    # del wb
    return data


# Actualiza el archivo tasas_BCV.xlsx
def actulizar_file_tasas():
    locale.setlocale(locale.LC_ALL, 'es_ES')
    df_file_tasa = datos_estad_bcv()
    df_file_tasa_new = get_data_usd_bcv_web_last_qt()
    name_file_tasa_download = list(dic_f_usd_year.values())[0][0]  # Obtiene el primer nombre de la lista de diccionario
    df_file_tasa_filtred = df_file_tasa[df_file_tasa['archivo'] != name_file_tasa_download]
    new_file_tasa = [df_file_tasa_new, df_file_tasa_filtred]
    df = concat(new_file_tasa).reset_index(drop=True)
    df['año'] = df['fecha'].dt.year
    df['mes'] = df['fecha'].dt.month
    df['dia'] = df['fecha'].dt.day
    df['mes_'] = df['fecha'].dt.month_name(locale='es_ES').str[:3]
    locale.setlocale(locale.LC_ALL, '')
    df['var_tasas'] = df['venta_ask2'].diff(
        periods=-1)  # Permite calcular la diferencia que existe entre el valor de la celda actual con respecto a la anterior
    df.to_excel(p_est_bcv)
    # df.to_excel(p_est_bcv_datapy) # Código agregado el 16-05-2024


def row_index(row):
    return row.name


def variacion_tasas_por_dia():
    return datos_estad_bcv()


def grafic(**kwargs):
    anio, col_valores = kwargs.get('anio','all'), kwargs.get('col_valores', 'venta_ask2')
    var_tasa = variacion_tasas_por_dia()
    df = var_tasa if anio == 'all' else var_tasa[var_tasa['año'] == anio].copy()
    set_style('whitegrid')
    fig, ax = subplots(figsize=(16, 7))
    multi = lineplot(x='fecha',
                         y=col_valores,
                         hue='cod_mon',
                         marker='o',
                         linewidth=0.7,
                         data=df,
                         palette='deep')  # crest

    # Descomentar codigo si deseas ver los valores de las etiquetas
    # zip joins x and y coordinates in pairs
    '''
    for x, y in zip(df['fecha'], df[valores_eval]):
        label = "{:.2f}".format(y)
        plt.annotate(label,  # this is the text
                     (x, y),  # these are the coordinates to position the label
                     textcoords="offset pixels",  # how to position the text
                     size=7,
                     rotation=90,
                     xytext=(0, 7),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center

    plt.xticks(rotation=90)
    '''
    title('Variación Tasa USD BCV', fontsize=15, fontweight="bold")
    tight_layout()
    show()


def union_data_bcv_paralelo():
    df_data_bcv = datos_estad_bcv()
    df_data_bcv['archivo'] = 'bcv'
    df_data_par = datos_estadisticas_tasas()
    df_data_par['archivo'] = 'par'
    new_file_tasa = [df_data_bcv, df_data_par]
    df = concat(new_file_tasa).reset_index(drop=True)
    return df.sort_values(by=['fecha'], ascending=False).reset_index(drop=True)


def grafic3(anio, valores_eval):
    var_tasa = union_data_bcv_paralelo()
    df = var_tasa[var_tasa['año'] == anio]
    set_style('whitegrid')
    fig, ax = subplots(figsize=(16, 7))
    palette = ["#a9889a", "#146bad"]
    multi = lineplot(x='fecha',
                         y=valores_eval,
                         hue='archivo',
                         marker='o',
                         linewidth=0.7,
                         data=df,
                         palette='mako')  # crest, deep, viridis, husl
    xticks(rotation=90)
    title('Variación Tasa USD', fontsize=15, fontweight="bold")
    tight_layout()
    show()