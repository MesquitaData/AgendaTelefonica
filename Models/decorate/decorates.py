# Componente Base
from abc import ABC, abstractmethod

# Abstract Base Class
class BuscarComponent(ABC):

    # @abstractmethod determina que qualquer classe concreta que herdar de BuscarComponent deverá implementar
    # o metodo buscar(). Logo, tanto BuscarTodosContatos quanto FiltrarPorNome precisam implementar esse metodo.
    @abstractmethod
    def buscar(self): pass

# Busca todos os contatos sem aplicar nenhum fitro
# Utiliza os metodos disponibilizados pela camada de negocio
class BuscarTodosContatos(BuscarComponent):
    def __init__(self, agenda_bo):
        self.contatos = agenda_bo._agenda_ativa.contatos  # Ocorre a recuperação dos contatos

    def buscar(self):
        return self.contatos

# Decorator baser
class FiltroDecorator(BuscarComponent):
    def __init__(self, component: BuscarComponent):
        self.componente = component

    def buscar(self):
        return self.componente.buscar()

class FiltrarPorNome(FiltroDecorator):
    # Objeto que será decorado e nome para busca por filtro
    def __init__(self, component: BuscarComponent, nome: str):
        super().__init__(component) # Chama o construtor da classe FiltroDecorator, armazenando o componente recebido
        self.nome = nome.strip().lower()

    def buscar(self):
        contatos = super().buscar()
        return [contato for contato in contatos if self.nome in contato.nome.lower()]

class FiltrarPorEmail(FiltroDecorator):
    def __init__(self, component: BuscarComponent, email: str):
        super().__init__(component)
        self.email = email

    def buscar(self):
        contatos = super().buscar()
        return [contato for contato in contatos if self.email == contato.email]

class FiltrarPorTelefone(FiltroDecorator):
    def __init__(self, component: BuscarComponent, telefone: str):
        super().__init__(component)
        self.telefone = telefone

    def buscar(self):
        contatos = super().buscar()
        return [contato for contato in contatos if self.telefone == contato.telefone]

class FiltrarPorIdade(FiltroDecorator):
    def __init__(self, component: BuscarComponent, idade: int):
        super().__init__(component)
        self.idade = idade

    def buscar(self):
        contatos = super().buscar()
        return [contato for contato in contatos if self.idade == contato.idade]




