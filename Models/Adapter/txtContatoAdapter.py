from Models.VO.ContatoVO import ContatoVO

class TXTContatoAdapter:
    def adaptar(self, caminho_arquivo):
        contatos = []
        with open(caminho_arquivo,"r",encoding="utf-8") as arquivo:
            for indice, linha in enumerate(arquivo, start=1):
                linha = linha.strip()

                # Ignora linhas vazias
                if not linha:
                    continue
                campos = linha.split(";")

                # Verifica se existem os três campos
                if len(campos) != 3:
                    raise ValueError(f"Linha {indice} possui formato inválido.")
                nome, telefone, email = campos
                contato = ContatoVO(
                    indice,
                    nome.strip(),
                    telefone.strip(),
                    email.strip()
                )
                contatos.append(contato)
        return contatos