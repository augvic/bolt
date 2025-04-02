# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Bibliotecas.
import time
from scripts import utilitarios
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# ================================================== #

# ~~ Cria instância do navegador utilizando o webdriver.
def instanciar() -> webdriver.Chrome:

    """
    Resumo:
    - Cria instância do navegador.
    
    Parâmetros:
    - ===
    
    Retorna:
    - driver (webdriver.Chrome): Instância do navegador.
    
    Exceções:
    - ===
    """

    # ~~ Definindo configurações.
    options = Options()
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("detach", True)

    # ~~ Criando instância.
    driver = webdriver.Chrome(options=options)
    abas_abertas = driver.window_handles
    if len(abas_abertas) > 1:
        driver.switch_to.window(abas_abertas[0])
        driver.close()
    try:
        driver.switch_to.window(abas_abertas[0])
    except:
        driver.switch_to.window(abas_abertas[1])

    # ~~ Retorna instância.
    return driver

# ================================================== #

# ~~ Acessa e loga na GoDeep.
def acessar_godeep(driver: webdriver.Chrome) -> None:

    """
    Resumo:
    - Acessa e loga na GoDeep.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Acessando GoDeep e fazendo login.
    driver.get(f"https://www.revendedorpositivo.com.br/admin/")
    microsoft_login_botao = None
    try:
        microsoft_login_botao = driver.find_element(By.ID, value="login-ms-azure-ad")
        microsoft_login_botao.click()
        time.sleep(5)
        body = driver.find_element(By.TAG_NAME, value="body").text
        if any(login_string in body for login_string in ["Because you're accessing sensitive info, you need to verify your password.", "Sign in", "Pick an account", "Entrar"]):
            utilitarios.printar_mensagem(mostrar_data_hora="Only")
            input("Necessário logar conta Microsoft. Aperte ENTER aqui depois para continuar.")
            utilitarios.printar_mensagem(char_type="=", char_qtd=50)
        if "Approve sign in request" in body:
            time.sleep(3)
            codigo = driver.find_element(By.ID, value="idRichContext_DisplaySign").text
            utilitarios.printar_mensagem(mostrar_data_hora="Only")
            input(f"Necessário authenticator Microsoft para continuar: {codigo}. Aperte ENTER aqui depois para continuar.")
            utilitarios.printar_mensagem(char_type="=", char_qtd=50)
    except:
        driver.get(f"https://www.revendedorpositivo.com.br/admin/index/")

# ================================================== #

# ~~ Verifica status de assinatura de cliente na GoDeep.
def coletar_status_assinatura_godeep(driver: webdriver.Chrome, cnpj: str) -> str:

    """
    Resumo:
    - Verifica status de assinatura de cliente na GoDeep.

    Parâmetros:
    - cnpj (str)
    - driver (webdriver.Chrome)

    Retorna:
    - status (str):
        - "Sem Cadastro"
        - "Atualizar Cadastro"
        - "Cadastro Concluído"
        - "Assinatura Incompleta"
        - "Aguardando Assinatura"

    Exceções:
    - ===
    """

    # ~~ Valor padrão.
    status = ""

    # ~~ Acessa site e acessa aba da DocuSign. Se não encontrar cliente, é porque ele não possui cadastro.
    try:
        driver.get("https://www.revendedorpositivo.com.br/admin/clients")
        pesquisa = driver.find_element(By.ID, value="keyword") 
        pesquisa.clear()
        pesquisa.send_keys(cnpj)
        pesquisa.send_keys(Keys.ENTER)
        time.sleep(3)
        editar = driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
        editar = editar.get_attribute("href")
        driver.get(str(editar)) 
        time.sleep(3)
        docu_sign = driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[14].find_element(By.XPATH, value=".//a").get_attribute("href")
        driver.get(str(docu_sign))
    except:
        status = "Sem Cadastro"
        return status

    # ~~ Se status não for "Sem Cadastro", procura status do documento.
    if status == "":
        docs = driver.find_elements(By.XPATH, value="//table[@class='table-bordered table-striped table-condensed cf']/tbody/tr")
        for doc in docs:
            sem_documento = doc.find_elements(By.XPATH, value=".//td")[0].text
            if sem_documento == "Não foram encontrados registros.":
                status = "Atualizar Cadastro"
                break
            status = doc.find_elements(By.XPATH, value=".//td")[1].text
            if status == "completed":
                status = "Cadastro Concluído"
                break
            elif status == "delivered":
                status = "Assinatura Incompleta"
            elif status == "sent":
                status = "Aguardando Assinatura"  

    # ~~ Retorna status.
    return status

# ================================================== #

# ~~ Fecha navegador.
def fechar(driver: webdriver.Chrome) -> None:

    """
    Resumo:
    - Fecha o navegador.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Fecha navegador.
    driver.quit()

# ================================================== #