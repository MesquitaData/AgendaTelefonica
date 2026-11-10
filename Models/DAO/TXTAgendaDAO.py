from pathlib import Path
from Models.DAO.AgendaDAOAbstract import AgendaDAO
from Models.VO.AgendaVO import AgendaVO
import threading
from Models.synchronized import synchronized

# Bloqueio compartilhado.
_LOCK_ARQUIVO = threading.RLock()

class TXTAgendaDAO(AgendaDAO):

    _instancia = None  # Implementacao do Padrao Singleton
    _lock_instancia = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock_instancia:
            if cls._instancia is None:
                cls._instancia = super().__new__(cls)
                cls._instancia._lock = _LOCK_ARQUIVO

            return cls._instancia

    @synchronized
    def __init__(self):
        raiz = Path(__file__).resolve().parents[2] / "agendas_sistema.txt"
        self.caminho = raiz
        self.caminho.parent.mkdir(parents=True, exist_ok=True)

    @synchronized
    def _ler(self):
        agendas = set()

        if not self.caminho.exists():
            return agendas

        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()

                if not linha:
                    continue

                nome_agenda = linha.split(";")[0].strip()
                agendas.add(nome_agenda)

        return agendas

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
            with open(self.caminho, "a", encoding="utf-8") as arquivo:
                arquivo.write(nome_agenda + "\n")

    @synchronized
    def listar_agendas(self):
        return self._ler()