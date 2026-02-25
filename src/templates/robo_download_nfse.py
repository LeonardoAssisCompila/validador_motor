from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from db_mongo.banco_mongo import Banco_Mongo
from templates import robo_acesso
from templates import robo_cadastro
from config_dados import cnpj
import os

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
        #sucesso_cadastro = robo_cadastro.inicio(driver, fechar_driver=False)
        #if not sucesso_cadastro:
        #    print("Cadastro não foi concluído com sucesso. Encerrando o fluxo de download.")
        #    return False
        
        sucesso_acesso = robo_acesso.inicio(driver, fechar_driver=False)

        if not sucesso_acesso:
            print("Acesso não foi concluido ")
            return False

        #Função para ativar uploardPlanilha Escrituração
        banco = Banco_Mongo()
        uploard_planilha = banco.adicionar_robotizacao_nfse_por_cnpj(cnpj)
        print(f'Ativação do Serviço de UploadPlanilha - {uploard_planilha}')

        #Pagina recebidas
        driver.get('https://app.motorfiscal.com.br/consulta-nfes/recebidas')


        try:
            mensagem_tour = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Pular Tour")]'))
            )
            mensagem_tour.click()

        except TimeoutException:
            pass
        
        wait = WebDriverWait(driver, 10)
        aba_nfse = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Consulta NFs-e')]"))
        )
        aba_nfse.click()

        aba_recebidas = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="/consulta-nfses/recebidas"]'))
        )
        aba_recebidas.click()

        botao_upload = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Upload planilha')]"))
        )
        botao_upload.click()

        #Vamos enviar a planilha (dentro de src/planilha/planilha_nfse.xlsx)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho_arquivo = os.path.join(base_dir, "planilha", "planilha_nfse.xlsx")

        input_file = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        input_file.send_keys(caminho_arquivo)

        botao_enviar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.='Enviar']"))
        )
        botao_enviar.click()


        validar_sucesso(driver)

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
