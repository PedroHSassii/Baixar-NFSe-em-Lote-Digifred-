# Baixador Automático de NFS-e — Digifred

> 🇧🇷 Português | [🇺🇸 English](#-english)

Script em Python para baixar em lote os PDFs de NFS-e emitidas no sistema **Digifred**, a partir de um intervalo numérico ou de uma lista de notas em CSV.

Feito para evitar o download manual, nota por nota, no portal do município.

## Funcionalidades

- Baixa PDFs de NFS-e em lote, por intervalo ou por lista em CSV
- Pula notas cujo PDF já existe na pasta de destino
- Valida se a resposta do servidor é realmente um PDF antes de salvar
- Registra as notas que falharam em `falhas.csv`, com status e motivo
- Aplica uma pausa entre os downloads para não sobrecarregar o servidor

## Requisitos

- Python 3.8 ou superior
- Biblioteca `requests`

## Instalação

```bash
git clone https://github.com/PedroHSassii/Baixar-NFSe-em-Lote-Digifred-.git
cd Baixar-NFSe-em-Lote-Digifred-
pip install requests
```

## Configuração

A configuração é feita editando as constantes no topo do script escolhido.

**Comuns aos dois scripts:**

| Constante | Descrição | Exemplo | Obrigatória |
|---|---|---|---|
| `CODIGO` | Código do estabelecimento no Digifred | `1234` | Sim |
| `MUNICIPIO` | Identificador do município na URL do Digifred | `nomedomunicipio` | Sim |
| `PASTA_DESTINO` | Pasta onde os PDFs são salvos | `notas_nfse` | Não |

**Apenas em `BaixarNFSe.py` (por intervalo):**

| Constante | Descrição | Exemplo |
|---|---|---|
| `INICIO` | Número da primeira nota do intervalo | `202500000000322` |
| `FIM` | Número da última nota do intervalo | `202500000000855` |

**Apenas em `BaixarNFSe CSV.py` (por lista):**

| Constante | Descrição | Exemplo |
|---|---|---|
| `ARQUIVO_CSV` | Caminho do CSV com uma NFS-e por linha | `notas.csv` |

O CSV deve ter um número de nota por linha, na primeira coluna. Números com menos de 15 dígitos são completados com zeros à esquerda automaticamente.

```csv
202500000000322
202500000000323
202500000000340
```

## Uso

Baixar um intervalo contínuo de notas:

```bash
python "BaixarNFSe.py"
```

Baixar apenas as notas listadas em um CSV:

```bash
python "BaixarNFSe CSV.py"
```

## Saída

```
notas_nfse/
├── nfse_202500000000322.pdf
├── nfse_202500000000323.pdf
└── falhas.csv              # gerado só quando alguma nota falha
```

O `falhas.csv` traz três colunas: `nfse`, `status` e `motivo` — útil para reprocessar as pendências alimentando o script de CSV com elas.

## Estrutura do projeto

```
.
├── BaixarNFSe.py        # download por intervalo numérico (INICIO → FIM)
├── BaixarNFSe CSV.py    # download a partir de uma lista de notas em CSV
└── README.md
```

## Observações

- O script depende da estrutura de URL do Digifred (`/{municipio}/nfse/web/nfse/exibe_nota_pdf/{codigo}/{numero}`); mudanças no sistema podem exigir ajuste.
- A pausa de 0,3 s entre requisições é intencional. Aumente-a se for baixar volumes grandes.
- Use apenas com notas que você tem autorização para acessar.

## Licença

Não definida.

---

## 🇺🇸 English

> [🇧🇷 Português](#baixador-automático-de-nfs-e--digifred) | 🇺🇸 English

# Bulk NFS-e Downloader — Digifred

Python script that downloads NFS-e (Brazilian municipal electronic service invoices) PDFs in bulk from the **Digifred** system, either by numeric range or from a CSV list of invoice numbers.

Built to avoid downloading invoices one by one through the municipal portal.

### Features

- Bulk download of NFS-e PDFs, by range or from a CSV list
- Skips invoices whose PDF already exists in the destination folder
- Verifies the server response is actually a PDF before saving
- Logs failed invoices to `falhas.csv`, with status and reason
- Pauses between downloads to avoid overloading the server

### Requirements

- Python 3.8 or later
- `requests` library

### Installation

```bash
git clone https://github.com/PedroHSassii/Baixar-NFSe-em-Lote-Digifred-.git
cd Baixar-NFSe-em-Lote-Digifred-
pip install requests
```

### Configuration

Configuration is done by editing the constants at the top of the chosen script.

**Common to both scripts:**

| Constant | Description | Example | Required |
|---|---|---|---|
| `CODIGO` | Establishment code in Digifred | `1234` | Yes |
| `MUNICIPIO` | Municipality identifier used in the Digifred URL | `nomedomunicipio` | Yes |
| `PASTA_DESTINO` | Folder where PDFs are saved | `notas_nfse` | No |

**`BaixarNFSe.py` only (range mode):**

| Constant | Description | Example |
|---|---|---|
| `INICIO` | First invoice number in the range | `202500000000322` |
| `FIM` | Last invoice number in the range | `202500000000855` |

**`BaixarNFSe CSV.py` only (list mode):**

| Constant | Description | Example |
|---|---|---|
| `ARQUIVO_CSV` | Path to a CSV with one invoice number per line | `notas.csv` |

The CSV must hold one invoice number per line, in the first column. Numbers shorter than 15 digits are zero-padded automatically.

### Usage

Download a continuous range of invoices:

```bash
python "BaixarNFSe.py"
```

Download only the invoices listed in a CSV:

```bash
python "BaixarNFSe CSV.py"
```

### Output

PDFs are written to `notas_nfse/` as `nfse_<number>.pdf`. When any invoice fails, a `falhas.csv` is generated with the columns `nfse`, `status` and `motivo` (reason) — feed it back into the CSV script to retry.

### Notes

- The script relies on Digifred's URL structure (`/{municipio}/nfse/web/nfse/exibe_nota_pdf/{codigo}/{numero}`); changes to the system may require adjustment.
- The 0.3 s delay between requests is intentional. Increase it for large batches.
- Only use it for invoices you are authorized to access.

### License

Not defined.
