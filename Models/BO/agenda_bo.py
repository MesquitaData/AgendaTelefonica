from Controller.Validadores.ValidarEmail import ValidarEmail
from Controller.Validadores.ValidarNumero import ValidarNumero
from Models.memento.AgendaMemento import AgendaMemento
from Validadores.ValidarDuplicidade import ValidarDuplicidade
from Validadores.ValidarNome import ValidarNome
from Controller.Validadores.ValidarNumero import ValidarNumero
from Controller.Validadores.ValidarEmail import ValidarEmail
from Controller.Validadores.ValidarDuplicidade import ValidarDuplicidade
from Models.decorate.decorates import FiltrarPorNome, FiltrarPorTelefone, BuscarTodosContatos, FiltrarPorEmail
from Models.Adapter.ContatoAdapter import *

class AgendaBo:

    def __init__(self, nome_agenda, fabrica):
        # A fábrica fornece os DAOs concretos
        self.agenda_dao = fabrica.criar_agenda_dao()
        # self.contato_dao = fabrica.criar_contato_dao()

        # O ContatoDAO é injetado na AgendaVO para permitir Lazy Loading
        self._agenda_ativa = self.agenda_dao.obter_agenda(nome_agenda)

        # Cria a agenda caso ela ainda não exista
        if self._agenda_ativa is None:
            self.agenda_dao.salvar_agenda(nome_agenda,[])
            self._agenda_ativa = self.agenda_dao.obter_agenda(nome_agenda)

    def _salvar_contatos(self):
        # Centraliza a persistência dos contatos da agenda ativa.
        self.agenda_dao.salvar_agenda(self._agenda_ativa.nome,self._agenda_ativa.contatos)

    def criar_memento(self) -> AgendaMemento:
        return AgendaMemento(self._agenda_ativa.contatos)

    def restaurar_memento(self, memento: AgendaMemento) -> None:
        self._agenda_ativa.contatos = memento.contatos
        self._salvar_contatos()

    def adicionar_contato(self, contatoVO):
        nome_validar = ValidarNome()
        numero_validar = ValidarNumero()
        email_validar = ValidarEmail()
        duplicidade_validar = ValidarDuplicidade(self._agenda_ativa.contatos)

        nome_validar.set_proximo(numero_validar).set_proximo(email_validar).set_proximo(duplicidade_validar)

        erro = nome_validar.validar(contatoVO)
        if erro:
            return "Dados inválidos ou contato já existente!"

        contatoVO.id = len(self._agenda_ativa.contatos) + 1
        self._agenda_ativa.contatos.append(contatoVO)
        self._salvar_contatos()

        return None

    def excluir_contato(self, id_contato):

        contatos_filtrados = [
            c for c in self._agenda_ativa.contatos
            if c.id != id_contato
        ]

        if len(self._agenda_ativa.contatos) == len(contatos_filtrados):
            return False

        # Utiliza o setter da propriedade contatos da AgendaVO
        self._agenda_ativa.contatos = contatos_filtrados

        # Reajusta os IDs dos contatos
        for novo_id, contato in enumerate(self._agenda_ativa.contatos, start=1): contato.id = novo_id

        self._salvar_contatos()
        return True

    def buscar_contatos(self, contato):
        busca = BuscarTodosContatos(self)
        if contato.telefone:
            busca = FiltrarPorTelefone(busca, contato.telefone)

        if contato.nome:
            busca = FiltrarPorNome(busca, contato.nome)

        if contato.email:
            busca = FiltrarPorEmail(busca, contato.email)

        return busca.buscar()

    def listar_contatos(self):
        return self._agenda_ativa.contatos # Aproveita o Lazy Loading e o cache da AgendaVO

    def alternar_agenda(self, nome_agenda):
        nova_agenda = self.agenda_dao.obter_agenda(nome_agenda)
        if nova_agenda is None:
            return False
        self._agenda_ativa = nova_agenda
        return True

    def importar_contatos_bo(self):
        contatos = self.agenda_dao.importar_contatos(self._agenda_ativa.nome)
        if not contatos: return False
        adicionados = 0
        for contato in contatos:
            resultado = self.adicionar_contato(contato)
            if resultado is None: adicionados += 1
        return adicionados > 0