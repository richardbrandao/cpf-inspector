# CPF Inspector 🔍

Este é um script Python simples para validar CPFs em arquivos CSV ou TXT. Ele oferece a funcionalidade de validar CPFs em um único arquivo ou em vários arquivos em um diretório e pode filtrar a saída para exibir apenas CPFs válidos.

## Requisitos

- Python 3.x 🐍

## Como usar

1. Baixe ou clone este repositório para o seu sistema local.

2. Certifique-se de ter Python instalado em seu sistema.

3. Abra o terminal (ou prompt de comando) e navegue até o diretório onde você baixou/clonou este repositório.

4. Execute o script com os argumentos necessários. Veja abaixo os exemplos de uso:

### Exemplos de uso:

- Para validar CPFs em um único arquivo:

```bash
python cpf_inspector.py <arquivo_com_cpfs>
```

- Para validar CPFs em um único arquivo e salvar os resultados em um novo arquivo:

```bash
python cpf_inspector.py <arquivo_com_cpfs> -o <nome_do_arquivo_de_saída>
```

- Para validar CPFs em um único arquivo e exibir apenas os CPFs válidos:

```bash
python cpf_inspector.py -t <arquivo_com_cpfs>
```

- Para validar CPFs em vários arquivos em um diretório (*pode ser combinado com **-t** e **-o***):

```bash
python cpf_inspector.py -d <diretorio_com_arquivos>
```

- Para ver o manual da ferramenta:

```bash
python cpf_inspector.py -h
```

## Contribuindo

Sinta-se à vontade para contribuir com melhorias, sugestões ou relatar problemas. Basta abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter detalhes. 📝
