import random
from Models.DAO.AgendaDAO import AgendaDAO
from Models.VO.ContatoVO import ContatoVO
from Validadores.ValidarNome import ValidarNome
from Controller.Validadores.ValidarNumero import ValidarNumero
from Controller.Validadores.ValidarEmail import ValidarEmail
from Controller.Validadores.ValidarDuplicidade import ValidarDuplicidade
from Models.decorate.decorates import FiltrarPorNome, FiltrarPorTelefone, BuscarTodosContatos, FiltrarPorEmail

class AgendaBo:
    def __init__(self, nome_agenda):
        self._dao = None
        self._agenda_ativa = self.dao.obter_agenda(nome_agenda)

    @property
    def dao(self):
        if self._dao is None:
            self._dao = AgendaDAO()
        return self._dao

    def adicionar_contato(self, contatoVO):
        nome_validar = ValidarNome()
        numero_validar = ValidarNumero()
        email_validar = ValidarEmail()
        duplicidade_validar = ValidarDuplicidade(self._agenda_ativa.contatos)

        nome_validar.set_proximo(numero_validar).set_proximo(email_validar).set_proximo(duplicidade_validar)

        erro = nome_validar.validar(contatoVO) # validação em cadeia a partir da validação de nome
        if erro:
            return "Dados inválidos ou contato já existente!"

        # Se passou por toda a cadeia com sucesso, persiste os dados
        telefone = contatoVO.telefone
        contatoVO.telefone = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}" # Formatação do telefone
        contatoVO.id = len(self._agenda_ativa.contatos) + 1
        self._agenda_ativa.contatos.append(contatoVO)
        self.dao.salvar_agenda(self._agenda_ativa)
        return True

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
    def buscar_contatos_decorator(self, contato):
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

    def busca_contato(self,parametro):
        for contato in self._agenda_ativa.contatos:
            if parametro == contato.telefone: return True
        return False
        # return [c for c in self._agenda_ativa.contatos if parametro is not c.telefone]

    def importar_contatos_bo(self):
        contatos = self.dao.importar_contatos_dao()
        if not contatos:
            return False
        for contato in contatos:
            # telefone_existe = self.busca_contato(contato.telefone) # Verifica se o telefone já existe na agenda ativa
            if self.busca_contato(contato.telefone): continue
            resultado = self.adicionar_contato(contato)
            if resultado is not True: return False

        return True