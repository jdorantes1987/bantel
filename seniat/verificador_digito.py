from seniat.verificador_documento import VerificadorDocumento


class VerificadorDigito:
    def __init__(self, documento) -> None:
        self.documento_formateado = VerificadorDocumento(
            documento
        ).get_documento_formateado()

    def get_rif(self):
        doc = self.documento_formateado
        no_existe = "n/e"
        es_documento_valido = doc != no_existe
        if es_documento_valido:
            letra_rif = doc[:1]
            match letra_rif:
                case "V":
                    tipo = 1
                case "E":
                    tipo = 2
                case "J":
                    tipo = 3
            formula = 11 - (
                (
                    tipo * 4
                    + int(doc[1:2]) * 3
                    + int(doc[2:3]) * 2
                    + int(doc[3:4]) * 7
                    + int(doc[4:5]) * 6
                    + int(doc[5:6]) * 5
                    + int(doc[6:7]) * 4
                    + int(doc[7:8]) * 3
                    + int(doc[8:9]) * 2
                )
                % 11
            )
            digito_verificador = (
                formula
                if (letra_rif == "V" and formula <= 9)
                or (letra_rif in ["J", "E"] and formula < 10)
                else 0
            )
            rif = doc + str(digito_verificador) if len(doc) == 9 else doc
            return (
                rif
                if rif[-1] == str(digito_verificador)
                else "Error en dígito verificador"
            )
        else:
            return no_existe


if __name__ == "__main__":
    print(VerificadorDigito("J000792240").get_rif())
