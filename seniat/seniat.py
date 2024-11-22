from io import BytesIO

from bs4 import BeautifulSoup
import requests
from PIL import Image

def leer_imagen(url):
    session_obj = requests.Session()
    response = session_obj.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
    imagen = Image.open(BytesIO(response.content))
    return imagen

def consultar_rif(rif):
    user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    session_obj = requests.Session()
    response = session_obj.get('http://contribuyente.seniat.gob.ve/BuscaRif/Captcha.jpg', 
                               headers=user_agent)
    imagen = Image.open(BytesIO(response.content))
    # rif = input('ingrese el rif:')
    imagen.show()
    cod_imagen = input('ingrese codigo de imagen:')
    # Cerrar el objeto BytesIO
    imagen.close()
    # Eliminar la referencia al objeto BytesIO
    del imagen
    #session_obj = requests.Session()
    response = session_obj.get(f'http://contribuyente.seniat.gob.ve/BuscaRif/BuscaRif.jsp?p_rif={rif}&codigo={cod_imagen}', 
                                headers=user_agent)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all('table')
    # Itera sobre cada tabla
    # for table in tables:
    #     print("Nueva Tabla:")
    #     for row in table.find_all('tr'):
    #         columns = row.find_all(['th', 'td'])
    #         #data = [column.text.strip().replace('\xa0', '').split("\n")[2][10:].strip() for column in columns]
    #         data = [column.text.strip() for column in columns]
    #         print(data)
    
    datos_contibuyente = {}
    for row in tables[1].find_all('tr'):
        columns = row.find_all(['th', 'td'])
        data = [column.text.strip().replace('\xa0', '').split("\n")[2][10:].strip() for column in columns]
    datos_contibuyente['razon_soc'] = data[0]
    
    for row in tables[2].find_all('tr'):
        columns = row.find_all(['th', 'td'])
        data = [column.text for column in columns]
    data = data[0].strip().replace('\r', '').split("\n")
    datos_contibuyente['tipo'] = data[0]
    
    if not 'firma' in datos_contibuyente['tipo']:
        ##Persona Jurídica
        datos_contibuyente['actividad_economica'] = data[0][21:]
        datos_contibuyente['condicion_agente'] = data[1][11:].lstrip() + data[2][12:].lstrip() + data[3].lstrip() + ' ' + data[4].lstrip()
        datos_contibuyente['condicion_porcentaje'] = data[6].lstrip()
    else:
        #Persona Natural
        for row in tables[2].find_all('tr'):
            columns = row.find_all(['th', 'td'])
            data = [column.text for column in columns]
        datos_contibuyente['firmas'] = data[0].strip()

        for row in tables[3].find_all('tr'):
            columns = row.find_all(['th', 'td'])
            data = [column.text.strip().split("\n") for column in columns]
        datos_contibuyente['actividad_economica'] = data[0][0][21:].strip()    
        datos_contibuyente['condicion_agente'] = data[0][2].lstrip()
    return datos_contibuyente
        


