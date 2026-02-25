import os
from templates import robo_cadastro
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



def limpar():
    os.system("clear") 


def menu():
    limpar()
    
    verde = "\033[92m"
    azul = "\033[94m"
    amarelo = "\033[93m"
    reset = "\033[0m"

    print(verde + "=" * 50)
    print("VALIDADOR DO MOTOR FISCAL".center(50))
    print("=" * 50 + reset)

    print(azul + "\nSelecione o teste que deseja executar:\n" + reset)

    print(f"{amarelo}[ 1 ]{reset} - Teste de Cadastro de Usuário")
    print(f"{amarelo}[ 2 ]{reset} - Teste de Download de NFS-e")
    print(f"{amarelo}[ 3 ]{reset} - Teste de Download de NF-e")
    print(f"{amarelo}[ 4 ]{reset} - Teste de Download de CT-e")

    print("\n" + "=" * 50)

    while True:
        try:
            opcao = int(input("\nDigite o número do teste desejado: "))
            if opcao in [1, 2, 3, 4]:
                return opcao
            else:
                print("Opção inválida. Escolha entre 1 e 4.")
        except ValueError:
            print("Digite apenas números.")

usuario = menu()

driver = webdriver.Firefox()
driver.get('https://app.motorfiscal.com.br/entrar')

if usuario == 1:
    robo_cadastro.inicio(driver)
else:
    print(f"\n Você escolheu a opção {usuario}, mas ainda não está implementada.")
