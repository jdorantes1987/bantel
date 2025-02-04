from io import BytesIO
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from PIL import Image

from seniat.verificador_digito import VerificadorDigito


def leer_imagen(url):
    session_obj = requests.Session()
    response = session_obj.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
    )
    imagen = Image.open(BytesIO(response.content))
    return imagen


def consultar_rif(rif):
    user_agent = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/7.0.4 Mobile/16B91 Safari/605.1.15"
    }
    session_obj = requests.Session()
    response = session_obj.get(
        "http://contribuyente.seniat.gob.ve/BuscaRif/Captcha.jpg", headers=user_agent
    )
    imagen = Image.open(BytesIO(response.content))
    # rif = input('ingrese el rif:')
    imagen.show()
    cod_imagen = input("ingrese código de imagen:").lower()
    # Cerrar el objeto BytesIO
    imagen.close()
    # Eliminar la referencia al objeto BytesIO
    del imagen
    datos_contibuyente = {}
    while True:
        response = session_obj.get(
            f"http://contribuyente.seniat.gob.ve/BuscaRif/BuscaRif.jsp?p_rif={rif}&codigo={cod_imagen}",
            headers=user_agent,
        )
        desired_status_code = 200
        # condición de éxito
        if response.status_code == desired_status_code:
            soup = BeautifulSoup(response.content, "html.parser")
            tables = soup.find_all("table")

            for row in tables[1].find_all("tr"):
                columns = row.find_all(["th", "td"])
                data = [
                    column.text.strip().replace("\xa0", "").split("\n")
                    for column in columns
                ]
                # data = [column.text.strip().replace('\xa0', '').split("\n")[2][10:].strip() for column in columns]
            datos_contibuyente["estatus"] = data[0]
            respuesta = ", ".join(datos_contibuyente["estatus"])
            if "No existe" not in respuesta and "no coincide" not in respuesta:
                datos_contibuyente["razon_soc"] = datos_contibuyente["estatus"][2][10:]
                for row in tables[2].find_all("tr"):
                    columns = row.find_all(["th", "td"])
                    data = [column.text for column in columns]
                data = data[0].strip().replace("\r", "").split("\n")
                tipo_contribuyente = data[0]

                if "firma" not in tipo_contribuyente:
                    ## Persona Jurídica
                    datos_contibuyente["actividad_economica"] = data[0][21:]
                    datos_contibuyente["condicion_agente"] = (
                        data[1][11:].lstrip()
                        + data[2][32:].lstrip()
                        + data[3].lstrip()
                        + " "
                        + data[4].lstrip()
                        if len(data) > 3
                        else ""
                    )
                    datos_contibuyente["condicion_porcentaje"] = (
                        data[2].lstrip() if len(data) == 3 else data[5].lstrip()
                    ) + (data[6].lstrip() if len(data) == 7 else "")
                else:
                    # Persona Natural
                    for row in tables[2].find_all("tr"):
                        columns = row.find_all(["th", "td"])
                        data = [column.text for column in columns]
                    datos_contibuyente["firmas"] = data[0].strip()

                    for row in tables[3].find_all("tr"):
                        columns = row.find_all(["th", "td"])
                        data = [column.text.strip().split("\n") for column in columns]
                    datos_contibuyente["actividad_economica"] = data[0][0][21:].strip()
                    tipo = len(data[0])
                    if tipo == 3:
                        datos_contibuyente["condicion_agente"] = data[0][2].lstrip()
                    else:
                        datos_contibuyente["condicion_agente"] = (
                            data[0][2].strip() + " " + data[0][5].lstrip()
                        )
                break
            else:
                if "No existe" in respuesta:
                    datos_contibuyente["estatus"] = "No existe el RIF consultado"
                    break
                elif "no coincide" in respuesta:
                    print(datos_contibuyente)
                    cod_imagen = input("ingrese nuevamente el código de imagen:")
        else:
            datos_contibuyente["estatus"] = "Error en conexión"
            break

    return datos_contibuyente


if __name__ == "__main__":
    rif = VerificadorDigito("j500823010").get_rif()
    no_existe = "n/e"
    if rif != no_existe:
        pprint(consultar_rif(rif), sort_dicts=False)
    else:
        print(no_existe)
