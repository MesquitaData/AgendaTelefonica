class AgendaVO:
    def __init__(self, nome_agenda,dao):
        self.nome = nome_agenda
        self.dao = dao
        self._contatos = None  # Lazy Initialization

    @property
    def contatos(self):
        if self._contatos is None:
            self._contatos = self.dao.obter_contatos(self.nome)
        return self._contatos