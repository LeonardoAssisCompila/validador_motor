from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def validar_sucesso(driver: webdriver.Firefox) -> bool:

    try:
        WebDriverWait(driver, 20).until_not(EC.url_contains("/cadastrar"))
        print("Cadastro realizado com sucesso!")
        return True
    except TimeoutException:
        print("Não foi possível confirmar o sucesso do cadastro (URL não mudou).")
        return False


def inicio():
    driver = None
    try:
        driver = webdriver.Firefox()
        driver.get('https://app.motorfiscal.com.br/entrar')
        
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/cadastrar")]'))
        )
        button.click()
        
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//span[contains(text(),"Cadastrar no MotorFiscal")]')))
        
        nome = driver.find_element(By.ID, "form_cadastro-nome")
        nome.send_keys("Teste Motor")

        email = driver.find_element(By.ID, "form_cadastro-email")
        email.send_keys("motor_teste@gmail.com")

        telefone = driver.find_element(By.ID, "form_cadastro-telefone")
        telefone.send_keys("11956128238")

        #lembra de colocar a mensagem Senha deve conter: mínimo 8 caracteres, números, letras maiúsculas, caracteres especiais
        telefone = driver.find_element(By.ID, "form_cadastro-pass")
        telefone.send_keys("Leonardo1!")

        aceito = driver.find_element(By.ID,"form_cadastro-licensa")
        aceito.click()

        #Proximo
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'form_cadastro-usuario_btn'))
        )
        button.click()

        WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.ID,'form_cadastro-cnpj')))
        
        nome = driver.find_element(By.ID, "form_cadastro-cnpj")
        nome.send_keys("43.456.133/0001-80")

        email = driver.find_element(By.ID, "form_cadastro-razao")
        email.send_keys("Teste Motor")
        
        wait = WebDriverWait(driver, 10)
        
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//span[normalize-space()='Estado']/following::button[contains(@class,'dropdown-toggle')][1]"
            ))
        ).click()
        
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//ul//span[normalize-space()='São Paulo']"
            ))
        ).click()
        
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//span[normalize-space()='Cidade']/following::button[contains(@class,'dropdown-toggle')][1]"
            ))
        ).click()
        
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//ul//span[normalize-space()='Campinas']"
            ))
        ).click()

        #Proximo
        proximo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'form_cadastro-empresa_btn'))
        )
        proximo.click()


        #Pula
        pula = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'form_cadastro-skip_btn'))
        )
        pula.click()

        #adicionar depois
        pula_depois = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'form_cadastro-add_later_btn'))
        )
        pula_depois.click()

        # validação final de sucesso
        validar_sucesso(driver)

        input("Pressione ENTER para fechar o navegador...")
    except Exception as e:
        print("Erro navegação da Pagina do motor fiscal:", e)
    finally:
        if driver is not None:
            driver.quit()

inicio()
