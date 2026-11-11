import json
from pathlib import Path
from Models.Adapter.ContatoAdapter import TXTContatoAdapter
from Models.DAO.AgendaDAOAbstract import AgendaDAO
from Models.VO.AgendaVO import AgendaVO
from Models.VO.ContatoVO import ContatoVO
import threading
from Models.synchronized import synchronized

# Bloqueio compartilhado.
_LOCK_ARQUIVO = threading.RLock()

# Implementação da classe concreta DAO para arquivos JSON
class JSONAgendaDAO(AgendaDAO):

    _instancia = None # Implementacao do Padrao Singleton
    _lock_instancia = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock_instancia:
            if cls._instancia is None:
                cls._instancia = super().__new__(cls)
                cls._instancia._lock = _LOCK_ARQUIVO

            return cls._instancia

    @synchronized
    def __init__(self):
        if getattr(self, "_inicializado", False):
            return
        raiz = Path(__file__).resolve().parents[2] / "agendas_sistema.json"
        self.caminho = raiz
        self.caminho.parent.mkdir(parents=True, exist_ok=True) # garante a existencia do diretorio onde esta o arquivo
        self._inicializado = True

    @synchronized
    def ler_arquivo(self):
        if not self.caminho.exists():
            return {}

        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    @synchronized
    def obter_agenda(self, nome_agenda):
        agendas = self.ler_arquivo()

        if nome_agenda not in agendas:
            return None

        return AgendaVO(nome_agenda, self)

    @synchronized
    def obter_contatos(self, nome_agenda):
        agendas = self.ler_arquivo()
        dados_agenda = agendas.get(nome_agenda, {})

        return [
            ContatoVO(
                c["id"],
                c["nome"],
                c["telefone"],
                c["email"]
            )
            for c in dados_agenda.get("contatos", [])
        ]

    @synchronized
    def salvar_agenda(self, nome_agenda, contatos):
        agendas = self.ler_arquivo()
        agendas[nome_agenda] = {
            "contatos": [
                {
                    "id": c.id,
                    "nome": c.nome,
                    "telefone": c.telefone,
                    "email": c.email
                }
                for c in contatos
            ]
        }
        with open(self.caminho, "w", encoding="utf-8") as arquivo:
            json.dump(agendas, arquivo, ensure_ascii=False, indent=4)

        return True

    @synchronized
    def importar_contatos(self,nome_agenda):
        caminho_arquivo = Path(__file__).resolve().parents[2] / "agendas_sistema.txt"
        try:
            adapter = TXTContatoAdapter()
            contatos = adapter.adaptar(caminho_arquivo,nome_agenda)
            return contatos

        except (OSError, ValueError, KeyError, TypeError) as erro:
            print(f"Erro na importação: {type(erro).__name__}: {erro}")
            return []