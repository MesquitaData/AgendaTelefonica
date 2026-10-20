from random import Random
from Models.BO import agenda_bo
from Models.BO.agenda_bo import AgendaBo
from Models.DAO.AgendaDAO import AgendaDAO
from Models.VO.ContatoVO import ContatoVO
from Models.observer.Observer import Subject
from Models.Adapter.txtContatoAdapter import TXTContatoAdapter

class AgendaFacade(Subject):
    def __init__(self, nome_agenda: str = "Pessoal"):
        super().__init__()
        self._nome_agenda = nome_agenda
        self._agenda_bo = None
    #     self._dao = None
    #     self._agenda_ativa = self.dao.obter_agenda(nome_agenda)
    #
    # @property
    # def dao(self):
    #     if self._dao is None:
    #         self._dao = AgendaDAO()
    #     return self._dao

    @property
    def agenda_bo(self):
        if self._agenda_bo is None:
            self._agenda_bo = AgendaBo(self._nome_agenda)
        return self._agenda_bo

    def importar_contatos_txt(self, caminho_arquivo):
        try:
            adapter = TXTContatoAdapter()
            contatos = adapter.adaptar(caminho_arquivo)

            if not contatos:
                return False

            # Adiciona cada contato utilizando as regras e a persistência já existentes no sistema.
            for contato in contatos:
                resultado = self.adicionar_contato(contato.nome,contato.telefone,contato.email)

                # Se houver erro de validação ou inclusão, interrompe a importação.
                if isinstance(resultado, str) or not resultado:
                    return False

            return True

        except (OSError, ValueError, KeyError, TypeError):
            return False

    def adicionar_contato(self, nome, telefone, email):
        # if not nome or not telefone:
        #     return False
        #
        # proximo_id = Random.randint(self,1000, 9999)
        # novo_contato = ContatoVO(proximo_id, nome, telefone, email)
        # self._agenda_ativa.contatos.append(novo_contato)
        # self.dao.salvar_agenda(self._agenda_ativa)

        novo_contato: ContatoVO = self.agenda_bo.adicionar_contato(nome, telefone, email)

        # Se o Business Object retornar uma mensagem de erro,
        # não notifica os observadores.
        if isinstance(novo_contato, str):
            return novo_contato

        if not novo_contato:
            return False

        self.notificar("contato_adicionado", novo_contato)
        return novo_contato

    def excluir_contato(self, id_contato):
        # contatos_filtrados = [c for c in self._agenda_ativa.contatos if c.id != id_contato]
        #
        # if len(self._agenda_ativa.contatos) == len(contatos_filtrados):
        #     return False
        #
        # self._agenda_ativa.contatos = contatos_filtrados
        # self.dao.salvar_agenda(self._agenda_ativa)

        # O OBSERVER ENTRA AQUI: Notifica que um contato foi removido

        self.agenda_bo.excluir_contato(id_contato)

        self.notificar("contato_excluido", id_contato)
        return True

    # Métodos de listagem e busca não alteram o estado, então não precisam notificar
    def listar_contatos(self):
        return self.agenda_bo.listar_contatos()

    def buscar_contatos(self, termo):
        termo = termo.lower()
        return self.agenda_bo.buscar_contatos(termo)
