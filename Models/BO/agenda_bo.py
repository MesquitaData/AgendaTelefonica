from Controller.Validadores.ValidarEmail import ValidarEmail
from Controller.Validadores.ValidarNumero import ValidarNumero
from Models.DAO.AgendaDAO import AgendaDAO
from Models.memento.AgendaMemento import AgendaMemento
from Validadores.ValidarDuplicidade import ValidarDuplicidade
from Validadores.ValidarNome import ValidarNome


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
        return AgendaMemento(self._agenda_ativa)

    def restaurar_memento(self, memento: AgendaMemento) -> None:
        self._agenda_ativa.memento = memento
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
    def buscar_contatos(self, termo):
         return [c for c in self._agenda_ativa.contatos if termo in c.nome.lower() or termo in c.telefone]

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
        if not contatos:
            return False
        for contato in contatos:

            # Verifica se o telefone já existe na agenda ativa
            telefone_existe = self.buscar_contatos(contato.telefone)
            if telefone_existe: continue
            resultado = self.adicionar_contato(contato)
            if resultado is not True: return False

        return True