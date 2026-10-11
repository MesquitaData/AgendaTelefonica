from Models.AgendaDAO import AgendaDAO
from Models.ContatoVO import ContatoVO

class Observer:
    """Interface que todo observador deve implementar."""
    def atualizar(self, evento: str, dados=None):
        pass

class Subject:
    """Classe base para quem deseja ser observado (gerencia as assinaturas)."""
    def __init__(self):
        self._observadores = []

    def inscrever(self, observador: Observer):
        if observador not in self._observadores:
            self._observadores.append(observador)

    def desinscrever(self, observador: Observer):
        self._observadores.remove(observador)

    def notificar(self, evento: str, dados=None):
        for observador in self._observadores:
            observador.atualizar(evento, dados)


class AgendaController(Subject):  # Herda de Subject
    def __init__(self, nome_agenda="Pessoal"):
        super().__init__()  # Inicializa a lista de observadores
        self.dao = AgendaDAO()
        self.agenda_ativa = self.dao.obter_agenda(nome_agenda)

    def adicionar_contato(self, nome, telefone, email=""):
        if not nome or not telefone:
            return False

        proximo_id = max([c.id for c in self.agenda_ativa.contatos], default=0) + 1
        novo_contato = ContatoVO(proximo_id, nome, telefone, email)
        self.agenda_ativa.contatos.append(novo_contato)
        self.dao.salvar_agenda(self.agenda_ativa)

        # O OBSERVER ENTRA AQUI: Notifica que um contato foi adicionado
        self.notificar("contato_adicionado", novo_contato)
        return True

    def excluir_contato(self, id_contato):
        contatos_filtrados = [c for c in self.agenda_ativa.contatos if c.id != id_contato]

        if len(self.agenda_ativa.contatos) == len(contatos_filtrados):
            return False

        self.agenda_ativa.contatos = contatos_filtrados
        self.dao.salvar_agenda(self.agenda_ativa)

        # O OBSERVER ENTRA AQUI: Notifica que um contato foi removido
        self.notificar("contato_excluido", id_contato)
        return True

    # Métodos de listagem e busca não alteram o estado, então não precisam notificar
    def listar_contatos(self):
        return self.agenda_ativa.contatos

    def buscar_contatos(self, termo):
        termo = termo.lower()
        return [
            c for c in self.agenda_ativa.contatos
            if termo in c.nome.lower() or termo in c.telefone
        ]

