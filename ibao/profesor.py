import persona as p


class Profesor(p.Persona):
    def __init__(
        self, cedula, nombre, apellido, edad, telefono, direccion, asignaturas
    ):
        super().__init__(cedula, nombre, apellido, edad, telefono, direccion)
        self.asignaturas = asignaturas
