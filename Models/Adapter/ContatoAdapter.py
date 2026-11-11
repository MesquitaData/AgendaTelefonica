from Models.VO.ContatoVO import ContatoVO
from abc import ABC, abstractmethod
import json

class ContatoAdapter(ABC):
    @abstractmethod
    def adaptar(self, caminho_arquivo,nome_agenda): pass

class JSONContatoAdapter(ContatoAdapter):
    def adaptar(self, caminho_arquivo,nome_agenda):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return [
            ContatoVO(c["id"], c["nome"], c["telefone"], c["email"])
            for c in dados[nome_agenda]["contatos"]
        ]

class TXTContatoAdapter(ContatoAdapter):
    def adaptar(self, caminho_arquivo,nome_agenda):
        contatos = []
        with open(caminho_arquivo,"r",encoding="utf-8") as arquivo:
            for indice, linha in enumerate(arquivo, start=1):
                linha = linha.strip()

                # Ignora linhas vazias
                if not linha:
                    continue
                campos = linha.split(";")

                # Verifica se existem os três campos
                if len(campos) != 5:
                    raise ValueError(f"Linha {indice} possui formato inválido.")
                nome_agenda,id_contato,nome, telefone, email = campos
                contato = ContatoVO(
                    int(id_contato),
                    nome.strip(),
                    telefone.strip(),
                    email.strip()
                )
                contatos.append(contato)
        return contatos