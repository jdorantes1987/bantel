from accesos.datos import dict_con_admin
from administracion_profit.facturas import procesar_facturacion_masiva


def procesar_documentos(indice_file, a_bs, num_fact_format):
    """Ejecuta el proceso de facturación de acuerdo a la empresa seleccionada.

    Args:
        indice_file (int): 0 Recibos 1 Facturas
        a_bs (boolean): convertir los montos en bolívares según la tasa actual de BCV.
        num_fact_format (boolean): aplicar formato al correlativo de factura.
    """
    if indice_file == 0:
        dict_con_admin.update(
            {
                "host": "10.100.104.11",
                "base_de_datos": "BANTEL_I",
            }
        )
    else:
        dict_con_admin.update(
            {
                "host": "10.100.104.11",
                "base_de_datos": "BANTEL_A",
            }
        )  # 10.100.104.11 BANTEL PRODUCCIÓN | 10.22.22.3 BANTEL DESARROLLO

    procesar_facturacion_masiva(indice_file, a_bs, num_fact_format)


def generar_recibos():
    procesar_documentos(indice_file=0, a_bs=False, num_fact_format=True)


def generar_facturas():
    procesar_documentos(indice_file=1, a_bs=True, num_fact_format=False)


# Correr proceso
# ----------------------------------------------------------------------------------------------------
# generar_recibos()
generar_facturas()
