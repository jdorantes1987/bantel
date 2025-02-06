import winreg
import csv


def listar_registro(clave_base, ruta_clave, escritor_csv):
    try:
        clave = winreg.OpenKey(clave_base, ruta_clave)
        i = 0
        while True:
            try:
                subclave = winreg.EnumKey(clave, i)
                ruta_subclave = f"{ruta_clave}\\{subclave}"
                escritor_csv.writerow([ruta_subclave, "", ""])
                listar_registro(clave_base, ruta_subclave, escritor_csv)
                i += 1
            except OSError:
                break
        j = 0
        while True:
            try:
                nombre, valor, tipo = winreg.EnumValue(clave, j)
                escritor_csv.writerow([ruta_clave, nombre, valor])
                j += 1
            except OSError:
                break
        winreg.CloseKey(clave)
    except OSError as e:
        print(f"Error al leer el registro: {e}")


ruta_clave = r"SOFTWARE"
# ruta_clave = r"SOFTWARE\Microsoft\Windows\CurrentVersion"
archivo_csv = "datos_registro CURRENT_USER.csv"

with open(archivo_csv, mode="w", newline="", encoding="utf-8") as archivo:
    escritor_csv = csv.writer(archivo)
    escritor_csv.writerow(["Ruta", "Nombre", "Valor"])
    listar_registro(winreg.HKEY_CURRENT_USER, ruta_clave, escritor_csv)

print(f"Los datos del registro se han guardado en {archivo_csv}")
