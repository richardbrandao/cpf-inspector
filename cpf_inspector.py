import argparse
import csv
import os
import colorama

colorama.init()

def banner():
    print(colorama.Fore.CYAN +         r"   __________  ______   ____                           __            ")
    print(colorama.Fore.CYAN +         r"  / ____/ __ \/ ____/  /  _/___  _________  ___  _____/ /_____  _____")
    print(colorama.Fore.LIGHTBLUE_EX + r" / /   / /_/ / /_      / // __ \/ ___/ __ \/ _ \/ ___/ __/ __ \/ ___/")
    print(colorama.Fore.LIGHTBLUE_EX + r"/ /___/ ____/ __/    _/ // / / (__  ) /_/ /  __/ /__/ /_/ /_/ / /    ")
    print(colorama.Fore.BLUE +         r"\____/_/   /_/      /___/_/ /_/____/ .___/\___/\___/\__/\____/_/     ")
    print(colorama.Fore.BLUE +         r"                                  /_/" + colorama.Fore.MAGENTA + f"  by:richardbrandao(git) {versao_atual}")
    print(colorama.Style.RESET_ALL)

versao_atual = "v1.0.0"
repo_zip_url = "https://github.com/richardbrandao/cpf-inspector/archive/refs/heads/main.zip"
repo_folder_name = "cpf-inspector"

def calcular_primeiro_digito_verificador(cpf):
    cpf_numerico = "".join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos do CPF

    pesos = [10, 9, 8, 7, 6, 5, 4, 3, 2]

    soma = sum(int(cpf_numerico[i]) * pesos[i] for i in range(9)) # Faz a soma ponderada dos 9 primeiros dígitos

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

def formatar_cpf(cpf):  # Função para formatar um CPF no seguinte padrão >> XYZ.XYZ.XYZ-YZ
    cpf_numerico = "".join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos do CPF

    # Adiciona a formatação se o CPF tiver 11 dígitos
    if len(cpf_numerico) == 11:
        return f"{cpf_numerico[:3]}.{cpf_numerico[3:6]}.{cpf_numerico[6:9]}-{cpf_numerico[9:]}"

def processar_arquivo(filename, output_filename, show_valid_only, writer):
    cpf_valido_encontrado = False  # Variável para verificar se algum CPF válido foi encontrado
    total_cpfs = 0
    cpfs_validos = 0
    cpfs_invalidos = 0

    try:
        with open(filename, newline='') as file:
            if filename.endswith('.csv') or filename.endswith('.txt'):  # Verifica se o arquivo é CSV ou TXT
                reader = csv.reader(file)

                print(" Nº" + " " * 8 + "CPF" + " " * 26 + "STATUS") # Monta o cabeçalho
                print("-" * 46)

                for row in reader:
                    cpf = row[0]  # Extrai o CPF da linha
                    total_cpfs += 1
                    if validar_cpf(cpf):  # Verifica se o CPF é válido
                        cpfs_validos += 1
                        cpf_valido_encontrado = True
                        cpf_formatado = formatar_cpf(cpf)  # Formata o CPF
                        print(f"[{total_cpfs}]".ljust(5) + f" {(cpf_formatado).ljust(35)}" + "[" + colorama.Fore.LIGHTGREEN_EX + "✓" + colorama.Style.RESET_ALL + "]")  # Exibe o CPF formatado como válido
                        if writer:
                            writer.writerow([cpf_formatado, 'VALIDO'])  # Escreve o CPF formatado como válido no arquivo de saída
                        elif output_filename:
                            print("[!] Erro: Não é possível escrever em um arquivo de saída.")
                    elif not show_valid_only:
                        cpfs_invalidos += 1
                        print(f"[{total_cpfs}]".ljust(5) + f" {(cpf).ljust(35)}" + "[" + colorama.Fore.RED + "X" + colorama.Style.RESET_ALL + "]")  # Exibe o CPF como inválido
                        if writer:
                            writer.writerow([cpf, 'INVALIDO'])  # Escreve o CPF como inválido no arquivo de saída
                        elif output_filename:
                            print("[!] Erro: Não é possível escrever em um arquivo de saída.")

                # Exibir estatísticas ao final do processamento
                print("-" * 46)
                print("\nEstatísticas de Validação:")
                print("Total de CPFs:".ljust(15) + f"{(total_cpfs)}")
                print("CPF válidos:".ljust(15) + f"{cpfs_validos}")
                print("CPF inválidos:".ljust(15) + f"{cpfs_invalidos}")

            else:
                print(f"[!] Arquivo {filename} não é suportado. Apenas arquivos .csv e .txt são aceitos.")
                return

            if not cpf_valido_encontrado and show_valid_only:
                print("[!] Não foram encontrados CPFs válidos no arquivo informado.")

    except FileNotFoundError:
        print(f'[!] O arquivo "{filename}" não foi encontrado.')
        print('[!] Certifique-se de que o caminho do arquivo esteja correto.')

def processar_diretorio(directory, output_filename, show_valid_only):
    try:
        if output_filename:
            with open(output_filename, 'w', newline='') as output_file:
                writer = csv.writer(output_file)  # Cria um escritor CSV
                for filename in os.listdir(directory):
                    if filename.endswith(".csv") or filename.endswith(".txt"):  # Verifica se o arquivo é CSV ou TXT
                        print(f"Arquivo: {filename}\n")
                        processar_arquivo(os.path.join(directory, filename), output_filename, show_valid_only, writer)
                        print("")
        else:
                for filename in os.listdir(directory):
                    if filename.endswith(".csv") or filename.endswith(".txt"):  # Verifica se o arquivo é CSV ou TXT
                        print(f"Arquivo: {filename}\n")
                        processar_arquivo(os.path.join(directory, filename), output_filename, show_valid_only, None)
                        print("")
    
    except FileNotFoundError:
        print(f'[!] O diretório "{directory}" não foi encontrado.')
        print('[!] Verifique se o caminho para o diretório está correto.')

def main(filename, output_filename, show_valid_only, directory):
    if directory:
        processar_diretorio(directory, output_filename, show_valid_only)  # Processa o diretório se fornecido
        print()
    elif filename:
        if output_filename:
            with open(output_filename, 'w', newline='') as output_file:
                writer = csv.writer(output_file)  # Cria um escritor CSV
                processar_arquivo(filename, output_filename, show_valid_only, writer)  # Processa o arquivo se fornecido
        else:
            processar_arquivo(filename, output_filename, show_valid_only, None)  # Processa o arquivo se fornecido
        print()
    else:
        print("Você deve fornecer um arquivo CSV ou TXT ou um diretório contendo arquivos CSV e/ou TXT para validar.")
        print("Para mais informações, digite: " + colorama.Fore.LIGHTYELLOW_EX + "python cpf_inspector.py --help\n")

if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser(description="Verifica CPFs em um arquivo ou em vários arquivos em um diretório. Formatos aceitos: CSV e TXT.")
    parser.add_argument("filename", nargs='?', help="Nome do arquivo contendo os CPFs a serem verificados.")
    parser.add_argument("-t", "--true", action="store_true", help="Exibe apenas os CPFs válidos.")
    parser.add_argument("-o", "--output", help="Salva os resultados em um arquivo. Formatos aceitos: CSV e TXT.")
    parser.add_argument("-d", "--directory", help="Valida todos os arquivos dentro do diretório informado.")
    args = parser.parse_args()

    main(args.filename, args.output, args.true, args.directory)  # Chama a função principal com os argumentos fornecidos
