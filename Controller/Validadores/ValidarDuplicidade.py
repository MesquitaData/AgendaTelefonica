from Controller.Validadores.ValidarNome import ValidarNome
from Controller.Validadores.ValidarEmail import ValidarEmail
from Controller.Validadores.ValidarNumero import ValidarNumero
from Controller.Validadores.Validador import Validador

class ValidarDuplicidade(Validador):
    def __init__(self, contatos_existentes):
        super().__init__()
        self.contatos_existentes = contatos_existentes

    def verificar(self, contato):
        for c in self.contatos_existentes:
            if c.telefone.strip() == contato.telefone.strip():
                return "Contato já cadastrado"
        return None  # Nenhum erro encontrado, segue para o próximo