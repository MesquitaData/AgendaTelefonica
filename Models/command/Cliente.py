from abc import ABC, abstractmethod

class Cliente(ABC):

    @abstractmethod
    def executar(self):
        pass