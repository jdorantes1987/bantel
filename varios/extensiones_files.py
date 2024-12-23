import os

i = 0
# traverse whole directory
for root, dirs, files in os.walk(r"C:\Users\jdorantes\Documents\Analisis"):
    # select file name
    for file in files:
        # check the extension of files
        if file.endswith(".xlsm"):
            i += 1
            # print whole path of files
            print(len(os.path.join(root, file)), os.path.join(root, file), sep=";")

print("Cantidad de archivos encontrados:", i)
