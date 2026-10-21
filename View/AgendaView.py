from Controller.AgendaController import AgendaController
from Models.observer.Observer import Observer
from pathlib import Path

class AgendaConsoleView(Observer):
    """Interface de usuário com suporte a múltiplas agendas."""

    def __init__(self):
        # O programa inicia na agenda Pessoal por padrão
        self.nome_agenda = "Pessoal"
        self.controller = AgendaController(self.nome_agenda)
        self.controller.inscrever_observador(self)

    def atualizar(self, evento: str, dados=None):
        """Este método é chamado automaticamente pelo Controller sempre que algo muda."""
        print("\n📢 [NOTIFICAÇÃO DO SISTEMA]")
        if evento == "contato_adicionado":
            print(f"» Novo contato salvo em tempo real: {dados.nome} ({dados.telefone})")
        elif evento == "contato_excluido":
            print(f"» O contato com ID {dados} foi removido com sucesso do banco JSON.")

    def iniciar(self):
        while True:
            print("\n=====================================")
            print(f"  AGENDA ATIVA: {self.nome_agenda.upper()}  ")
            print("=====================================")
            print("1. Adicionar Contato")
            print("2. Listar Contatos")
            print("3. Buscar Contato")
            print("4. Excluir Contato")
            print("5. ALTERAR AGENDA (Pessoal/Trabalho/etc)")
            print("6. Importar contatos de arquivo TXT")
            print("7. Sair")

            opcao = input("\nEscolha uma opção (1-7): ").strip()

            if opcao == "1":
                self._adicionar()
            elif opcao == "2":
                self._listar()
            elif opcao == "3":
                self._buscar()
            elif opcao == "4":
                self._excluir()
            elif opcao == "5":
                self._alternar_agenda()  # <- Nova funcionalidade da View
            elif opcao == "6":
                self.importar_contatos_txt()  # <- Funcionalidade Adapter
            elif opcao == "7":
                print("\n👋 Fechando o sistema... Até logo!")
                break
            else:
                print("\n⚠️ Opção inválida!")

    def _alternar_agenda(self):
        nova_agenda = (
            input("\nDigite o nome da agenda que deseja acessar: ")
            .strip()
            .capitalize()
        )
        if nova_agenda:
            self.nome_agenda = nova_agenda
            # O Controller simplesmente carrega o novo estado a partir do DAO
            self.controller = AgendaController(self.nome_agenda)
            self.controller.inscrever_observador(self)
            print(f"\n🔄 Você mudou para a agenda: '{self.nome_agenda}'")
        else:
            print("\n⚠️ Nome inválido.")

    def _adicionar(self):
        nome = input("Nome: ").strip()
        telefone = input("Telefone: ").strip()
        email = input("E-mail (opcional): ").strip()

        resultado = self.controller.adicionar_contato(
            nome, telefone, email
        )

        if isinstance(resultado, str):
            print(f"Erro: {resultado}")

        elif resultado:
            print("\n✅ Contato adicionado com sucesso!")

        else:
            print("\n⚠️ Erro: Nome e Telefone são obrigatórios.")

    def _listar(self):
        contatos = self.controller.listar_contatos()
        if not contatos:
            print(f"\n📭 A agenda '{self.nome_agenda}' está vazia.")
            return

        print(f"\n=== CONTATOS DA AGENDA: {self.nome_agenda.upper()} ===")
        for c in contatos:
            print(f"ID: {c.id} | {c.nome} - 📞 {c.telefone} | ✉️ {c.email}")

    def _buscar(self):
        termo = input("Digite o nome ou telefone para buscar: ").strip()
        resultados = self.controller.buscar_contatos(termo)

        if not resultados:
            print(f"\n❌ Nenhum contato encontrado para '{termo}'.")
            return

        print(f"\n🔍 Resultados encontrados ({len(resultados)}):")
        for c in resultados:
            print(f"ID: {c.id} | {c.nome} - {c.telefone}")

    def _excluir(self):
        try:
            id_excluir = int(input("\nDigite o ID do contato para remover: "))
            if self.controller.excluir_contato(id_excluir):
                print("\n🗑️ Contato removido com sucesso!")
            else:
                print("\n❌ ID não encontrado nesta agenda.")
        except ValueError:
            print("\n⚠️ Digite um número de ID válido.")

    def importar_contatos_txt(self):
        # caminho = input("Digite o caminho do arquivo TXT: ").strip().strip('"')
        caminho = Path(__file__).resolve().parent.parent / "contatos.txt"
        if not caminho:
            print("Nenhum arquivo foi informado.")
            return

        resultado = self.controller.importar_contatos_txt(str(Path(caminho)))
        if resultado:
            print("Contatos importados e salvos com sucesso no JSON!")
        else:
            print("Erro ao importar ou salvar os contatos no JSON.")