# Classe mãe que implementa um processo de validacao
class Validador:
    def __init__(self):
        self.proximo = None

    def set_proximo(self, proximo):
        self.proximo = proximo
        return proximo

    def validar(self, contato):
        erro = self.verificar(contato)

        if erro:
            return erro

        if self.proximo:
            return self.proximo.validar(contato)

        return None

    def verificar(self, contato):
        raise NotImplementedError()
