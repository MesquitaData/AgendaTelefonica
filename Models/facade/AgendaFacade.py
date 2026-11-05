from random import Random
from Models.BO import agenda_bo
from Models.BO.agenda_bo import AgendaBo
from Models.DAO.AgendaDAO import AgendaDAO
from Models.VO.ContatoVO import ContatoVO
from Models.decorate.decorates import FiltrarPorNome, FiltrarPorTelefone, BuscarTodosContatos, FiltrarPorEmail, \
    FiltrarPorIdade
from Models.observer.Observer import Subject
from Models.Adapter.txtContatoAdapter import TXTContatoAdapter

class AgendaFacade(Subject):
    def __init__(self, nome_agenda: str = "Pessoal"):
        super().__init__()
        self._nome_agenda = nome_agenda
        self._agenda_bo = None  # Lazy Loading

    # Sua finalidade é controlar a criação do objeto AgendaBo, evitando instanciá-lo desnecessariamente.
    # Isso significa que, depois da primeira criação, as próximas chamadas reutilizam o mesmo objeto.
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
                resultado = self.adicionar_contato(contato.nome,contato.telefone, contato.idade, contato.email)

                # Se houver erro de validação ou inclusão, interrompe a importação.
                if isinstance(resultado, str) or not resultado:
                    return False

            return True

        except (OSError, ValueError, KeyError, TypeError):
            return False

    def adicionar_contato(self, nome, telefone, idade, email):
        novo_contato: ContatoVO = self.agenda_bo.adicionar_contato(nome, telefone, idade, email)

        # Se o Business Object retornar uma mensagem de erro,
        # não notifica os observadores.
        if isinstance(novo_contato, str):
            return novo_contato

        if not novo_contato:
            return False

        # Os observadores podem executar ações específicas quando recebem essa notificação.
        self.notificar("contato_adicionado", novo_contato)
        return novo_contato

    def excluir_contato(self, id_contato):
        self.agenda_bo.excluir_contato(id_contato) # Encaminha a solicitação para a camada de negócio.

        if self.agenda_bo:
            # Os observadores podem executar ações específicas quando recebem essa notificação.
            self.notificar("contato_excluido", id_contato) # Implementação padrão observer
            return True

        return False

    # Métodos de listagem e busca não alteram o estado, então não precisam notificar
    def listar_contatos(self):
        return self.agenda_bo.listar_contatos() # Encaminha a solicitação para a camada de negócio.

    def buscar_contatos(self, nomeemailtelefone=None, idade=0):
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