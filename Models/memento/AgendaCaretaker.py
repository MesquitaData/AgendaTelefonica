from collections import deque
from Models.memento.AgendaMemento import AgendaMemento

class AgendaCaretaker:
    def __init__(self, limite_historico:int = 10):
        self._pilha_desfazer = deque(maxlen=limite_historico)

    def salvar(self, memento: AgendaMemento) -> None:
        self._pilha_desfazer.append(memento)

    def desfazer(self) -> AgendaMemento | None:
        if not self._pilha_desfazer:
            return None
        return self._pilha_desfazer.pop()