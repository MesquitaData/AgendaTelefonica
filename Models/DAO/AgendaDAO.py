import json
import os
from pathlib import Path
from Models.VO.ContatoVO import ContatoVO
from Models.VO.AgendaVO import AgendaVO
from Models.Adapter.txtContatoAdapter import TXTContatoAdapter

class AgendaDAO:
    """Responsável por salvar e buscar Agendas e seus contatos no JSON."""

    # Implementação do Singleton. Cada instância criada compartilha o mesmo caminho.
    # Garante que a classe AgendaDAO tenha apenas uma instância com ponto de acesso global a ela.
    # Garantindo que, durante a execução do programa, exista apenas uma instância dessa
    # classe, mesmo que você tente criar vários objetos.
    _instancia = None
    def __new__(cls, *args, **kwargs):  # Cria e retorna um objeto AgendaDAO
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia # Retorna a instância DAO. Em outras chamadas, é retornada a mesma instância.

    # Aqui se o atributo inicializado for True, não sobreescreve o caminho até o arquivo com os dados
    # Ou seja, para outros objetos DAO o arquivo_dados será o mesmo
    def __init__(self, arquivo_dados="agendas_sistema.json"): # Inicializa o objeto criado
        if not hasattr(self, "_inicializado"): # Verifica se o objeto já criado possui um determinado atributo
            self.arquivo_dados = arquivo_dados
            self._inicializado = True

    def _ler_arquivo(self):
        if not os.path.exists(self.arquivo_dados):
            return {}
        try:
            with open(self.arquivo_dados, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _gravar_arquivo(self, dados):
        with open(self.arquivo_dados, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def obter_agenda(self, nome_agenda):
        """Busca uma agenda pelo nome e reconstrói o objeto AgendaVO com seus Contatos."""
        todas_agendas = self._ler_arquivo()

        if nome_agenda not in todas_agendas:
            return AgendaVO(nome_agenda)  # Retorna uma agenda vazia se não existir

        dados_agenda = todas_agendas[nome_agenda]
        lista_contatos = []

        for c in dados_agenda["contatos"]:
            lista_contatos.append(ContatoVO(c["id"], c["nome"], c["telefone"], c["email"]))

        return AgendaVO(nome_agenda, lista_contatos)

    def salvar_agenda(self, agenda_vo):
        """Salva ou atualiza uma agenda específica no arquivo JSON."""
        todas_agendas = self._ler_arquivo()

        contatos_dict = [
            {"id": c.id, "nome": c.nome, "telefone": c.telefone, "email": c.email}
            for c in agenda_vo.contatos
        ]

        todas_agendas[agenda_vo.nome] = {
            "nome": agenda_vo.nome,
            "contatos": contatos_dict
        }

        self._gravar_arquivo(todas_agendas)

    # Aqui, futuramente, poderia ter outros caminhos para outros
    # tipos de arquivos ou BD
    def importar_contatos_dao(self):
        caminho_arquivo = Path(__file__).resolve().parents[2] / "contatos.txt"

        try:
            adapter = TXTContatoAdapter()
            return adapter.adaptar(caminho_arquivo)

        except (OSError, ValueError, KeyError, TypeError) as erro:
            return []