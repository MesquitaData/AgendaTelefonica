from abc import ABC, abstractmethod

class FabricaAgendaDAO(ABC):

    @abstractmethod
    def criar_agenda_dao(self): pass

    @abstractmethod
    def criar_contato_dao(self): pass