# """
#     sys.path.append()Uso básico: función de Python
#     La función de Python sys.path.append()es el método más básico y comúnmente utilizado para importar módulos desde diferentes directorios.

#     Cuando importas un módulo en Python, lo busca en los directorios enumerados en sys.path. Entonces, si desea importar un módulo desde un directorio que aún no está en sys.path, simplemente puede agregar ese directorio usando sys.path.append().
#     He aquí un ejemplo sencillo:
# """


# import sys

# # print the original sys.path
# print('Original sys.path:', sys.path)

# append a new directory to sys.path
# sys.path.append('/path/to/directory')


"""
Navegando directorios con os.pathyos.chdir()
A medida que avanza en su viaje con Python, es posible que necesite más control sobre sus directorios. Aquí es donde el osmódulo resulta útil, específicamente os.pathy os.chdir().

El os.pathmódulo contiene funciones para manipular rutas de archivos y os.chdir()cambia el directorio de trabajo actual. Al cambiar el directorio de trabajo, puede importar módulos de Python como si estuvieran en el mismo directorio que su script.

Veamos cómo funciona esto con un ejemplo:
"""

import os

# print the current working directory
print('Original working directory:', os.getcwd())

# change the working directory
os.chdir('/path/to/directory')

# print the updated working directory
print('Updated working directory:', os.getcwd())

# now you can import your module
# import your_module

