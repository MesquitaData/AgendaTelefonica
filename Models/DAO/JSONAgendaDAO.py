import json
from pathlib import Path
from Models.DAO.AgendaDAOAbstract import AgendaDAO
from Models.VO.AgendaVO import AgendaVO
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
        raiz = Path(__file__).resolve().parents[2] / "agendas_sistema.json"
        self.caminho = raiz
        self.caminho.parent.mkdir(parents=True, exist_ok=True)

    @synchronized
    def _ler(self):
        if not self.caminho.exists():
            return {}

        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    @synchronized
    def obter_agenda(self, nome_agenda, contato_dao):
        agendas = self._ler()
        if nome_agenda not in agendas:
            return None
        return AgendaVO(nome_agenda, contato_dao)

    @synchronized
    def salvar_agenda(self, nome_agenda):
        agendas = self._ler()
        if nome_agenda not in agendas:
            agendas[nome_agenda] = {
                "nome": nome_agenda,
                "contatos": []
            }

        with open(self.caminho, "w", encoding="utf-8") as arquivo:
            json.dump(
                agendas,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

    @synchronized
    def listar_agendas(self):
        agendas = self._ler()
        return list(agendas.keys())