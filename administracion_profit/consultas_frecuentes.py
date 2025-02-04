from accesos.datos import (
    factura_venta_con_su_detalle_en_usd,
    facturacion_x_anio,
    search_in_compras as buscar_en_compras,
    search_in_movbanco as buscar_en_mov_de_banco,
    search_in_ventas as buscar_en_ventas,
    variacion_tasa_en_cobros,
    variacion_tasa_en_cobros_por_mes,
)

from administracion_profit.clientes import (
    get_top_fact_x_cliente as top_clientes,
    search_clients as buscar_en_client,
)
from administracion_profit.edo_cta import (
    get_edo_cta_bs_y_usd,
    read_data_estados_de_cuenta,
)
from administracion_profit.edo_cta_registrar_mov import (
    establecer_color_amarillo_mov_edo_cta_por_registrar_banesco,
    mov_bcarios_pendientes_por_identif_en_edo_cta_banesco,
    registrar_mov_ban_edo_cta,
)
from administracion_profit.facturas import (
    diccionario_facturacion,
    diccionario_facturacion_total_por_anio,
)
from administracion_profit.facturas import (
    facturacion_saldo_x_clientes_detallado as facturas_con_saldo_det,
    facturacion_saldo_x_clientes_resumen as facturas_con_saldo_res,
    facturas_cobradas_x_clientes_detallado as facturas_cobradas_det,
)
from administracion_profit.facturas import (
    facturas_cobradas_x_clientes_resumen as facturas_cobradas_res,
    graf_calor_ventas,
)
from administracion_profit.obtener_igtf_y_comisiones import get_mov_igtf_comisiones
from administracion_profit.proveedores import (
    get_top_compras_x_prov as top_proveedores,
    search_prov as buscar_en_proveedores,
)
from banco_central.bcv import (
    a_bolivares,
    a_divisas,
    a_divisas_segun_fecha,
    get_date_value,
    get_tasa,
    get_tasa_fecha,
)

from banco_central.bcv_estadisticas_tasas import (
    actulizar_file_tasas as update_file_tasa_bcv,
    grafic as g1bcv,
    grafic3 as g2bcv,
)

# from banco_central.dolar_paralelo import (
#     actulizar_file_tasas as update_file_tasa_par,
#     grafic as g1par,
# )
# from seniat.consultar_rif import consultar_rif

# ##  -->BCV
# update_file_tasa_bcv()
# update_file_tasa_par()
# g1bcv(anio=2024, col_valores="venta_ask2")  # var_tasas o venta_ask2
# g2bcv(2023, "venta_ask2")  # var_tasas o venta_ask2
# g1par(2023, "venta_ask2")  # var_tasas o venta_ask2
# print("Tasa USD del día:", get_date_value(), "\n" * 1, get_tasa())
# print(
#     "El valor de la tasa para la fecha indicada es de:", get_tasa_fecha("20240612")
# )  # Obtiene valor la TASA según la FECHA indicada
# print(
#     "\ncantidad de $ {:,.2f}".format(a_divisas_segun_fecha(100, "20250131"))
# )  # Obtiene MONTO OPERACIÓN en usd según la tasa de la FECHA indicada
# print("Equivalente en $ {:,.2f}".format(a_divisas(511)))  # Convertir a Dólares
# print("Equivalente en Bs. {:,.2f}".format(a_bolivares(50)))  # Convertir a Bolívares

# # -->ESTADO DE CUENTA
# # Registrar los movimientos bancarios seleccionados del estado de cuenta actual banesco
# registrar_mov_ban_edo_cta(anio=2024, mes=12)
# establecer_color_amarillo_mov_edo_cta_por_registrar_banesco("20241201")
# print(mov_bcarios_pendientes_por_identif_en_edo_cta_banesco("2024-12-01").to_string())
# get_edo_cta_bs_y_usd()  # Estado de cuenta banesco en $$$$$$$
# # Muestra los resultados de las comisiones e IGTF a registrar manualmente
# print(get_mov_igtf_comisiones().to_string())
# directory = "C:/Users/jdorantes/Documents/Analisis/Estados de Cuenta/Banesco/2024/"
# file_pattern = "*2024*.xlsx"
# df = read_data_estados_de_cuenta(directory, file_pattern)
# df["Referencia"] = df["Referencia"].astype("str")
# df[df["Pendiente"].str.upper() == "SI"].to_excel("partidas pendientes banesco.xlsx")

