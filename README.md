# Agenda de Contatos Padronizada
Agenda de contatos feita inteiramente em python para a cadeira de **Arquitetura de Software**.
## Objetivo
    O objetivo deste projeto é aplicar todos os padrões vistos durante a disciplina
- **Padrões**
  1. MVC [X]
  2. DAO [X]
  4. VO [X]
  5. Observer[x]
  6. Lazy Loading [X]
    - Voce so carrega as informações quando for solicitado
  7. Fachada[x]
    ```python
        # DAO (Data Access Object)
    class UsuarioDAO:
        def __init__(self):
            print("[DAO] Inicializando conexão com banco...")
            self.usuarios = {
                1: {"nome": "Renan", "email": "renan@email.com"},
                2: {"nome": "Maria", "email": "maria@email.com"},
            }

        def buscar_por_id(self, usuario_id):
            print(f"[DAO] Consultando usuário {usuario_id} no banco...")
            return self.usuarios.get(usuario_id, None)


    # Fachada com Lazy Loader
    class UsuarioFacade:
        def __init__(self):
            self._dao = None  # DAO não é criado imediatamente

        @property
        def dao(self):
            # Lazy loading: só cria o DAO quando for usado pela primeira vez
            if self._dao is None:
                print("[LazyLoader] Criando DAO sob demanda...")
                self._dao = UsuarioDAO()
            return self._dao

        def obter_usuario(self, usuario_id):
            usuario = self.dao.buscar_por_id(usuario_id)
            if usuario:
                print("[Facade] Usuário encontrado!")
                return usuario
            else:
                print("[Facade] Usuário não existe.")
                return {"erro": "Usuário não encontrado"}


    # Controller
    class UsuarioController:
        def __init__(self):
            self.facade = UsuarioFacade()

        def consultar_usuario(self, usuario_id):
            print("[Controller] Recebendo requisição...")
            resultado = self.facade.obter_usuario(usuario_id)
            return resultado


    # --- Exemplo de uso ---
    if __name__ == "__main__":
        controller = UsuarioController()

        # Nenhum DAO criado ainda
        print(">>> Primeira consulta")
        print(controller.consultar_usuario(1))

        print("\n>>> Segunda consulta")
        print(controller.consultar_usuario(2))

    ```
  8. Abstract Factory
  9. Chain of responsibility [X]
  10. memento
  11. command
  12. singleton
  13. template method
  14. BO (business object) [X]
  15. decorate
  16. adapter
  17. synchronizer token
  18. value holder
  19. ghost
  20. virtual proxy
## Funcionalidades
