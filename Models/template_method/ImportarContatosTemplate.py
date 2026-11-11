from abc import ABC, abstractmethod

from Models.VO.ContatoVO import ContatoVO


class ImportarContatoTemplate(ABC):

    def executar_importacao(self):
        contatos = self.get_contatos_importados()
        if not contatos: return False
        adicionados = 0
        for contato in contatos:
            resultado = self.adicionar_contato(contato)
            if resultado is None: adicionados += 1
        return adicionados > 0

    @abstractmethod
    def get_contatos_importados(self): pass

    @abstractmethod
    def adicionar_contato(self, contato: ContatoVO): pass