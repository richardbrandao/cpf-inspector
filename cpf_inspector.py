import argparse
import csv
import os

def banner():
    print("  __________  ______   ____                           __             ")
    print("  / ____/ __ \/ ____/  /  _/___  _________  ___  _____/ /_____  _____")
    print(" / /   / /_/ / /_      / // __ \/ ___/ __ \/ _ \/ ___/ __/ __ \/ ___/")
    print("/ /___/ ____/ __/    _/ // / / (__  ) /_/ /  __/ /__/ /_/ /_/ / /    ")
    print("\____/_/   /_/      /___/_/ /_/____/ .___/\___/\___/\__/\____/_/     ")
    print("                                  /_/ by:richardbrandao(git) ver: 1.0")
    print("")

def calcular_primeiro_digito_verificador(cpf):
    cpf_numerico = "".join(filter(str.isdigit, cpf))

    pesos = [10, 9, 8, 7, 6, 5, 4, 3, 2]

    soma = sum(int(cpf_numerico[i]) * pesos[i] for i in range(9))

    resto = soma % 11

    if resto < 2:
        digito_verif_1 = 0
    else:
        digito_verif_1 = 11 - resto

    return digito_verif_1

def validar_cpf(cpf):
    cpf_numerico = ''.join(filter(str.isdigit, cpf))

    if len(cpf_numerico) != 11:
        return False

    if cpf_numerico == cpf_numerico[0] * 11:
        return False

    digito_verif_1 = calcular_primeiro_digito_verificador(cpf_numerico)

    if digito_verif_1 != int(cpf_numerico[9]):
        return False

    return True

def processar_arquivo(filename, output_filename, show_valid_only, writer):
    cpf_valido_encontrado = False

    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                cpf = row[0]
                if validar_cpf(cpf):
                    cpf_valido_encontrado = True
                    print(f"{cpf} - [VÁLIDO]")
                    if writer:
                        writer.writerow([cpf, 'VÁLIDO'])
                    elif output_filename:
                        print("Erro: Não é possível escrever em um arquivo de saída.")
                elif not show_valid_only:
                    print(f"{cpf} - [INVÁLIDO]")
                    if writer:
                        writer.writerow([cpf, 'INVÁLIDO'])
                    elif output_filename:
                        print("Erro: Não é possível escrever em um arquivo de saída.")
            if not cpf_valido_encontrado and show_valid_only:
                print("[!] Não foram encontrados CPFs válidos no arquivo informado.")
    except FileNotFoundError:
        print(f'[!] O arquivo "{filename}" não foi encontrado.')
        print('[!] Certifique-se de que o arquivo esteja no mesmo diretório onde você está executando o script Python.')

def processar_diretorio(directory, output_filename, show_valid_only):
    if output_filename:
        with open(output_filename, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            for filename in os.listdir(directory):
                if filename.endswith(".csv"):
                    print(f"Processando arquivo: {filename}")
                    processar_arquivo(os.path.join(directory, filename), output_filename, show_valid_only, writer)
                    print("")
    else:
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                print(f"Processando arquivo: {filename}")
                processar_arquivo(os.path.join(directory, filename), output_filename, show_valid_only, None)
                print("")

def main(filename, output_filename, show_valid_only, directory):
    if directory:
        processar_diretorio(directory, output_filename, show_valid_only)
    elif filename:
        if output_filename:
            with open(output_filename, 'w', newline='') as output_file:
                writer = csv.writer(output_file)
                processar_arquivo(filename, output_filename, show_valid_only, writer)
        else:
            processar_arquivo(filename, output_filename, show_valid_only, None)
    else:
        print("Você deve fornecer um arquivo CSV ou um diretório contendo arquivos CSV para validar.")

if __name__ == "__main__":
    banner()
    parser = argparse.ArgumentParser(description="Verifica CPFs em um arquivo CSV ou em vários arquivos CSV em um diretório.")
    parser.add_argument("filename", nargs='?', help="Nome do arquivo CSV contendo os CPFs a serem verificados.")
    parser.add_argument("-t", "--true", action="store_true", help="Exibe apenas os CPFs válidos.")
    parser.add_argument("-o", "--output", help="Salva os resultados em um arquivo CSV.")
    parser.add_argument("-d", "--directory", help="Valida todos os arquivos CSV dentro do diretório informado.")
    args = parser.parse_args()

    main(args.filename, args.output, args.true, args.directory)
