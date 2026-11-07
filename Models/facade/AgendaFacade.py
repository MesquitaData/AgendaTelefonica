from Models.BO.agenda_bo import AgendaBo
from Models.decorate.decorates import FiltrarPorNome, FiltrarPorTelefone, BuscarTodosContatos, FiltrarPorEmail
from Controller.observer.Observer import Subject

class AgendaFacade(Subject):
    def __init__(self, nome_agenda: str = "Pessoal"):
        super().__init__()
        self._nome_agenda = nome_agenda
        self.agenda_bo = AgendaBo(self._nome_agenda)

    def importar_contatos_facade(self):
        self.notificar("importar_contatos")
        return self.agenda_bo.importar_contatos_bo()

    def adicionar_contato(self,contatoVO):
        retorno = self.agenda_bo.adicionar_contato(contatoVO)
        # Se o Business Object retornar uma mensagem de erro, notifica aos observadores(controller)
        # que esse contato telefônico já existe na agenda!!!
        if isinstance(retorno, str):
            self.notificar("contato_existente",contatoVO)
            return

        # Os observadores podem executar ações específicas quando recebem essa notificação.
        self.notificar("contato_adicionado", contatoVO) # Aplicação padrão observer
        return contatoVO

    def excluir_contato(self, id_contato):
        self.agenda_bo.excluir_contato(id_contato) # Encaminha a solicitação para a camada de negócio.

        if self.agenda_bo:
            # Os observadores podem executar ações específicas quando recebem essa notificação.
            self.notificar("contato_excluido", id_contato) # Implementação padrão observer
            return True

        return False

    # Métodos de listagem e busca não alteram o estado, então não precisam notificar
    def listar_contatos(self):
        self.notificar("contatos_listados",self._nome_agenda)
        return self.agenda_bo.listar_contatos() # Encaminha a solicitação para a camada de negócio.

    def buscar_contatos(self, nome=None, telefone=None, email=None):
        self.notificar("buscar_contatos",self._nome_agenda)
        busca = BuscarTodosContatos(self.agenda_bo) # Implementação do padrão decorator

        if nome:
            busca = FiltrarPorNome(busca, nome)
        if telefone:
            busca = FiltrarPorTelefone(busca, telefone)
        if email:
            busca = FiltrarPorEmail(busca, email)

        return busca.buscar() # Entregar à camada que a chamou a lista de contatos encontrados

    def alternar_agenda(self, nome_agenda):
        self.notificar("alternar_agenda")
        return self.agenda_bo.alternar_agenda(nome_agenda)