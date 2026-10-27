from Models.command.Cliente import Cliente

class ListarContatosCommand(Cliente):
    def __init__(self, facade):
        self.facade = facade

    def executar(self):
        print("[COMMAND] Executando ListarContatosCommand...")
        contatos = self.facade.listar_contatos()
        return contatos