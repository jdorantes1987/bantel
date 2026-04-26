import pyodbc

# Configura los detalles de tu conexión
# Reemplaza los valores con los de tu servidor y base de datos
driver = "{SQL Server}"  # O la versión de tu driver
server = "10.100.104.11"
database = "BANTEL_A"
username = "profit"
password = "profit"

# Cadena de conexión (connection string)
connection_string = (
    f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
)

try:
    # Intenta establecer la conexión
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    print("¡Conexión a la base de datos SQL Server exitosa!")

    # Opcional: Ejecuta una consulta simple para verificar que todo funciona
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    if row:
        print(f"Versión del servidor: {row[0]}")

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"Error al conectar a la base de datos: {sqlstate}")
    print(f"Detalles del error: {ex}")

finally:
    # Cierra la conexión si se estableció
    if "cnxn" in locals() and cnxn:
        cnxn.close()
        print("Conexión cerrada.")
