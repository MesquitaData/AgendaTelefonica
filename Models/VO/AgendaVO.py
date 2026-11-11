class AgendaVO:
    def __init__(self, nome_agenda,contatos_dao):
        self.nome = nome_agenda
        self.dao = contatos_dao
        self._contatos = None  # Lazy Initialization

    @property
    def contatos(self):
        if self._contatos is None:
            self._contatos = self.dao.obter_contatos(self.nome)
        return self._contatos

    # Esse metodo será executado quando alguém atribuir um valor à propriedade
    # property contatos, preenchendo o atributo interno self._contatos
    @contatos.setter
    def contatos(self, contatos):
        self._contatos = contatos