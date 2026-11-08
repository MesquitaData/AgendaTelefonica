from Validadores import Validador
import re

class ValidarNumero(Validador.Validador):
    def verificar(self, contato):
        telefone = contato.telefone or ""

        if not re.fullmatch(r"[0-9()+\-\s]+", telefone):
            return "O telefone contém caracteres inválidos."

        digitos = re.sub(r"\D", "", telefone)

        if len(digitos) != 11:
            return "O telefone deve ter 11 dígitos."

        return None