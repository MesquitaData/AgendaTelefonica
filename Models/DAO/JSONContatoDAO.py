import json
import threading
from pathlib import Path
from Models.Adapter.ContatoAdapter import TXTContatoAdapter
from Models.DAO.ContatoDAOAbstract import ContatoDAO
from Models.VO.ContatoVO import ContatoVO
from Models.synchronized import synchronized

# Bloqueio compartilhado para operações no arquivo TXT.
_LOCK_ARQUIVO = threading.RLock()

class JSONContatoDAO(ContatoDAO):

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
        raiz = Path(__file__).resolve().parents[2] / "agendas_sistema.json"
        self.caminho = raiz

    @synchronized
    def _ler(self):
        if not self.caminho.exists():
            return {}

        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    @synchronized
    def obter_contatos(self, nome_agenda):
        agendas = self._ler()
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
    def salvar_contatos(self, nome_agenda, contatos):
        agendas = self._ler()

        if nome_agenda not in agendas:
            return False

        agendas[nome_agenda]["contatos"] = [
            {
                "id": c.id,
                "nome": c.nome,
                "telefone": c.telefone,
                "email": c.email
            }
            for c in contatos
        ]

        with open(self.caminho, "w", encoding="utf-8") as arquivo:
            json.dump(
                agendas,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

        return True

    @synchronized
    def importar_contatos(self,nome_agenda):
        caminho_arquivo = Path(__file__).resolve().parents[2] / "agendas_sistema.txt"

        try:
            adapter = TXTContatoAdapter()
            contatos = adapter.adaptar(caminho_arquivo)
            return contatos

        except (OSError, ValueError, KeyError, TypeError) as erro:
            print(f"Erro na importação: {type(erro).__name__}: {erro}")
            return []