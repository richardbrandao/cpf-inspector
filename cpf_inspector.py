import argparse
import csv
import os

def banner():
    print("  __________  ______   ____                           __             ")
    print("  / ____/ __ \/ ____/  /  _/___  _________  ___  _____/ /_____  _____")
    print(" / /   / /_/ / /_      / // __ \/ ___/ __ \/ _ \/ ___/ __/ __ \/ ___/")
    print("/ /___/ ____/ __/    _/ // / / (__  ) /_/ /  __/ /__/ /_/ /_/ / /    ")
    print("\____/_/   /_/      /___/_/ /_/____/ .___/\___/\___/\__/\____/_/     ")
    print("                                  /_/ by:richardbrandao(git) ver: 1.1")
    print("")

def calcular_primeiro_digito_verificador(cpf):
    cpf_numerico = "".join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos do CPF

    pesos = [10, 9, 8, 7, 6, 5, 4, 3, 2]

    # Faz a soma ponderada dos 9 primeiros dígitos
    soma = sum(int(cpf_numerico[i]) * pesos[i] for i in range(9))

    resto = soma % 11

    # Calcula o primeiro dígito verificador
    if resto < 2:
        digito_verif_1 = 0
    else:
        digito_verif_1 = 11 - resto

    return digito_verif_1

def validar_cpf(cpf):
    cpf_numerico = ''.join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos do CPF

    if len(cpf_numerico) != 11:  # Verifica se o CPF tem 11 dígitos
        return False

    if cpf_numerico == cpf_numerico[0] * 11:  # Verifica se todos os dígitos são iguais
        return False

    digito_verif_1 = calcular_primeiro_digito_verificador(cpf_numerico)  # Calcula o primeiro dígito verificador

    if digito_verif_1 != int(cpf_numerico[9]):  # Verifica se o primeiro dígito verificador é igual ao fornecido
        return False

    return True

def formatar_cpf(cpf):  # Função para formatar um CPF no seguinte padrão >> XXX.XXX.XXX-XX
    cpf_numerico = "".join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos do CPF

    # Adiciona a formatação se o CPF tiver 11 dígitos
    if len(cpf_numerico) == 11:
        return f"{cpf_numerico[:3]}.{cpf_numerico[3:6]}.{cpf_numerico[6:9]}-{cpf_numerico[9:]}"
    else:
        return "000.000.000-00"  # Retorna CPF formatado padrão se não tiver 11 dígitos

def processar_arquivo(filename, output_filename, show_valid_only, writer):
    # Função para processar um arquivo de CPFs
    cpf_valido_encontrado = False  # Variável para verificar se algum CPF válido foi encontrado

    try:
        with open(filename, newline='') as file:
            if filename.endswith('.csv') or filename.endswith('.txt'):  # Verifica se o arquivo é CSV ou TXT
                reader = csv.reader(file)
                for row in reader:
                    cpf = row[0]  # Extrai o CPF da linha

                    if validar_cpf(cpf):  # Verifica se o CPF é válido
                        cpf_valido_encontrado = True
                        cpf_formatado = formatar_cpf(cpf)  # Formata o CPF
                        print(f"{cpf_formatado} - [VÁLIDO]")  # Exibe o CPF formatado como válido
                        if writer:
                            writer.writerow([cpf_formatado, 'VÁLIDO'])  # Escreve o CPF formatado como válido no arquivo de saída
                        elif output_filename:
                            print("[!] Erro: Não é possível escrever em um arquivo de saída.")
                    elif not show_valid_only:
                        print(f"{cpf} - [INVÁLIDO]")  # Exibe o CPF como inválido
                        if writer:
                            writer.writerow([cpf, 'INVÁLIDO'])  # Escreve o CPF como inválido no arquivo de saída
                        elif output_filename:
                            print("[!] Erro: Não é possível escrever em um arquivo de saída.")
            else:
                print(f"[!] Arquivo {filename} não é suportado. Apenas arquivos .csv e .txt são aceitos.")
                return

            if not cpf_valido_encontrado and show_valid_only:
                print("[!] Não foram encontrados CPFs válidos no arquivo informado.")  # Exibe uma mensagem se nenhum CPF válido for encontrado

    except FileNotFoundError:
        print(f'[!] O arquivo "{filename}" não foi encontrado.')  # Exibe uma mensagem se o arquivo não for encontrado
        print('[!] Certifique-se de que o arquivo esteja no mesmo diretório onde você está executando o script Python.')

    except FileNotFoundError:
        print(f'[!] O arquivo "{filename}" não foi encontrado.')  # Exibe uma mensagem se o arquivo não for encontrado
        print('[!] Certifique-se de que o arquivo esteja no mesmo diretório onde você está executando o script Python.')

def processar_diretorio(directory, output_filename, show_valid_only):
    if output_filename:
        with open(output_filename, 'w', newline='') as output_file:
            writer = csv.writer(output_file)  # Cria um escritor CSV
            for filename in os.listdir(directory):
                if filename.endswith(".csv") or filename.endswith(".txt"):  # Verifica se o arquivo é CSV ou TXT
                    print(f"Processando arquivo: {filename}")
                    processar_arquivo(os.path.join(directory, filename), output_filename, show_valid_only, writer)
                    print("")
    else:
        for filename in os.listdir(directory):
            if filename.endswith(".csv") or filename.endswith(".txt"):  # Verifica se o arquivo é CSV ou TXT
                print(f"Processando arquivo: {filename}")
                processar_arquivo(os.path.join(directory, filename), output_filename, show_valid_only, None)
                print("")

def main(filename, output_filename, show_valid_only, directory):
    if directory:
        processar_diretorio(directory, output_filename, show_valid_only)  # Processa o diretório se fornecido
    elif filename:
        if output_filename:
            with open(output_filename, 'w', newline='') as output_file:
                writer = csv.writer(output_file)  # Cria um escritor CSV
                processar_arquivo(filename, output_filename, show_valid_only, writer)  # Processa o arquivo se fornecido
        else:
            processar_arquivo(filename, output_filename, show_valid_only, None)  # Processa o arquivo se fornecido
    else:
        print("Você deve fornecer um arquivo CSV ou TXT ou um diretório contendo arquivos CSV e/ou TXT para validar.")  # Exibe uma mensagem se nenhum arquivo for fornecido

if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser(description="Verifica CPFs em um arquivo ou em vários arquivos em um diretório. Formatos aceitos: CSV e TXT.")
    parser.add_argument("filename", nargs='?', help="Nome do arquivo contendo os CPFs a serem verificados.")
    parser.add_argument("-t", "--true", action="store_true", help="Exibe apenas os CPFs válidos.")
    parser.add_argument("-o", "--output", help="Salva os resultados em um arquivo. Formatos aceitos: CSV e TXT.")
    parser.add_argument("-d", "--directory", help="Valida todos os arquivos dentro do diretório informado.")
    args = parser.parse_args()

    main(args.filename, args.output, args.true, args.directory)  # Chama a função principal com os argumentos fornecidos
