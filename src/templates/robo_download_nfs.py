from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from templates import robo_acesso
from templates import robo_cadastro

#TODO lembra de coloca a função que deleta conta nesse modulo ainda

def validar_sucesso(driver: webdriver.Firefox) -> bool:

    try:
        WebDriverWait(driver, 20).until_not(EC.url_contains("/cadastrar"))
        print("Cadastro realizado com sucesso!")
        return True
    except TimeoutException:
        print("Não foi possível confirmar o sucesso do cadastro (URL não mudou).")
        return False


def inicio(driver: webdriver.Firefox):
    try:
        # chama o robô de cadastro e, se der certo, continua o fluxo deste robô
        sucesso_cadastro = robo_cadastro.inicio(driver, fechar_driver=False)

        if not sucesso_cadastro:
            print("Cadastro não foi concluído com sucesso. Encerrando o fluxo de download.")
            return False
        
        sucesso_acesso = robo_acesso.inicio(driver, fechar_driver=False)

        if not sucesso_acesso:
            print("Acesso não foi concluido ")
            return False


        # validação final de sucesso
        validar_sucesso(driver)

        input("Pressione ENTER para fechar o navegador...")
        return True
    except Exception as e:
        print("Erro navegação da Pagina do motor fiscal:", e)
        return False
    finally:
        if driver is not None:
            driver.quit()

if __name__ == "__main__":
    driver = webdriver.Firefox()
    try:
        driver.get('https://app.motorfiscal.com.br/entrar')
        inicio(driver)
    finally:
        driver.quit()
