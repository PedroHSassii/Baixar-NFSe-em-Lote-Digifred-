# Baixador Automático de NFS-e

Este projeto contém um script em Python para baixar automaticamente arquivos PDF de NFS-e a partir de uma sequência numérica de notas fiscais.

O script foi criado para automatizar o download das notas fiscais emitidas no sistema da Digifred, usando um intervalo inicial e final de numeração.

## Funcionalidades

- Baixa PDFs de NFS-e em lote
- Permite definir número inicial e final das notas
- Salva os arquivos em uma pasta organizada
- Evita baixar novamente arquivos que já existem
- Valida se o retorno do servidor realmente parece ser um PDF
- Gera um arquivo `falhas.csv` com as notas que não puderam ser baixadas
- Inclui pausa entre os downloads para evitar sobrecarregar o servidor

## Exemplo de uso

O script baixa automaticamente as notas de um intervalo:

```text
Ex : 202500000000322 até 202500000000855
