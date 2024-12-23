import persona as p


class Estudiante(p.Persona):
    def __init__(
        self, cedula, nombre, apellido, edad, telefono, direccion, materias, estatus
    ):
        super().__init__(cedula, nombre, apellido, edad, telefono, direccion)
        self.materias = materias
        self.estatus = estatus


estudiante1 = Estudiante(
    "15152791", "Mirtha", "Graterol", 42, "04146126353", "Catia", "Seguros", "A"
)
print(estudiante1.materias)
print(Estudiante.mro())  # Metodo de resolucion de orden en herencia
print(isinstance(estudiante1, p.Persona))
