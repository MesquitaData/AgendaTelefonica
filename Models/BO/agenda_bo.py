import random
from Controller.Validadores.CadeiaResp import criar_cadeia
from Models.DAO.AgendaDAO import AgendaDAO
from Models.VO.ContatoVO import ContatoVO


class AgendaBo:
    def __init__(self, nome_agenda):
        self._dao = None
        self._agenda_ativa = self.dao.obter_agenda(nome_agenda)

    @property
    def dao(self):
        if self._dao is None:
            self._dao = AgendaDAO()
        return self._dao

    def adicionar_contato(self, nome, telefone, email):
        cadeia = criar_cadeia()
        if not nome or not telefone:
            return False
        id_contato = len(self._agenda_ativa.contatos) + 1  # Autoincremental
        novo_contato = ContatoVO(id_contato, nome, telefone, email)
        erro = cadeia.validar(novo_contato) # Chama da Chain of Responsability
        if erro:
            return erro
        self._agenda_ativa.contatos.append(novo_contato)
        self.dao.salvar_agenda(self._agenda_ativa)
        return novo_contato

    def excluir_contato(self, id_contato):
        contatos_filtrados = [c for c in self._agenda_ativa.contatos if c.id != id_contato]

        if len(self._agenda_ativa.contatos) == len(contatos_filtrados):
            return False

        self._agenda_ativa.contatos = contatos_filtrados
        self.dao.salvar_agenda(self._agenda_ativa)
        return None

    # Métodos de listagem e busca não alteram o estado, então não precisam notificar
    def listar_contatos(self):
        return self._agenda_ativa.contatos

    def buscar_contatos(self, termo):
        return [
            c for c in self._agenda_ativa.contatos
            if termo in c.nome.lower() or termo in c.telefone
        ]