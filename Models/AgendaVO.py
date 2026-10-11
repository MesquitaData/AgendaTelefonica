class AgendaVO:
    def __init__(self, nome_agenda, contatos=None):
        self.nome = nome_agenda
        self.contatos = contatos if contatos is not None else []