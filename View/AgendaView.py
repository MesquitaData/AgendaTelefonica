from AbstractFactory.FabricaAgendasDAO import JSONDAOFactory, TXTDAOFactory
from agenda_controller import AgendaController
from command.Invocador import Invocador
from observer.Observer import *


def login():
    # opcao = ""
    fabrica = None
    while True:
        print("\n📢 [SELECIONE A PERSISTÊNCIA]\n")
        print("» 1. Persistência JSON")
        print("» 2. Persistência TXT")
        print("» 0. Sair\n")
        opcao_selecionada = input("Escolha a opção: ").strip()
        if opcao_selecionada in ("0", "1", "2"):
            opcao = opcao_selecionada
            break
        print("\nOpção inválida! Tente novamente.")

    match opcao:
        case "1":
            fabrica = JSONDAOFactory()
        case "2":
            fabrica = TXTDAOFactory()
        case "0":
            print("Encerrando o sistema...")
            exit()

    return AgendaConsoleView(fabrica)

class AgendaConsoleView:

    """Interface de usuário com suporte a múltiplas agendas."""
    def __init__(self, fabrica):
        self.nome_agenda = "Pessoal"
        self.controller = AgendaController(self, fabrica, self.nome_agenda)
        self.invocador = Invocador()




    def iniciar(self):
        while True:
            print("\n=====================================")
            print(f"  AGENDA ATIVA: {self.controller.nome_agenda.upper()}  ")
            print("=====================================")
            print("1. Adicionar Contato")
            print("2. Listar Contatos")
            print("3. Buscar Contato")
            print("4. Excluir Contato")
            print("5. ALTERAR AGENDA (Pessoal ou Trabalho)")
            print("6. Importar contatos")
            print("7. Desfazer última alteração (ctrl-z)")
            print("8. Sair")

            opcao = input("\nEscolha uma opção (1-8): ").strip()

            match opcao:
                case "1":
                    self.controller.adicionar()
                case "2":
                    self.controller.listar()
                case "3":
                    self.controller.buscar()
                case "4":
                    self.controller.excluir()
                case "5":
                    self.controller.alternar_agenda()
                case "6":
                    self.controller.importar_contatos()
                case "7":
                    self.controller.desfazer_alteracoes()
                case "8":
                    print("\n👋 Fechando o sistema... Até logo!")
                    break
                case _:
                    print("\n⚠️ Opção inválida!")