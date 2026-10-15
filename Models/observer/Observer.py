class Observer:
    """Interface que todo observador deve implementar."""
    def atualizar(self, evento: str, dados=None):
        pass

class Subject:
    """Classe base para quem deseja ser observado (gerencia as assinaturas)."""
    def __init__(self):
        self._observadores = []

    def inscrever(self, observador: Observer):
        if observador not in self._observadores:
            self._observadores.append(observador)

    def desinscrever(self, observador: Observer):
        self._observadores.remove(observador)

    def notificar(self, evento: str, dados=None):
        for observador in self._observadores:
            observador.atualizar(evento, dados)