# # -->BANCO
# # Muestra los resultados de la busqueda en los movimientos bancarios
# print(buscar_en_mov_de_banco(texto_a_buscar="remol", anio="all", mes="all").to_string())


# # -->PROVEEDORES
# print(
#     buscar_en_proveedores("V133396426").reset_index(drop=True).to_string()
# )  # Muestra los resultados de la busqueda en la tabla de PROVEEDORES
# print(
# buscar_en_compras(str_search="jeep", anio="all").to_string()
# )  # Muestra los resultados de la busqueda en las COMPRAS
# print(top_proveedores().to_string())  # TOP Facturación por proveedores

# -->CLIENTES
# Expresión regular para ubicar los clientes AGRUPADOS que tiene guion (-) ejemplo: CL39-4
patron = r"[A-Za-z]{2}\d{1,3}-\d{1,3}"
# Expresión regular para ubicar los clientes NO AGRUPADOS ejemplo: CL95 sin el guion
patron2 = r"[A-Za-z]{2}\d{1,3}$"
patron3 = (
    r"^0414-\d{7}$"  # Expresión regular para números de teléfono que comienzan con 414
)
# print(
#     buscar_en_client("maria", resumir_datos=True).reset_index(drop=True).to_string()
# )  # Muestra los resultados de la busqueda en la tabla de CLIENTES
# print(
#     buscar_en_ventas(str_search="CL251", anio="all", mes="all")
#     .reset_index(drop=True)
#     .to_string()
# )  # Muestra los resultados de la busqueda en las VENTAS
# print(top_clientes(anio=2024, top=5).to_string())  # TOP Facturación por cliente
# # Listado de facturacion del mes con la variación en la tasa en USD
# # "Ojo solo hace la comparación de la base imponible de la factura"
# print(variacion_tasa_en_cobros(anio=2024).to_string())
# print(
#     variacion_tasa_en_cobros_por_mes(anio=2023)
# )  # Resumen de facturacion del mes con la variación en la tasa en USD
# print(
#     facturas_con_saldo_det(anio="all", dato_cliente="all").to_string()
# )  # FACTURAS CON SALDO detallado
# print(
#     facturas_con_saldo_res(anio="all", usd=True).to_string()
# )  # FACTURAS CON SALDO resumido
# facturas_con_saldo_res(anio="all", dato_cliente="all", usd=False).to_excel(
#     "clientes_con_saldo.xlsx"
# )
# print(facturas_cobradas_det(anio=2024).to_string())  # FACTURAS COBRADAS detallado
# print(
#     facturas_cobradas_res(anio=2024, usd=False).to_string()
# )  # FACTURAS COBRADAS resumido
# facturas_cobradas_res(anio="all", usd=False).to_excel("cobros_por_clientes.xlsx")
# # Diccionario que devuelve de manera INDIVIDUAL
# # el total base imponible en BS o USD de la FACTURACIÓN por AÑO y MES
# print(diccionario_facturacion(anio=2021, mes=1, conv_usd=True))
# # Diccionario que devuelve de manera INDIVIDUAL
# # el total base imponible en BS o USD de la FACTURACIÓN por AÑO
# print(diccionario_facturacion_total_por_anio(anio=2021, conv_usd=True))
# # DETALLE de FACTUTACIÓN archivo Excel
# factura_venta_con_su_detalle_en_usd(anio=2023, usd=True).to_excel(
#     "Facturacion en Bs y Usd al 31-12-2024.xlsx"
# )
# # obtiene el TOTAL BASE IMPONIBLE en BS o $ de la FACTURACIÓN por AÑO y MES
# print(facturacion_x_anio(usd=True).to_string())
# graf_calor_ventas(usd=False)  # GRÁFICO facturación

# # -->SENIAT
# print(consultar_rif("V125639476"))
