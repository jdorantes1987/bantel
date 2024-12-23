import files


def listar():
    print("Indique la unidad donde se realizará la busqueda:")
    unidad = input()
    print("Se buscará en la unidad:", unidad)
    print("\n" * 1)
    print("Indique la descripción del archivo a buscar:")
    typedtext = input()
    print("Se buscarán todos los archivos que contengan la palabra ", typedtext)
    print("\n" * 1)

    print(
        "Indique la extensión del archivo a buscar, en caso de que no saberlo se buscaran todas las extensiones:"
    )
    typedext = input()
    print("Se buscarán todas las extensiones ", typedext)
    print("Buscando...")
    print("\n" * 1)
    files.buscar(unidad, typedtext, typedext)
