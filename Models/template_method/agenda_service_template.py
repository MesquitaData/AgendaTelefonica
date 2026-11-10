from abc import ABC, abstractmethod

from Models.VO.ContatoVO import ContatoVO


class AgendaServiceTemplate(ABC):

     @abstractmethod
     def adicionar_contato(self, contato: ContatoVO): pass

     @abstractmethod
     def excluir_contato(self, id_contato: int): pass

     @abstractmethod
     def buscar_contato(self, contato: ContatoVO): pass

     @abstractmethod
     def listar_contatos(self): pass

     @abstractmethod
     def alternar_agendas(self, nome_agenda: str): pass

     @abstractmethod
     def importar_contatos(self): pass