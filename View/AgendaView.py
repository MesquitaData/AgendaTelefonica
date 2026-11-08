from Models.facade.AgendaFacade import AgendaFacade
from Controller.observer.Observer import Observer
from Models.VO.ContatoVO import ContatoVO
from command.ExcluirContatoCommand import ExcluirContatoCommand
from command.Invocador import Invocador
from command.ListarContatosCommand import ListarContatosCommand


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
        match evento:
            case "contato_adicionado":
                print(f"» Novo contato salvo em tempo real: {dados.nome} ({dados.telefone})")
            case "contato_excluido":
                print(f"» O contato com ID {dados} foi removido com sucesso da base de dados.")
            case "alternar_agenda":
                print(f"» A agenda foi alterada para {self.nome_agenda.upper()}.")
            case "buscar_contato":
                print(f"» Resultado da busca dos contatos salvos na agenda {dados}")
            case "listar_contatos":
                print(f"» Retornando os contatos salvos na agenda {dados}")
            case "importar_contatos":
                print("» Retornando os contatos salvos na agenda")
            case "contato_existente":
                print("» Esse contato telefônico já foi cadastrado no sistema!")
            case "sucesso_memento":
                print("» Memento restaurado com sucesso!")
            case "erro_memento":
                print("» Erro ao tentar restaurar o memento!")


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
            print("7. Desfazer última alteração (ctrl-z)")
            print("8. Sair")

            opcao = input("\nEscolha uma opção (1-8): ").strip()

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
                self.importar_contatos()
            elif opcao == "7":
                self.agenda_facade.desfazer_alteracoes()
            elif opcao == "8":
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
        idade = int(input("Idade: ").strip())
        contato = ContatoVO(0,nome,telefone, idade, email)
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
            print(f"ID: {c.id} | {c.nome} - 📞 {c.telefone} | 🎂 {c.idade} anos | ✉️ {c.email}")

    def _buscar(self):
        print("\n🔍 === COMO DESEJA BUSCAR? ===")
        print("1. Buscar só por Nome, E-mail ou Telefone")
        print("2. Buscar só por Idade")
        print("3. Buscar por Nome, E-mail ou Telefone E filtrar por Idade")

        opcao = input("\nEscolha uma opção (1-3): ").strip()

        item: str = ""
        idade: int = 0

        if opcao == "1":
            item = input("Digite o nome, e-mail ou telefone: ").strip()
            if not item:
                print("⚠️ Campo de busca não pode ser vazio.")
                return

        elif opcao == "2":
            try:
                idade = int(input("Digite a idade: ").strip())
            except ValueError:
                print("⚠️ Digite um número inteiro válido para a idade.")
                return

        elif opcao == "3":
            item = input("Digite o nome, e-mail ou telefone: ").strip()
            try:
                idade = int(input("Digite a idade para filtrar: ").strip())
            except ValueError:
                print("⚠️ Digite um número inteiro válido para a idade.")
                return

        else:
            print("\n⚠️ Opção de busca inválida!")
            return

        resultados = self.agenda_facade.buscar_contatos(item, idade)

        if not resultados:
            print("\n❌ Nenhum contato encontrado com os critérios informados.")
            return

        print(f"\n🔍 Resultados encontrados ({len(resultados)}):")
        for c in resultados:
            print(f"ID: {c.id} | {c.nome} - " f"📞 {c.telefone} | 🎂 {c.idade} anos | ✉️ {c.email}")

    def _excluir(self):
        try:
            id_excluir = int(input("\nDigite o ID do contato para remover: "))
            comando = ExcluirContatoCommand(self.agenda_facade, id_excluir)
            self.invocador.definir_comando(comando)
            self._invocador.executar_comando()
        except ValueError:
            print("\n⚠️ Digite um número de ID válido.")

    def importar_contatos(self):
        resultado = self.agenda_facade.importar_contatos_facade()
        if not resultado:
            print("Erro ao importar ou salvar os contatos no JSON.")