from abc import ABC, abstractmethod

class AgendaDAO(ABC):

    @abstractmethod
    def obter_agenda(self, nome_agenda, contato_dao): pass

    @abstractmethod
    def salvar_agenda(self, nome_agenda): pass