class ContatoVO:
    def __init__(self, id_contato: int, nome: str, telefone: str, email: str = ""):
        self.id = id_contato
        self.nome = nome
        self.telefone = telefone
        self.email = email