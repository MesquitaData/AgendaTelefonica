# Plano de Melhorias
## Para que o padrão VO existe ? -> Trafegar
|Tarefa|Concluído|
|---|:---:|
|Imprementar o VO Corretamente (Ele também é um DTO)|[X]|
|Retirar os Lazy loader de DAO pq dao aparece em todo canto|[X]|
|Implementar o memento|[]|
|Trocar o comander de model para controller|[]|

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
