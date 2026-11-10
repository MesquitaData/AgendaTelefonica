from abc import ABC, abstractmethod

class ContatoDAO(ABC):

    @abstractmethod
    def obter_contatos(self, nome_agenda): pass

    @abstractmethod
    def salvar_contatos(self, nome_agenda, contatos): pass

    @abstractmethod
    def importar_contatos(self,nome_agenda): pass