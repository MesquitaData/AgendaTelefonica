from Controller.Validadores.ValidarNome import ValidarNome
from Controller.Validadores.ValidarEmail import ValidarEmail
from Controller.Validadores.ValidarNumero import ValidarNumero

def criar_cadeia():
    nome = ValidarNome()
    email = ValidarEmail()
    numero = ValidarNumero()

    nome.set_proximo(numero).set_proximo(email)

    return nome