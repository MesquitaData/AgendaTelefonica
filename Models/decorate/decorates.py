# Componente Base
from abc import ABC, abstractmethod

from Models.BO.agenda_bo import AgendaBo


class BuscarComponent(ABC):

    @abstractmethod
    def buscar(self): pass

class BuscarTodosContatos(BuscarComponent):

    def __init__(self, agenda_bo:AgendaBo):
        self.contatos = agenda_bo.listar_contatos()

    def buscar(self):
        return self.contatos


# Decorator base
class FiltroDecorator(BuscarComponent):
    def __init__(self, component: BuscarComponent):
        self.componente = component

    def buscar(self):
        return self.componente.buscar()

class FiltrarPorNome(FiltroDecorator):
    def __init__(self, component: BuscarComponent, nome: str):
        super().__init__(component)
        self.nome = nome

    def buscar(self):
        contatos = super().buscar()
        return [contato for contato in contatos if self.nome in contato.nome.lower()]


class FiltrarPorEmail(FiltroDecorator):
    def __init__(self, component: BuscarComponent, email: str):
        super().__init__(component)
        self.email = email

    def buscar(self):
        contatos = super().buscar()
        return [contato for contato in contatos if self.email == contato.email]


class FiltrarPorTelefone(FiltroDecorator):
    def __init__(self, component: BuscarComponent, telefone: str):
        super().__init__(component)
        self.telefone = telefone

    def buscar(self):
        contatos = super().buscar()
        return [contato for contato in contatos if self.telefone == contato.telefone]


