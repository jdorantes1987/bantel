import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from administracion_profit.facturas import facturacion_docs_sin_saldo
from pandas import read_excel
from pandas import merge

def leer_imagen(url):
    session_obj = requests.Session()
    respuesta = session_obj.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
    imagen = Image.open(BytesIO(respuesta.content))
    return imagen


# leer_imagen('http://contribuyente.seniat.gob.ve/BuscaRif/Captcha.jpg').show()


def facturas_ret_islr_efect():
    l_campos = ['nro_doc', 'fec_reg', 'Nro. Declaracion', 'Fecha Pago', 'Monto Retenido', '% Ret.']
    fact = facturacion_docs_sin_saldo()
    fact['nro_doc'] = fact['nro_doc'].astype('Int64')
    # Lee un archivo .xlsx
    fact_ret_islr = read_excel("Retenciones Efectivas Seniat.xlsx")
    # Extrae los primeros 80 caracteres de la izquierda
    fact_ret_islr['Descripción'] = fact_ret_islr['Descripción'].str[:30]
    join1 = merge(fact, fact_ret_islr, how='left', left_on='nro_doc', right_on='Nro. Factura')
    join1['Nro. Declaracion'] = join1['Nro. Declaracion'].astype('Int64')
    join1['Fecha Pago'] = pd.to_datetime(join1['Fecha Pago'], format='%d/%m/%Y')
    join1['ret_efect'] = join1.apply(lambda x: 'Si' if x['Monto Retenido'] > 0.00 else 'No', axis=1)
    return join1


facturas_ret_islr_efect().to_string()


