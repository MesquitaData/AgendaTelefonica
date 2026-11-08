from Models.BO.agenda_bo import AgendaBo
from Models.decorate.decorates import FiltrarPorNome, FiltrarPorTelefone, BuscarTodosContatos, FiltrarPorEmail, \
    FiltrarPorIdade
from Controller.observer.Observer import Subject
from memento.AgendaCaretaker import AgendaCaretaker


class AgendaFacade(Subject):
    def __init__(self, nome_agenda: str = "Pessoal"):
        super().__init__()
        self._nome_agenda = nome_agenda
        self.agenda_bo = AgendaBo(self._nome_agenda)
        self.caretaker = AgendaCaretaker(30)

    def importar_contatos_facade(self):
        self.notificar("importar_contatos")
        return self.agenda_bo.importar_contatos_bo()

    def adicionar_contato(self,contatoVO):
        memento = self.agenda_bo.criar_memento()
        retorno = self.agenda_bo.adicionar_contato(contatoVO)
        # Se o Business Object retornar uma mensagem de erro, notifica aos observadores(controller)
        # que esse contato telefônico já existe na agenda!!!
        if isinstance(retorno, str):
            self.notificar("contato_existente",contatoVO)
            return

        self.caretaker.salvar(memento)
        # Os observadores podem executar ações específicas quando recebem essa notificação.
        self.notificar("contato_adicionado", contatoVO) # Aplicação padrão observer
        return contatoVO

    def excluir_contato(self, id_contato):
        memento = self.agenda_bo.criar_memento()

        if self.agenda_bo:
            self.agenda_bo.excluir_contato(id_contato) # Encaminha a solicitação para a camada de negócio.
            self.caretaker.salvar(memento)
            # Os observadores podem executar ações específicas quando recebem essa notificação.
            self.notificar("contato_excluido", id_contato) # Implementação padrão observer
            return True

        return False

    def desfazer_alteracoes(self) -> bool:
        memento_anterior = self.caretaker.desfazer()
        if memento_anterior is None:
            self.notificar("erro_memento")
            return False
        self.agenda_bo.restaurar_memento(memento_anterior)
        self.notificar("sucesso_memento")
        return True

    # Métodos de listagem e busca não alteram o estado, então não precisam notificar
    def listar_contatos(self):
        self.notificar("contatos_listados",self._nome_agenda)
        return self.agenda_bo.listar_contatos() # Encaminha a solicitação para a camada de negócio.

    def buscar_contatos(self, nomeemailtelefone:str="", idade=0):
        busca = FiltrarPorIdade(BuscarTodosContatos(self.agenda_bo), idade=idade) \
            if idade != 0 else BuscarTodosContatos(self.agenda_bo) # Implementação do padrão decorator

        if nomeemailtelefone:
            nome = FiltrarPorNome(busca, nomeemailtelefone).buscar()
            email = FiltrarPorEmail(busca, nomeemailtelefone).buscar()
            telefone = FiltrarPorTelefone(busca, nomeemailtelefone).buscar()

            if len(nome): return nome

            if len(telefone): return telefone

            if len(email):return email

            return []
        return [] if idade == 0 else busca.buscar()

    def alternar_agenda(self, nome_agenda):
        self.notificar("alternar_agenda")
        return self.agenda_bo.alternar_agenda(nome_agenda)