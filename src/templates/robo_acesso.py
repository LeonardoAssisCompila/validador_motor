from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config_dados import email, senha
from selenium.webdriver.common.action_chains import ActionChains
import time

def validar_sucesso(driver: webdriver.Firefox) -> bool:
    verde = "\033[92m"
    azul = "\033[94m"
    amarelo = "\033[93m"
    reset = "\033[0m"
    vermelho = "\033[91m"

    try:
        WebDriverWait(driver, 20).until_not(EC.url_contains("/cadastrar"))
        print(f"{verde}realizado acesso no motor com sucesso!")
        return True
    except TimeoutException:
        print(f"{vermelho}Não foi possível confirmar o sucesso do acesso.")
        return False


def inicio(driver: webdriver.Firefox, fechar_driver: bool = True) -> bool:
    try:

        email_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='email']"))
        )
        email_input.send_keys(email)
    
        senha_input = driver.find_element(By.XPATH, "//input[@name='password']")
        senha_input.send_keys(senha)

        for tentativa in range(3):
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@class='sc-eDLKkx iTXGwv']"))
                )

                actions = ActionChains(driver)
                actions.double_click(button).perform()

                time.sleep(1)
                button = driver.find_element(By.XPATH, "//button[@class='sc-eDLKkx iTXGwv']")

                if button.is_enabled():
                    pass
                else:
                    break

            except Exception as e:
                time.sleep(2)

        # validação final de sucesso
        sucesso = validar_sucesso(driver)

        return sucesso
    except Exception as e:
        print("Erro navegação da Pagina do motor fiscal:", e)
        return False
    finally:
        if fechar_driver and driver is not None:
            driver.quit()

if __name__ == "__main__":
    driver = webdriver.Firefox()
    try:
        driver.get('https://app.motorfiscal.com.br/entrar')
        inicio(driver)
    finally:
        driver.quit()
