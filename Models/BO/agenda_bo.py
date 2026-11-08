from Controller.Validadores.ValidarEmail import ValidarEmail
from Controller.Validadores.ValidarNumero import ValidarNumero
from Models.DAO.AgendaDAO import AgendaDAO
from Models.memento.AgendaMemento import AgendaMemento
from Validadores.ValidarDuplicidade import ValidarDuplicidade
from Validadores.ValidarNome import ValidarNome
from Controller.Validadores.ValidarNumero import ValidarNumero
from Controller.Validadores.ValidarEmail import ValidarEmail
from Controller.Validadores.ValidarDuplicidade import ValidarDuplicidade
from Models.decorate.decorates import FiltrarPorNome, FiltrarPorTelefone, BuscarTodosContatos, FiltrarPorEmail

class AgendaBo:
    def __init__(self, nome_agenda):
        self.dao = AgendaDAO()
        self._agenda_ativa = self.dao.obter_agenda(nome_agenda)

    # @property
    # def dao(self):
    #     if self._dao is None:
    #         self._dao = AgendaDAO()
    #     return self._dao

    def criar_memento(self) -> AgendaMemento:
        return AgendaMemento(self._agenda_ativa.contatos)

    def restaurar_memento(self, memento: AgendaMemento) -> None:
        self._agenda_ativa.contatos = memento.contatos
        self.dao.salvar_agenda(self._agenda_ativa)

    def adicionar_contato(self, contatoVO):
        nome_validar = ValidarNome()
        numero_validar = ValidarNumero()
        email_validar = ValidarEmail()
        duplicidade_validar = ValidarDuplicidade(self._agenda_ativa.contatos)

        nome_validar.set_proximo(numero_validar).set_proximo(email_validar).set_proximo(duplicidade_validar)

        erro = nome_validar.validar(contatoVO) # validação em cadeia a partir da validação de nome
        if erro:
            return "Dados inválidos ou contato já existente!"

        if len([c for c in self._agenda_ativa.contatos if contatoVO.nome in c.nome.lower() or contatoVO.telefone in c.telefone]) != 0:
            return "Este contanto já exite nesta agenda !"

        # Se passou por toda a cadeia com sucesso, persiste os dados
        contatoVO.id = len(self._agenda_ativa.contatos) + 1
        self._agenda_ativa.contatos.append(contatoVO)
        self.dao.salvar_agenda(self._agenda_ativa)
        return None

    def excluir_contato(self, id_contato):
        contatos_filtrados = [c for c in self._agenda_ativa.contatos if c.id != id_contato]

        if len(self._agenda_ativa.contatos) == len(contatos_filtrados):
            return False
        self._agenda_ativa.contatos = contatos_filtrados

        # Reajusta os IDs dos contatos
        for novo_id, contato in enumerate(self._agenda_ativa.contatos, start=1):
            contato.id = novo_id
        self.dao.salvar_agenda(self._agenda_ativa)
        return True

    # Métodos de listagem e busca não alteram o estado, então não precisam notificar
    def buscar_contatos(self, contato):
        busca = BuscarTodosContatos(self)  # Implementação do padrão decorator

        if contato.telefone:
            busca = FiltrarPorTelefone(busca, contato.telefone)
        if contato.nome:
            busca = FiltrarPorNome(busca, contato.nome)
        if contato.email:
            busca = FiltrarPorEmail(busca, contato.email)

        return busca.buscar()  # Entregar à camada que a chamou a lista de contatos encontrados

    # PROJETO TRANSFORMANDO EM DECORATOR
    def listar_contatos(self):
        return self._agenda_ativa.contatos

    def alternar_agenda(self, nome_agenda):
        nova_agenda = self.dao.obter_agenda(nome_agenda)
        if nova_agenda is None:
            return False
        self._agenda_ativa = nova_agenda
        return True

    def importar_contatos_bo(self):
        contatos = self.dao.importar_contatos_dao()
        adicionado = 0
        if not contatos: return False
        for contato in contatos:
            if not self.adicionar_contato(contato):
                adicionado+=1
                continue
        if adicionado != 0: return True
        return False