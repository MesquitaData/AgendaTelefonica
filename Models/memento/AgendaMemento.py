import copy


class AgendaMemento:
    def __init__(self, contatos: list):
        self._contatos = copy.deepcopy(contatos)

    @property
    def contatos(self):
        return copy.deepcopy(self._contatos)
