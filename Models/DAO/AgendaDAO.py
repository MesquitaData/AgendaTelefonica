import json
import os
from Models.VO.ContatoVO import ContatoVO
from Models.VO.AgendaVO import AgendaVO


class AgendaDAO:
    """Responsável por salvar e buscar Agendas e seus contatos no JSON."""

    def __init__(self, arquivo_dados="agendas_sistema.json"):
        self.arquivo_dados = arquivo_dados

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