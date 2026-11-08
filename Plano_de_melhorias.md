# Plano de Melhorias
## Para que o padrão VO existe ? -> Trafegar
|Tarefa|Concluído|
|---|:---:|
|Imprementar o VO Corretamente (Ele também é um DTO)|[X]|
|Retirar os Lazy loader de DAO pq dao aparece em todo canto|[X]|
|Implementar o memento|[X]|
|Trocar o comander de model para controller|[X]|

### Por que Trocar o comander de model para controller ?

> 2. O Command (Models/command/) ➔ SIM! Deveria estar no CONTROLLER ⚠
> 
> • O que ele faz: O Invocador recebe uma ordem da View (AgendaView.py), empacota essa intenção do usuário em um comando (ExcluirContatoCommand) e manda a Facade executar.
> 
>• Por que é Controller: Na literatura de software e no MVC clássico, o padrão Command representa uma "Ação do Usuário" (ex: o clique de um botão ou escolha de um menu). Ele é a ponte exata entre a View (quem pede) e o Model (quem executa).
>
>• Veredito: Ele é 100% um mecanismo de controle de fluxo de interação. O lugar ideal dele no MVC seria:
> 
> Controller/
    └── command/
        ├── Cliente.py
        ├── Invocador.py
        ├── ListarContatosCommand.py
        └── ExcluirContatoCommand.py

### Por que o caretaker fica no controller ?
    ### Por que muitos livros colocam a pilha no Controller?
    
    Porque eles separam dois tipos de dados:

     1. Dados de Negócio (Model):
         • São os dados reais da sua agenda: Ana, Beto, telefones, emails.
         • Eles precisam ser persistidos no disco (agendas_sistema.json).
         • Se o programa fechar, esses dados não podem sumir.
     2. Dados de Sessão / Aplicação (Controller):
         • O "Desfazer / Ctrl+Z" não é um dado da sua agenda. Ele é o rastro do que o usuário fez enquanto usava o teclado.
         • Se o usuário fechar o programa, o histórico de Ctrl+Z morre na memória RAM.
         • O Controller é quem interpreta o que o usuário quer: "o usuário clicou em desfazer, então eu devo orquestrar a volta no tempo".

      │ A analogia:
      │ Em uma agenda de papel: os nomes e telefones são o Model.
      │ A mão da pessoa segurando a borracha e decidindo quando apagar o que escreveu nos últimos 5 minutos é o Controller.

