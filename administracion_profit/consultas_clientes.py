from accesos.datos import search_in_ventas as buscar_en_ventas
from facturas import facturacion_saldo_x_clientes as fact_saldo
from clientes import search_clients as buscar_en_client
from clientes import get_top_fact_x_cliente as top_clientes

# *******Consulta tabla CLIENTES*******
print(buscar_en_client("J409543390").reset_index(drop=True).to_string())

# # _______Consulta FACTURAS clientes_______
# print(buscar_en_ventas("ADRIAN").reset_index(drop=True).to_string())
#
# # _______TOP Facturación por clientes_______
# print(top_clientes(top=5).to_string())

# # _______Facturas de clientes con SALDO_______
# print(fact_saldo().to_string())


