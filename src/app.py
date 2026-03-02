import os
import time
from selenium import webdriver
from templates import robo_cadastro
from templates import robo_download_nfse
from templates import robo_download_nfe
from templates import robo_download_cte
from templates import robo_acesso


def limpar():
    os.system("clear") 


def menu():
    limpar()
    
    verde = "\033[92m"
    azul = "\033[94m"
    amarelo = "\033[93m"
    reset = "\033[0m"
    vermelho = "\033[91m"

    print(verde + "=" * 50)
    print("VALIDADOR DO MOTOR FISCAL".center(50))
    print("=" * 50 + reset)

    print(azul + "\nSelecione o teste que deseja executar:\n" + reset)

    print(f"{amarelo}[ 1 ]{reset} - Teste de Cadastro de Usuário")
    print(f"{amarelo}[ 2 ]{reset} - Teste de Download de NFS-e")
    print(f"{amarelo}[ 3 ]{reset} - Teste de Download de NF-e")
    print(f"{amarelo}[ 4 ]{reset} - Teste de Download de CT-e")
    print(f"{amarelo}[ 5 ]{reset} - Teste de Acesso ao Motor")


    print("\n" + "=" * 50)

    while True:
        try:
            opcao = int(input("\nDigite o número do teste desejado: "))
            if opcao in [1, 2, 3, 4, 5]:
                return opcao
            else:
                print("Opção inválida. Escolha entre 1 e 5.")
        except ValueError:
            print("Digite apenas números.")

usuario = menu()

inicio_teste = time.time()

driver = webdriver.Firefox()
driver.get('https://app.motorfiscal.com.br/entrar')
vermelho = "\033[91m"
azul = "\033[94m"

robos = {
    1: robo_cadastro,
    2: robo_download_nfse,
    3: robo_download_nfe,
    4: robo_download_cte,
    5: robo_acesso
}
opcao = robos.get(usuario)

if opcao:
    servico_robo = opcao.__name__.split('.')[-1]
    print(f'{azul} Inicializando o robo {servico_robo}')
    opcao.inicio(driver)
else:
    print(f"{vermelho}\nVocê escolheu a opção {usuario}, mas ainda não está implementada.")

fim_teste = time.time()
duracao_segundos = fim_teste - inicio_teste
duracao_minutos = duracao_segundos / 60

print(f"\nTempo total de execução: {duracao_segundos:.2f} segundos (~{duracao_minutos:.2f} minutos).")
