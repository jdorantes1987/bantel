from re import findall

class VerificadorDocumento():
    def __init__(self, documento) -> None:
        self.documento = documento
    
    def __es_persona_juridica(self):
        return str(self.__extraer_letras(self.documento)).upper() in ['J', 'G']
    
    def __es_persona_natural(self):
        return str(self.__extraer_letras(self.documento)).upper() in ['V', 'E']
    
    def __get_letra(self):
        return self.__extraer_letras(self.documento)
    
    def __es_documento_valido(self):
        es_persona_juridica = self.__es_persona_juridica()
        es_persona_natural = self.__es_persona_natural()
        es_dimension_valida = (len(self.documento) <= 10 and es_persona_natural) or \
                              (len(self.documento) == 10 and es_persona_juridica) 
        tiene_letra = len(self.__get_letra())
        tiene_mas_de_una_letra =  tiene_letra > 1
        # esta opción permite validar en caso de que no se coloque niguna letra saber si es un número válido, 
        # se entiende que es una cedula V
        es_valido_sin_letras = len(self.__extraer_numeros(self.documento)) > 4 and len(self.__extraer_numeros(self.documento)) <= 8 and not tiene_letra
        return (not tiene_mas_de_una_letra and es_dimension_valida) or es_valido_sin_letras
    
    def __extraer_letras(self, documento):
        # Patrón que coincide solo con letras
        patron = r'[a-zA-Z]'
        return ''.join(findall(patron, documento))
    
    def __extraer_numeros(self, cadena):
        # retorna los números de la List Comprehension 
        return ''.join([caracter for caracter in cadena if caracter.isdigit()])
    
    def get_documento_formateado(self):
        documento_formatado = self.documento
        es_documento_valido = self.__es_documento_valido()
        tiene_letra = len(self.__get_letra()) > 0
        if es_documento_valido:
            if not tiene_letra:
               documento_formatado = f"V{str(self.documento).zfill(8)}" 
        else:
               documento_formatado = 'n/e'           
        return documento_formatado
        
    def imprime(self):
        return self.get_documento_formateado()
        
            
if __name__ == '__main__' :
    print(VerificadorDocumento('18329114').imprime())

