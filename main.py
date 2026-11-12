from View.AgendaView import AgendaConsoleView, login
from Models.AbstractFactory.FabricaAgendasDAO import JSONDAOFactory
from Models.AbstractFactory.FabricaAgendasDAO import TXTDAOFactory

# def login():
#     while True:
#         print("\n📢 [SELECIONE A PERSISTÊNCIA]\n")
#         print("» 1. Persistência JSON")
#         print("» 2. Persistência TXT")
#         print("» 0. Sair\n")
#         opcao = input("Escolha a opção: ").strip()
#         if opcao in ("0", "1", "2"):
#             return opcao
#         print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    # escolha = login()
    # match escolha:
    #     case "1":
    #         fabrica = JSONDAOFactory()
    #     case "2":
    #         fabrica = TXTDAOFactory()
    #     case "0":
    #         print("Encerrando o sistema...")
    #         exit()
    app = login()
    app.iniciar()