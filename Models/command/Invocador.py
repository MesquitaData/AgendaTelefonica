class Invocador:
    def __init__(self):
        self.comando = None

    def definir_comando(self, comando):
        self.comando = comando

    def executar_comando(self):
        if self.comando is None:
            raise ValueError("Nenhum comando foi definido.")
        return self.comando.executar()