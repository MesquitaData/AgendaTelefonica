from command.Cliente import Cliente

class ExcluirContatoCommand(Cliente):
    def __init__(self, facade, id_contato):
        self.facade = facade
        self.id_contato = id_contato

    def executar(self):
        print("[COMMAND] Executando ExcluirContatoCommand...")
        resultado = self.facade.excluir_contato(self.id_contato)
        return resultado