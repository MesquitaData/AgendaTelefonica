from Models.facade.AgendaFacade import AgendaFacade
from Controller.observer.Observer import Observer
from Models.VO.ContatoVO import ContatoVO
from command.ExcluirContatoCommand import ExcluirContatoCommand
from command.Invocador import Invocador
from command.ListarContatosCommand import ListarContatosCommand

class AgendaConsoleView(Observer):
    """Interface de usuário com suporte a múltiplas agendas."""
    def __init__(self, fabrica):
        super().__init__()
        self.nome_agenda = "Pessoal"

        # A fábrica é repassada à Facade
        self.agenda_facade = AgendaFacade(
            fabrica=fabrica,
            nome_agenda=self.nome_agenda
        )
        self.agenda_facade.inscrever(self)
        self._invocador = Invocador()

    # Implementação padrão Observer, que observará a Facade
    def atualizar(self, evento: str, dados=None):
        """Este método é chamado automaticamente pelo Controller sempre que algo muda."""
        print("\n📢 [NOTIFICAÇÃO DO SISTEMA]")
        match evento:
            case "contato_adicionado":
                telefone = dados.telefone
                telefone = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
                print(f"» Novo contato salvo em tempo real. Nome: {dados.nome} - Telefone: {telefone}")
            case "contato_excluido":
                print(f"» O contato com ID {dados} foi removido com sucesso da base de dados.")
            case "alternar_agenda":
                print(f"» A agenda foi alterada para AGENDA {dados.upper()}.")
            case "buscar_contato":
                print(f"» Resultado da busca dos contatos salvos na agenda {dados}")
            case "importar_contatos":
                print("» Retornando os contatos salvos na agenda")
            case "contato_existente":
                print(f"» {dados}")
            case "sucesso_memento":
                print("» Memento restaurado com sucesso!")
            case "erro_memento":
                print("» Erro ao tentar restaurar o memento!")
            case "importar_contatos_sem_sucesso":
                print("Nenhum contato foi importado. Verifique se os contatos já existem na agenda.")


    def iniciar(self):
        while True:
            print("\n=====================================")
            print(f"  AGENDA ATIVA: {self.nome_agenda.upper()}  ")
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
                    self._adicionar()
                case "2":
                    self._listar()
                case "3":
                    self._buscar()
                case "4":
                    self._excluir()
                case "5":
                    self._alternar_agenda()  # <- Nova funcionalidade da View
                case "6":
                    self.importar_contatos()
                case "7":
                    self.agenda_facade.desfazer_alteracoes()
                case "8":
                    print("\n👋 Fechando o sistema... Até logo!")
                    break
                case _:
                    print("\n⚠️ Opção inválida!")

    def _alternar_agenda(self):
        nova_agenda = (input("\nDigite o nome da agenda que deseja acessar: ").strip().capitalize())
        if nova_agenda in ["Pessoal","Trabalho"]:
            self.nome_agenda = self.agenda_facade.alternar_agenda_facade(nova_agenda).nome
        else:
            print("Informe uma opção válida de agenda!!!")

    def _adicionar(self):
        nome = input("Nome: ").strip()
        telefone = input("Telefone: ").strip()
        email = input("E-mail (opcional): ").strip()
        contato = ContatoVO(0,nome,telefone,email)
        return self.agenda_facade.adicionar_contato(contato)

    def _listar(self):
        comando = ListarContatosCommand(self.agenda_facade)
        self._invocador.definir_comando(comando)
        contatos = self._invocador.executar_comando()

        if not contatos:
            print(f"\n📭 A agenda '{self.nome_agenda}' está vazia.")
            return

        print(f"\n=== CONTATOS DA AGENDA: {self.nome_agenda.upper()} ===")
        for c in contatos:
            telefone = c.telefone
            telefone = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"  # Formatação do telefone
            print(f"ID: {c.id} | {c.nome} - 📞 {telefone} | ✉️ {c.email}")

    def _buscar(self):
        print("\n🔍 Filtros de Busca:\n")
        nome = telefone = email = ""
        opcao_filtro = input("Qual filtro deseja usar para a busca ?\n1- Nome\n2- Telefone\n3- Email\nInforme a opção: ").strip()
        match opcao_filtro:
            case "1":
                nome = input("Filtrar por Nome: ").strip()
            case "2":
                telefone = input("Filtrar por Telefone: ").strip()
            case "3":
                email = input("Filtrar por E-mail: ").strip()
            case _:
                return
        resultados = self.agenda_facade.buscar_contatos(ContatoVO(0, nome, telefone, email),self.nome_agenda) #Controller

        if not resultados:
            print("\n❌ Nenhum contato encontrado com os critérios informados.")
            return

        print(f"\n🔍 Resultados encontrados ({len(resultados)}):")
        for c in resultados:
            telefone = c.telefone
            telefone = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"  # Formatação do telefone
            print(f"ID: {c.id} | {c.nome} - " f"📞 {telefone} | ✉️ {c.email}")

    def _excluir(self):
        try:
            id_excluir = int(input("\nDigite o ID do contato para remover: "))
            comando = ExcluirContatoCommand(self.agenda_facade, id_excluir)
            self._invocador.definir_comando(comando)
            self._invocador.executar_comando()
        except ValueError:
            print("\n⚠️ Digite um número de ID válido.")

    def importar_contatos(self): self.agenda_facade.importar_contatos_facade()