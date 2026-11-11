from abc import ABC, abstractmethod
from Models.DAO.JSONAgendaDAO import JSONAgendaDAO
from Models.DAO.TXTAgendaDAO import TXTAgendaDAO

class FabricaAgendaDAO(ABC):
    @abstractmethod
    def criar_agenda_dao(self): pass

class JSONDAOFactory(FabricaAgendaDAO):
    def criar_agenda_dao(self): return JSONAgendaDAO()

class TXTDAOFactory(FabricaAgendaDAO):
    def criar_agenda_dao(self): return TXTAgendaDAO()