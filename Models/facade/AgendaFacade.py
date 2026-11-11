from Controller.observer.Observer import Subject
from Models.BO.agenda_bo import AgendaBo
from memento.AgendaCaretaker import AgendaCaretaker


class AgendaFacade(Subject):

    def __init__(self, fabrica, nome_agenda: str = "Pessoal"):
        super().__init__()
        self._nome_agenda = nome_agenda
        self.agenda_bo = AgendaBo(nome_agenda, fabrica) # Injeta a fábrica na camada de negócio
        self.caretaker = AgendaCaretaker(30)

    def importar_contatos(self):
        resultado = self.agenda_bo.executar_importacao()
        if resultado:
            self.notificar("importar_contatos")
        else:
            self.notificar("importar_contatos_sem_sucesso")
        return resultado

    def adicionar_contato(self, contatoVO):
        memento = self.agenda_bo.criar_memento()
        retorno = self.agenda_bo.adicionar_contato(contatoVO)

        if isinstance(retorno, str):
            self.notificar("contato_existente", retorno)
            return None

        self.caretaker.salvar(memento)
        self.notificar("contato_adicionado", contatoVO)
        return contatoVO

    def excluir_contato(self, id_contato):
        memento = self.agenda_bo.criar_memento()
        resultado = self.agenda_bo.excluir_contato(id_contato)

        # Só salva o Memento e notifica se houve exclusão
        if not resultado:
            return False
        self.caretaker.salvar(memento)
        self.notificar("contato_excluido", id_contato)
        return True

    def desfazer_alteracoes(self) -> bool:
        memento_anterior = self.caretaker.desfazer()
        if memento_anterior is None:
            self.notificar("erro_memento")
            return False

        self.agenda_bo.restaurar_memento(memento_anterior)
        self.notificar("sucesso_memento")
        return True

    def listar_contatos(self):
        resultado = self.agenda_bo.listar_contatos()
        self.notificar("contatos_listados", self._nome_agenda)
        return resultado

    def buscar_contatos(self, contato):
        self.notificar("buscar_contatos", self._nome_agenda)
        return self.agenda_bo.buscar_contatos(contato)

    def alternar_agenda(self, nome_agenda):
        resultado = self.agenda_bo.alternar_agenda(nome_agenda)
        if resultado:
            self._nome_agenda = nome_agenda
            self.notificar("alternar_agenda", nome_agenda)
        return resultado