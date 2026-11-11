from abc import ABC, abstractmethod

class AgendaDAO(ABC):

    @abstractmethod
    def obter_agenda(self, nome_agenda, dao): pass

    @abstractmethod
    def salvar_agenda(self, nome_agenda): pass

    @abstractmethod
    def obter_contatos(self, nome_agenda): pass

    @abstractmethod
    def ler_arquivo(self): pass

    @abstractmethod
    def importar_contatos(self, nome_agenda): pass

    @abstractmethod
    def criar_agenda(self): pass