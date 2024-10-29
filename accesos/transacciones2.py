# from  accesos.conexion_mkwsp import ConexionBDMysql

class GestorTransacciones2:
    def __init__(self, conexion_db):
        self.conexion = conexion_db
        
    def iniciar_transaccion(self):
        self.conexion.conn.autocommit = False

    def confirmar_transaccion(self):
        self.conexion.conn.commit()
        self.conexion.conn.autocommit = True

    def revertir_transaccion(self):
        self.conexion.conn.rollback()
        self.conexion.conn.autocommit = True
        
    def get_cursor(self):
        try:
            cursor = self.conexion.conn.cursor()
        except Exception as e:
            print("Error al crear cursor: ", e)
        return cursor
        
##  Ejemplo de uso:
# conexion = ConexionBDMysql() #  Crea un objeto conexión
# conexion.conectar()  # inicia la conexión
# gestor = GestorTransacciones2(conexion)
# gestor.iniciar_transaccion()
# cursor = gestor.get_cursor()
# try:
#     # Realiza operaciones en la base de datos...
#     strsql = "INSERT INTO usuarios (id, nombre, estado, correo, telefono, movil, cedula, pasarela, codigo, direccion_principal, codigo_cliente) VALUES (18, 'PRUEBA', 'ACTIVO', 'sianilarez@gmail.com', '+584248997872', '+584248997872', ' V24110681', 's/data', '123', 'HOTEL CCT - CENTRO COMERCIAL CIUDAD TAMANACO', 'CL10');"
#     cursor.execute(strsql)
#     strsql2 = "INSERT INTO tblavisouser (id, cliente, mora, reconexion, impuesto, avatar_cliente, chat, zona, diapago, tipopago, tipoaviso, meses, fecha_factura, diafactura, avisopantalla, corteautomatico, avisosms, avisosms2, avisosms3, afip_condicion_iva, afip, afip_condicion_venta, afip_automatico, avatar_color, tiporecordatorio, afip_punto_venta, id_telegram, router_eliminado, otros_impuestos, mikrowisp_app_id, isaviable, invoice_electronic, invoice_data, fecha_suspendido, limit_velocidad, mantenimiento, data_retirado, fecha_retirado, tipo_estrato, fecha_corte_fija, mensaje_comprobante, id_moneda, afip_enable_percepcion, gatewaynoty, fecha_registro, empresa_afip, code_toku) VALUES (0, 18, '', '', 'NADA', '', 0, 1, 0, 1, 0, 0, null, 0, 0, 0, 0, 0, 0, 'Consumidor Final', '', 'Contado', 0, '#04CF98', 0	, '', 0, 0, 'a:3:{i:1;s:0:"";i:2;s:0:"";i:3;s:0:"";}', '', 0, 0, '', null, 0, 0, '', '', 1, '', 0, 1, 0, '', now(), 1, '');"
#     cursor.execute(strsql2)
#     gestor.confirmar_transaccion()
#     print("Transacción confirmada.")
# except Exception as e:
#     gestor.revertir_transaccion()
#     print(f"Error en la transacción: {e}")
# finally:
#     conexion.desconectar()       

# print('Listo')
# print(conexion.get_read_sql('select * from usuarios'))
