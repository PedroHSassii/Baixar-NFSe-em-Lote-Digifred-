from pathlib import Path
import csv
import time
import requests

# Arquivo CSV contendo uma NFS-e por linha
ARQUIVO_CSV = Path("")

# Código e Município do Estabelecimento
CODIGO = ""
MUNICIPIO = ""

# Pasta onde os PDFs serão salvos
PASTA_DESTINO = Path("notas_nfse")
PASTA_DESTINO.mkdir(exist_ok=True)

# Arquivo de log para notas que falharem
ARQUIVO_FALHAS = PASTA_DESTINO / "falhas.csv"

BASE_URL = "https://sim.digifred.net.br/{municipio}/nfse/web/nfse/exibe_nota_pdf/{codigo}/{numero}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

falhas = []

# Lê somente as NFS-e existentes no CSV
with ARQUIVO_CSV.open("r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)

    for linha in reader:
        if not linha:
            continue

        numero_nfse = linha[0].strip()

        if not numero_nfse:
            continue

        # Garante 15 posições
        numero_nfse = numero_nfse.zfill(15)

        url = BASE_URL.format(
            codigo=CODIGO,
            numero=numero_nfse,
            municipio=MUNICIPIO
        )

        arquivo_pdf = PASTA_DESTINO / f"nfse_{numero_nfse}.pdf"

        if arquivo_pdf.exists():
            print(f"Já existe: {arquivo_pdf.name}")
            continue

        print(f"Baixando NFS-e {numero_nfse}...")

        try:
            resposta = requests.get(
                url,
                headers=headers,
                timeout=30
            )

            if resposta.status_code != 200:
                print(
                    f"Falhou {numero_nfse}: "
                    f"HTTP {resposta.status_code}"
                )

                falhas.append([
                    numero_nfse,
                    resposta.status_code,
                    "HTTP diferente de 200"
                ])

                continue

            conteudo = resposta.content

            # Confere se realmente retornou um PDF
            if not conteudo.startswith(b"%PDF"):
                print(
                    f"Falhou {numero_nfse}: "
                    f"retorno não parece ser PDF"
                )

                falhas.append([
                    numero_nfse,
                    resposta.status_code,
                    "Retorno não é PDF"
                ])

                continue

            arquivo_pdf.write_bytes(conteudo)

            print(f"Salvo: {arquivo_pdf.name}")

            # Pequena pausa para não sobrecarregar o servidor
            time.sleep(0.3)

        except Exception as erro:
            print(
                f"Erro na NFS-e {numero_nfse}: {erro}"
            )

            falhas.append([
                numero_nfse,
                "ERRO",
                str(erro)
            ])

# Salva as falhas
if falhas:
    with ARQUIVO_FALHAS.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "nfse",
            "status",
            "motivo"
        ])

        writer.writerows(falhas)

    print(
        f"\nConcluído com falhas. "
        f"Veja: {ARQUIVO_FALHAS}"
    )

else:
    print("\nConcluído sem falhas.")