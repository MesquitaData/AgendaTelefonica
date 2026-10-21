from Models.facade.AgendaFacade import AgendaFacade
from Models.observer.Observer import Observer


class AgendaController:  # Herda de Subject
    def __init__(self, nome_agenda="Pessoal"):
        super().__init__()  # Inicializa a lista de observadores
        self.agenda_facade = AgendaFacade(nome_agenda=nome_agenda)

    def inscrever_observador(self, observador: Observer):
        self.agenda_facade.inscrever(observador)

    def desiscrever_observador(self, observador: Observer):
        self.agenda_facade.inscrever(observador)

    def adicionar_contato(self, nome, telefone, email=""):
        return self.agenda_facade.adicionar_contato(nome, telefone, email)

    def excluir_contato(self, id_contato):
        return self.agenda_facade.excluir_contato(id_contato)


    # Métodos de listagem e busca não alteram o estado, então não precisam notificar
    def listar_contatos(self):
        return self.agenda_facade.listar_contatos()

    def buscar_contatos(self, termo):
        return self.agenda_facade.buscar_contatos(termo)

