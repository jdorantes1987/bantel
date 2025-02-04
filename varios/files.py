import datetime
import glob
import os
import subprocess

path_desktop = os.path.join(
    os.path.join(os.environ["USERPROFILE"]), "Desktop"
)  # Ruta del escritorio
path_documentos = os.path.join(
    os.path.join(os.environ["USERPROFILE"]), "Documents"
)  # Ruta mis Documentos


#  Escoger la unidad de almacenamiento
def escoger_unidad():
    escritorio = path_desktop + "\\"
    mis_documentos = path_documentos + "\\"
    drive_str = subprocess.check_output("fsutil fsinfo drives").decode(
        "utf-8"
    )  # decode('utf-8') Eliminar el prefijo 'b' de una caden
    drives = drive_str.split()
    drives.pop(0)  # Elimina el primer elemento
    drives.insert(0, escritorio)
    drives.insert(1, mis_documentos)
    print(drives)
    ind = input("ingrese el indice de la unidad:" + "\n")
    return drives[int(ind)]  # retorna la unidad seleccionada


# glob.glob() return a list of file name with specified pathname
def buscar(ruta, descripcion="*", extension="."):
    for file_ in glob.glob(
        ruta + "**/*" + descripcion + "*" + extension, recursive=True
    ):
        print(os.path.join(ruta, file_))


def busqueda_interactiva():
    unidad = escoger_unidad()  # Seleccionar unidad
    str_name_file = input("ingrese parte del nombre del archivo:" + "\n")
    str_ext = input("ingrese la extensión del archivo:" + "\n")
    print("\nBuscando en la unidad", unidad)
    buscar(str(unidad), str_name_file, str_ext)


def files_modified(path, date_modified):
    print(
        "\n",
        "-" * 7,
        f"Archivos modificados del día {datetime.datetime.strftime(date_modified, format="%d-%m-%Y")}",
        "-" * 7,
    )
    for root, dirs, files in os.walk(path):
        for cur_file in files:
            file_path = os.path.join(root, cur_file)
            try:
                if (
                    datetime.date.fromtimestamp(os.path.getmtime(file_path))
                    == date_modified
                ):  # getmtime atributo clave
                    yield file_path
            except OSError:
                yield f"{file_path} no tiene permisos para acceder"


def created_today(path, date_created):
    print(
        "\n",
        "-" * 7,
        f"Archivos creados del día {datetime.datetime.strftime(date_created, format="%d-%m-%Y")}",
        "-" * 7,
    )
    for root, dirs, files in os.walk(path):
        for cur_file in files:
            file_path = os.path.join(root, cur_file)
            if (
                datetime.date.fromtimestamp(os.path.getctime(file_path)) == date_created
            ):  # getctime atributo clave
                yield file_path


def get_files_modified(**kwargs):
    date_modified = datetime.datetime.strptime(
        kwargs.get("date_modified", datetime.datetime.now().date().strftime("%Y%m%d")),
        "%Y%m%d",
    ).date()
    path = escoger_unidad()  # Seleccionar unidad
    for c_file in files_modified(path, date_modified=date_modified):
        print(c_file)


def get_files_created(**kwargs):
    date_created = datetime.datetime.strptime(
        kwargs.get("date_created", datetime.datetime.now().date().strftime("%Y%m%d")),
        "%Y%m%d",
    ).date()
    path = escoger_unidad()  # Seleccionar unidad
    for file in created_today(path, date_created=date_created):
        print(file)


def file_exists(path):
    return os.path.exists(path)


if __name__ == "__main__":
    busqueda_interactiva()
    # fecha = input("Fecha en formato AAAAMMDD:" + "\n")
    # get_files_modified()  # archivos modificados el día de hoy
    # get_files_created(date_created=fecha)  # archivos creados el día de hoy
