# CPF Inspector

Este é um script Python simples para validar CPFs em arquivos CSV. Ele oferece a funcionalidade de validar CPFs em um único arquivo CSV ou em vários arquivos CSV em um diretório e pode filtrar a saída para exibir apenas CPFs válidos.

## Requisitos

- Python 3.x

## Como usar

1. Baixe ou clone este repositório para o seu sistema local.

2. Certifique-se de ter Python instalado em seu sistema.

3. Abra o terminal (ou prompt de comando) e navegue até o diretório onde você baixou/clonou este repositório.

4. Execute o script com os argumentos necessários. Veja abaixo os exemplos de uso:

### Exemplos de uso:

- Para validar CPFs em um único arquivo CSV:

```bash
python cpf_inspector.py arquivo.csv
```

- Para validar CPFs em um único arquivo CSV e salvar os resultados em um novo arquivo:

```bash
python cpf_inspector.py arquivo.csv -o resultados.csv
```

- Para validar CPFs em um único arquivo CSV e exibir apenas os CPFs válidos:

```bash
python cpf_inspector.py arquivo.csv -t
```

- Para validar CPFs em vários arquivos CSV em um diretório (*pode ser combinado com **-t** e **-o***):

```bash
python cpf_inspector.py -d diretorio_com_csvs
```

## Contribuindo

Sinta-se à vontade para contribuir com melhorias, sugestões ou relatar problemas. Basta abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter detalhes.