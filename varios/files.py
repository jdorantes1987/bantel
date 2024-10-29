import glob
import os
import subprocess
import datetime

path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # Ruta del escritorio
path_documentos = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')  # Ruta mis Documentos

# glob.glob() return a list of file name with specified pathname
def buscar(ruta, descripcion='*', extension='.'):
    for file_ in glob.glob(ruta + '**/*' + descripcion + '*' + extension, recursive=True):
        print(os.path.join(ruta, file_))

def busqueda_interactiva():

    escritorio = path_desktop + '\\'
    mis_documentos = path_documentos + '\\'
    drive_str = subprocess.check_output("fsutil fsinfo drives").decode('utf-8')  # decode('utf-8') Eliminar el prefijo 'b' de una caden
    drives = drive_str.split()
    drives.pop(0)  # Elimina el primer elemento
    drives.insert(0, escritorio)
    drives.insert(1, mis_documentos)
    print(drives)
    ind = input('ingrese el indice de la unidad:' + '\n')
    str_name_file = input('ingrese parte del nombre del archivo:' + '\n')
    str_ext = input('ingrese la extensión del archivo:' + '\n')
    unidad = drives[int(ind)]
    print('\nBuscando en la unidad', unidad)
    buscar(str(unidad), str_name_file, str_ext)


def modified_today(path):
    print('\n', '-' * 7, 'Archivos modificados el día de hoy()', '-' * 7)
    today = datetime.datetime.now().date()
    for root, dirs, files in os.walk(path):
        for cur_file in files:
            file_path = os.path.join(root, cur_file)
            if datetime.date.fromtimestamp(os.path.getmtime(file_path)) == today:  # getmtime atributo clave
                yield file_path

def get_files_modified_today(path='C:\\Users\\jdorantes\\'):
    for c_file in modified_today(path):
        print(c_file)


def created_today(path):
    print('\n', '-' * 7, 'Archivos creados el día de hoy()', '-' * 7)
    today = datetime.datetime.now().date()
    for root, dirs, files in os.walk(path):
        for cur_file in files:
            file_path = os.path.join(root, cur_file)
            if datetime.date.fromtimestamp(os.path.getctime(file_path)) == today:   # getctime atributo clave
                yield file_path


def get_files_created_today(ruta='C:\\Users\\jdorantes\\'):
    for file in created_today(ruta):
        print(file)

def file_exists(path):
    return os.path.exists(path)
