import plotly.figure_factory as ff

import administracion_profit.facturas as fact
import varios.zoho as zh

# *******Datos de DECLARACION DE IMPUESTOS*******
# datos_declaracion = fact.datos_declaracion()
# datos_declaracion['Monto'] = datos_declaracion['Monto'].apply('{:,.2f}'.format)
# fig = ff.create_table(datos_declaracion)
# fig.update_layout(autosize=True, width=500, height=150,)
# nombre_file = 'Declaracion 1ra Qna Mar 2024.png'
# fig.write_image(nombre_file, scale=2)
# # aperez@bantel.net.ve
# zh.message(address_send=['jdorantes@bantel.net.ve'],
#            subject='Datos para la declaración',
#            text='Información para el pago de impuestos:',
#            img=nombre_file)

fact.ajustes_man_compras_sin_cta_contable()
fact.ajustes_aut_compras_sin_cta_contable()
fact.ajustes_man_ventas_sin_cta_contable()
fact.ajustes_aut_ventas_sin_cta_contable()
