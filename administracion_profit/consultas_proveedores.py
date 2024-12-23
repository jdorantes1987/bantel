from accesos.datos import search_in_compras as buscar_en_compras
from administracion_profit.proveedores import get_top_compras_x_prov as top_proveedores
from administracion_profit.proveedores import search_prov as buscar_en_proveedores

# *******Consulta PROVEEDORES*******
print(buscar_en_proveedores("J500562527").reset_index(drop=True).to_string())
# _______Consulta Facturas Proveedores_______
print(buscar_en_compras("jackson").to_string())
# # _______TOP Facturación por proveedores_______
print(top_proveedores(top=3).to_string())
