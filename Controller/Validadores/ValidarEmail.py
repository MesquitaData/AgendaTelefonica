from Validadores import Validador
import re

class ValidarEmail(Validador.Validador):
    def verificar(self, contato):
        email = contato.email or " "

        # O e-mail é opcional.
        if not email.strip():
            return None

        padrao = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.fullmatch(padrao, email):
            return "O e-mail informado não é válido."

        return None