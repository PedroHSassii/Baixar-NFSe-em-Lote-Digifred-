from pathlib import Path
import csv
import time
import requests

# Intervalo das notas
INICIO = 202500000000322
FIM = 202500000000855

# Código e Municipio do Estabelecimento
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

for numero in range(INICIO, FIM + 1):
    numero_nfse = f"{numero:015d}"
    url = BASE_URL.format(codigo=CODIGO, numero=numero_nfse, municipio=MUNICIPIO)

    arquivo_pdf = PASTA_DESTINO / f"nfse_{numero_nfse}.pdf"

    if arquivo_pdf.exists():
        print(f"Já existe: {arquivo_pdf.name}")
        continue

    print(f"Baixando NFS-e {numero_nfse}...")

    try:
        resposta = requests.get(url, headers=headers, timeout=30)

        if resposta.status_code != 200:
            print(f"Falhou {numero_nfse}: HTTP {resposta.status_code}")
            falhas.append([numero_nfse, resposta.status_code, "HTTP diferente de 200"])
            continue

        conteudo = resposta.content

        # Confere se parece ser PDF
        if not conteudo.startswith(b"%PDF"):
            print(f"Falhou {numero_nfse}: retorno não parece ser PDF")
            falhas.append([numero_nfse, resposta.status_code, "Retorno não é PDF"])
            continue

        arquivo_pdf.write_bytes(conteudo)
        print(f"Salvo: {arquivo_pdf.name}")

        # Pequena pausa para não sobrecarregar o servidor
        time.sleep(0.3)

    except Exception as erro:
        print(f"Erro na NFS-e {numero_nfse}: {erro}")
        falhas.append([numero_nfse, "ERRO", str(erro)])

if falhas:
    with ARQUIVO_FALHAS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nfse", "status", "motivo"])
        writer.writerows(falhas)

    print(f"\nConcluído com falhas. Veja: {ARQUIVO_FALHAS}")
else:
    print("\nConcluído sem falhas.")
