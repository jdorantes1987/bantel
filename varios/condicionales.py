# Validar la aprobación de una material según la calificación ingresada
# De 0 al 9,4 "Reprobado"
# De 9,5 al 14,4 "Deficiente"
# De 14,5 al 15,4 "Regular"
# De 15,5 al 16,4 "Eficiente"
# De 16,5 al 19,4 "Excelente"
# Mayor a 19 "Sobresaliente"

numero = int(input("Ingresa un número entre 1 y 20"))
msgIni = "El estudiante"
if numero >= 0 and numero <= 9.4:
    print(msgIni, "REPROBÓ con una calificación de", numero, "Puntos", sep=" ")
elif numero >= 9.5 and numero <= 14.4:
    print(
        msgIni,
        "ha pasado con una calificación DEFICIENTE de",
        numero,
        "Puntos",
        sep=" ",
    )
elif numero >= 14.5 and numero <= 15.4:
    print(
        msgIni, "ha pasado con una calificación REGULAR de", numero, "Puntos", sep=" "
    )
elif numero >= 15.5 and numero <= 16.4:
    print(
        msgIni, "ha pasado con una calificación EFICIENTE de", numero, "Puntos", sep=" "
    )
elif numero >= 16.5 and numero <= 19.4:
    print(
        msgIni, "ha pasado con una calificación EXCELENTE de", numero, "Puntos", sep=" "
    )
elif numero > 19:
    print(
        msgIni,
        "ha pasado con una calificación SOBRESALIENTE de",
        numero,
        "Puntos",
        sep=" ",
    )
else:
    print(
        "La ncalificación ingresada no está dentro del rango permitido.",
        "Puntos",
        sep=" ",
    )
