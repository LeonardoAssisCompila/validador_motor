from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def validar_sucesso(driver: webdriver.Firefox) -> bool:

    try:
        WebDriverWait(driver, 20).until_not(EC.visibility_of_element_located((By.XPATH,'//*[contains(@class,"react-joyride__tooltip")]')))
        print("Cadastro realizado com sucesso!")
        return True
    except TimeoutException:
        print("Não foi possível confirmar o Acesso do motor")
        return False


def inicio():
    driver = None
    try:
        driver = webdriver.Firefox()
        driver.get('https://app.motorfiscal.com.br/entrar')
        
        email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='email']"))
        )
        email.send_keys('motor_teste@gmail.com')
    
        senha = driver.find_element(By.XPATH, "//input[@name='password']")
        senha.send_keys("Leonardo1!")
        
        #Entrar
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='sc-eDLKkx iTXGwv']"))
        )
        button.click()
        
        validar_sucesso(driver)

        input("Pressione ENTER para fechar o navegador...")
    except Exception as e:
        print("Erro navegação da Pagina do motor fiscal:", e)
    finally:
        if driver is not None:
            driver.quit()

inicio()
        #from db_mongo.banco_mongo import Banco_Mongo
        #banco = Banco_Mongo()
        #id_conta = banco.buscar_id_conta_por_email("motor_teste@gmail.com")
        #print(id_conta)