from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config_dados import cnpj_formatado, email, telefone, senha, razao
def validar_sucesso(driver: webdriver.Firefox) -> bool:

    try:
        WebDriverWait(driver, 20).until_not(EC.url_contains("/cadastrar"))
        print("Cadastro realizado com sucesso!")
        return True
    except TimeoutException:
        print("Não foi possível confirmar o sucesso do cadastro (URL não mudou).")
        return False


def inicio(driver: webdriver.Firefox, fechar_driver: bool = True) -> bool:
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/cadastrar")]'))
        )
        button.click()
        
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//span[contains(text(),"Cadastrar no MotorFiscal")]')))
        
        nome = driver.find_element(By.ID, "form_cadastro-nome")
        nome.send_keys(razao)

        email_input = driver.find_element(By.ID, "form_cadastro-email")
        email_input.send_keys(email)

        telefone_input = driver.find_element(By.ID, "form_cadastro-telefone")
        telefone_input.send_keys(telefone)

        telefone_input = driver.find_element(By.ID, "form_cadastro-pass")
        telefone_input.send_keys(senha)

        aceito = driver.find_element(By.ID,"form_cadastro-licensa")
        aceito.click()

        #Proximo
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'form_cadastro-usuario_btn'))
        )
        button.click()

        WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.ID,'form_cadastro-cnpj')))
        
        cnpj_input = driver.find_element(By.ID, "form_cadastro-cnpj")
        cnpj_input.send_keys(cnpj_formatado)

        razao_input = driver.find_element(By.ID, "form_cadastro-razao")
        razao_input.send_keys(razao)
        
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
