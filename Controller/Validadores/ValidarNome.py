from Validadores import Validador
import unicodedata

class ValidarNome(Validador.Validador):
    def verificar(self, contato):
        nome = contato.nome

        if not nome or not nome.strip():
            return "O nome do contato é obrigatório."

        for caractere in nome:
            if caractere == " ":
                continue

            categoria = unicodedata.category(caractere)

            # Aceita letras Unicode, incluindo letras acentuadas.
            if categoria not in ("Lu", "Ll", "Lt", "Lm", "Lo"):
                return (
                    "O nome deve conter apenas letras "
                    "e espaços, incluindo acentos."
                )

        return None