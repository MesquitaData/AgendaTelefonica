from Models.AbstractFactory.FabricaAgendasDAO import FabricaAgendaDAO
from Models.DAO.JSONAgendaDAO import JSONAgendaDAO
from Models.DAO.JSONContatoDAO import JSONContatoDAO

class JSONDAOFactory(FabricaAgendaDAO):

    def criar_agenda_dao(self): return JSONAgendaDAO()

    def criar_contato_dao(self): return JSONContatoDAO()