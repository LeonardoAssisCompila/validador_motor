from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from db_mongo.banco_mongo import Banco_Mongo
from templates import robo_acesso
from templates import robo_cadastro
from config_dados import cnpj, email
import os

#TODO lembra de coloca a função que deleta conta nesse modulo ainda

def validar_sucesso(driver: webdriver.Firefox) -> bool:

    try:
        WebDriverWait(driver, 20).until_not(EC.url_contains("/cadastrar"))
        print("Cadastro realizado com sucesso!")
        return True
    except TimeoutException:
        print("Não foi possível confirmar o sucesso do cadastro.")
        return False


def inicio(driver: webdriver.Firefox):
    try:
        amarelo = "\033[93m"
        vermelho = "\033[91m"
        verde = "\033[92m"

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
        #uploard_planilha = banco.adicionar_robotizacao_nfse_por_cnpj(cnpj)
        #print(f'Ativação do Serviço de UploadPlanilha - {uploard_planilha}')

        #Pagina recebidas
        driver.get('https://app.motorfiscal.com.br/consulta-nfes/recebidas')


        try:
            mensagem_tour = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Pular Tour")]'))
            )
            mensagem_tour.click()

        except TimeoutException:
            pass
        
        wait = WebDriverWait(driver, 30)
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

        # Aguarda eventual overlay de carregamento sair da frente do botão
        try:
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.sc-lnsjTu.fTQwpL"))
            )
        except TimeoutException:
            print("Aviso: overlay de carregamento não sumiu; tentando clicar assim mesmo.")
        
        try:
            botao_upload.click()
        except Exception:
            driver.execute_script("arguments[0].click();", botao_upload)

        #Vamos enviar a planilha (dentro de src/planilha/planilha_nfse.xlsx)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho_arquivo = os.path.join(base_dir, "planilha", "planilha_nfse.xlsx")

        input_file = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        input_file.send_keys(caminho_arquivo)

        botao_enviar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.='Enviar']"))
        )
        botao_enviar.click()

        #Esperar carregar
        try:
            print(f"{amarelo} Processando Planilha... tempo maximo 120 segundos")

            WebDriverWait(driver, 120).until(
                EC.invisibility_of_element_located((By.XPATH, "//h2[normalize-space()='Carregar Planilha']"))
            )

            #Resumo do Processamento
            WebDriverWait(driver,120).until(
                EC.element_to_be_clickable((By.XPATH, "//h2[contains(., 'Resumo do Processamento')]"))
            )
            #Função para apagar a nota no banco deixei a nota com erro depois passa pendente s
            banco.apagar_nota_nfse_do_cnpj(cnpj)
        
        except TimeoutException:
            print(f"{vermelho}Timeout: processamento excedeu o tempo limite de 120 segundos.")
        
        #consulta na colletion usuario passando o email para pega o id da conta
        id_conta = banco.buscar_id_conta_por_email(email)
        print(id_conta)        

        #Vamos apagar a conta
        apagou = banco.apagar_conta_cnpj(cnpj, id_conta)
        print(apagou)

        
        if resp_db == True:
            print(f'{verde} Nota apagada do banco do CNPJ: {cnpj}')
        else:
            print(f'{vermelho} Erro ao apagar nota do CNPJ: {cnpj}')


        validar_sucesso(driver)

        return True
    except Exception as e:
        print(f"{vermelho}Erro navegação da Pagina do motor fiscal:", e)
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

