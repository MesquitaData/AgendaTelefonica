import csv
from pathlib import Path
from Models.Adapter.ContatoAdapter import JSONContatoAdapter
from Models.DAO.AgendaDAOAbstract import AgendaDAO
from Models.VO.AgendaVO import AgendaVO
import threading
from Models.VO.ContatoVO import ContatoVO
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
        if getattr(self, "_inicializado", False):
            return
        raiz = Path(__file__).resolve().parents[2] / "agendas_sistema.txt"
        self.caminho = raiz
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self._inicializado = True

    @synchronized
    def ler_arquivo(self):
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
    def salvar_agenda(self, nome_agenda,contatos):
        outros_registros = []
        agendas = self.ler_arquivo()

        # Preserva os registros das outras agendas
        if self.caminho.exists():
            with open(self.caminho, "r", encoding="utf-8", newline="") as arquivo:
                leitor = csv.reader(arquivo, delimiter=";")

                for linha in leitor:
                    if len(linha) == 5 and linha[0] != nome_agenda:
                        outros_registros.append(linha)

        # Reescreve o arquivo
        with open(self.caminho, "w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")

            # Preserva as agendas que não possuem contatos
            for agenda in agendas:
                if agenda != nome_agenda:
                    escritor.writerow([agenda])

            # Registra a agenda caso ainda não exista
            if nome_agenda not in agendas:
                escritor.writerow([nome_agenda])

            # Preserva os contatos das outras agendas
            escritor.writerows(outros_registros)

            # Registra os contatos da agenda atual
            for c in contatos:
                escritor.writerow([
                    nome_agenda,
                    c.id,
                    c.nome,
                    c.telefone,
                    c.email
                ])

        return True

    @synchronized
    def obter_agenda(self, nome_agenda):
        agendas = self.ler_arquivo()
        if nome_agenda not in agendas: return None
        return AgendaVO(nome_agenda, self)

    @synchronized
    def obter_contatos(self, nome_agenda):
        contatos = []
        if not self.caminho.exists():
            return contatos
        with open(self.caminho, "r", encoding="utf-8", newline="") as arquivo:
            leitor = csv.reader(arquivo, delimiter=";")
            for linha in leitor:
                if len(linha) != 5:
                    continue

                agenda, id_, nome, telefone, email = linha
                if agenda == nome_agenda:
                    contatos.append(ContatoVO(int(id_),nome,telefone,email))

        return contatos

    @synchronized
    def importar_contatos(self, nome_agenda):
        caminho_arquivo = Path(__file__).resolve().parents[2] / "agendas_sistema.json"
        try:
            adapter = JSONContatoAdapter()
            return adapter.adaptar(caminho_arquivo, nome_agenda)
        except (OSError, ValueError, KeyError, TypeError) as erro:
            print(f"Erro na importação: {type(erro).__name__}: {erro}")
            return []