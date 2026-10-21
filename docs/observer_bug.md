# Observer BUG

## Método _alterar_agenda
```python
if nova_agenda:
    self.nome_agenda = nova_agenda
    self.controller = AgendaController(self.nome_agenda)  # Cria novo controller e nova facade
```
* **Problema:** Ao instanciar um novo AgendaController, uma nova instância de AgendaFacade é criada, 
mas a View nunca se inscreve no novo Subject. A partir da troca de agenda, o sistema deixa de exibir as notificações.

### Solução
```python
if nova_agenda:
    self.nome_agenda = nova_agenda
    self.controller = AgendaController(self.nome_agenda)
    
    # Avisa a nova agenda: "Ei, agora sou eu que estou na tela, me notifique!"
    self.controller.agenda_facade.inscrever(self)
    
    print(f"\n🔄 Você mudou para a agenda: '{self.nome_agenda}'")
```