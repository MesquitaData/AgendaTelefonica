from Models.AbstractFactory.FabricaAgendasDAO import FabricaAgendaDAO
from Models.DAO.TXTAgendaDAO import TXTAgendaDAO
from Models.DAO.TXTContatoDAO import TXTContatoDAO

class TXTDAOFactory(FabricaAgendaDAO):

    def criar_agenda_dao(self):return TXTAgendaDAO()

    def criar_contato_dao(self): return TXTContatoDAO()