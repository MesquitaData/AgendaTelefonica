from Models.AbstractFactory.FabricaTXT import TXTDAOFactory
from View.AgendaView import AgendaConsoleView
from Models.AbstractFactory.FabricaJSON import JSONDAOFactory

def login():
    print("\n📢 [REALIZE O LOGIN]\n")
    print("» 1. Login com persistência .JSON")
    print("» 2. Login com persistência .TXT\n")
    opcao = int(input("Escolha a opcao de login: "))
    return opcao

if __name__ == "__main__":
    escolha = login()
    match escolha:
        case 1:
            app = AgendaConsoleView(JSONDAOFactory())
            app.iniciar()
        case 2:
            app = AgendaConsoleView(TXTDAOFactory())
            app.iniciar()