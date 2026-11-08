from Models.facade.AgendaFacade import AgendaFacade
from Controller.observer.Observer import Observer
from Models.command.Invocador import *
from Models.command.ListarContatosCommand import *
from Models.command.ExcluirContatoCommand import *
from Models.VO.ContatoVO import ContatoVO

class AgendaConsoleView(Observer):
    """Interface de usuário com suporte a múltiplas agendas."""
    def __init__(self):
        # O programa inicia na agenda Pessoal por padrão
        super().__init__()
        self.nome_agenda = "Pessoal"
        self.agenda_facade = AgendaFacade(nome_agenda=self.nome_agenda)
        self.agenda_facade.inscrever(self)
        self._invocador = None  # Lazy Loading, pois command só existe para listar e excluir

    # Cria o atributo invocador
    @property
    def invocador(self):
        if self._invocador is None: self._invocador = Invocador()
        return self._invocador

    # Implementação padrão Observer, que observará a Facade
    def atualizar(self, evento: str, dados=None):
        """Este método é chamado automaticamente pelo Controller sempre que algo muda."""
        print("\n📢 [NOTIFICAÇÃO DO SISTEMA]")
        if evento == "contato_adicionado":
            telefone = dados.telefone
            telefone = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
            print(f"» Novo contato salvo em tempo real: Nome: {dados.nome} - Telefone: {telefone}")
        elif evento == "contato_excluido":
            print(f"» O contato com ID {dados} foi removido com sucesso da base de dados.")
        elif evento == "alternar_agenda":
            print(f"» A agenda foi alterada para a Agenda {dados.upper()}.")
        elif evento == "buscar_contato":
            print(f"» Resultado da busca dos contatos salvos na agenda {dados}")
        elif evento == "listar_contatos":
            print(f"» Retornando os contatos salvos na agenda {dados}")
        elif evento == "importar_contatos":
            print(f"» Retornando os contatos salvos na agenda")
        elif evento == "contato_existente":
            print(f"» Esse contato telefônico já foi cadastrado no sistema!")
        elif evento == "importar_contatos_sem_sucesso":
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
                self.importar_contatos()  # <- Funcionalidade Adapter
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
        if nova_agenda in ["Pessoal", "Trabalho"]:
            if self.agenda_facade.alternar_agenda(nova_agenda):
                self.nome_agenda = nova_agenda
            else:
                print("\n⚠️ Não foi possível acessar a agenda.")
        else:
            print("\n⚠️ Nome inválido.")

    def _adicionar(self):
        nome = input("Nome: ").strip()
        telefone = input("Telefone: ").strip()
        email = input("E-mail (opcional): ").strip()
        contato = ContatoVO(0,nome,telefone,email)
        return self.agenda_facade.adicionar_contato(contato)

    def _listar(self):
        comando = ListarContatosCommand(self.agenda_facade)
        self.invocador.definir_comando(comando)
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
        print("\n🔍 Filtros de Busca (pressione Enter para ignorar um filtro):")
        nome = input("Filtrar por Nome: ").strip() or None
        telefone = input("Filtrar por Telefone: ").strip() or None
        email = input("Filtrar por E-mail: ").strip() or None
        resultados = self.agenda_facade.buscar_contatos(ContatoVO(0,nome,telefone,email)) #Controller

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
            self.invocador.definir_comando(comando)
            self._invocador.executar_comando()
        except ValueError:
            print("\n⚠️ Digite um número de ID válido.")

    def importar_contatos(self): self.agenda_facade.importar_contatos_facade()