from Models.facade.AgendaFacade import AgendaFacade
from Models.observer.Observer import Observer
from Models.command.Invocador import Invocador
from Models.command.ListarContatosCommand import ListarContatosCommand
from Models.command.ExcluirContatoCommand import ExcluirContatoCommand

class AgendaController:  # Herda de Subject
    def __init__(self, nome_agenda="Pessoal"):
        super().__init__()  # Inicializa a lista de observadores
        self.agenda_facade = AgendaFacade(nome_agenda=nome_agenda)

    def inscrever_observador(self, observador: Observer):
        self.agenda_facade.inscrever(observador)

    def desiscrever_observador(self, observador: Observer):
        self.agenda_facade.inscrever(observador)

    def importar_contatos_txt(self, caminho_arquivo):
        return self.agenda_facade.importar_contatos_txt(caminho_arquivo)

    def adicionar_contato(self,  nome, telefone, idade, email):
        return self.agenda_facade.adicionar_contato( nome, telefone, idade, email)

    # Implementando o padrão command para encapsular as funcionalidades de excluir e listar contatos
    def excluir_contato(self, id_contato):
        invocador = Invocador()
        comando = ExcluirContatoCommand(self.agenda_facade,id_contato)
        invocador.definir_comando(comando)
        return invocador.executar_comando()

    def listar_contatos(self):
        invocador = Invocador()
        comando = ListarContatosCommand(self.agenda_facade)
        invocador.definir_comando(comando)
        return invocador.executar_comando()

    def buscar_contatos(self, item=None, idade=0):
        return self.agenda_facade.buscar_contatos(item, idade)

