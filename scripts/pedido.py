# ================================================== #

# ~~ Bibliotecas.
import time
import os
import pandas_tools
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# ================================================== #

# ~~ Acessa pedido no site.
def acessar(driver: webdriver.Chrome, pedido: int) -> None:

    """
    Resumo:
    - Acessa a página do pedido no site.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    - pedido (int)
    
    Retorna:
    - ===
    
    Exceções:
    - "Pedido {pedido} não inserido no site ainda."
    """

    # ~~ Acessa pedido.
    driver.get(f"https://www.revendedorpositivo.com.br/admin/orders/edit/id/{pedido}")

    # ~~ Coleta conteúdo da página.
    conteúdo_página = driver.find_element(By.TAG_NAME, value="body").text

    # ~~ Se pedido não foi inputado ainda, retorna erro.
    if "Application error: Mysqli statement execute error" in conteúdo_página:
        raise Exception(f"Pedido {pedido} não inserido no site ainda.")

# ================================================== #

# ~~ Coleta data do pedido.
def coletar_data(driver: webdriver.Chrome) -> datetime:

    """
    Resumo:
    - Coleta a data do pedido no site. Página do pedido deve estar aberta.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    
    Retorna:
    - data (datetime)
    
    Exceções:
    - ===
    """

    # ~~ Coleta data.
    data = driver.find_element(By.XPATH, value="//label[@for='order_date']/following-sibling::div[@class='col-md-12']").text

    # ~~ Converte para datetime.
    data = datetime.strptime(data, "%d/%m/%Y %H:%M:%S")

    # ~~ Retorna a data.
    return data

# ================================================== #

# ~~ Coleta condição de pagamento do pedido.
def coletar_condição_pagamento(driver: webdriver.Chrome) -> str:

    """
    Resumo:
    - Coleta a condição de pagamento do pedido no site. Página do pedido deve estar aberta.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    
    Retorna:
    - condição_pagamento (str)
    
    Exceções:
    - ===
    """

    # ~~ Coleta condição de pagamento.
    condição_pagamento = driver.find_element(By.XPATH, value="//label[@for='payment_slip_installments_description']/following-sibling::div[@class='col-md-12']").text

    # ~~ Retorna a condição de pagamento.
    return condição_pagamento

# ================================================== #

# ~~ Coleta forma de pagamento do pedido.
def coletar_forma_pagamento(driver: webdriver.Chrome) -> str:

    """
    Resumo:
    - Coleta a forma de pagamento do pedido no site. Página do pedido deve estar aberta.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    
    Retorna:
    - forma_pagamento (str)
    
    Exceções:
    - ===
    """

    # ~~ Coleta forma de pagamento.
    forma_pagamento = driver.find_element(By.XPATH, value="//label[@for='payment_name']/following-sibling::div[@class='col-md-12']").text
    lista_pagamentos_hífen = ["Boleto à Vista - Log - Imprimir", "Elo - Log", "Visa - Log", "Master - Log", "Pix - Log"]
    if forma_pagamento in lista_pagamentos_hífen:
        forma_pagamento = forma_pagamento.split(" - ")[0]

    # ~~ Retorna forma de pagamento.
    return forma_pagamento

# ================================================== #

# ~~ Coleta CNPJ do cliente.
def coletar_cnpj(driver: webdriver.Chrome) -> str:

    """
    Resumo:
    - Coleta o CNPJ do cliente no site. Página do pedido deve estar aberta.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    
    Retorna:
    - cnpj (str)
    
    Exceções:
    - ===
    """

    # ~~ Coleta CNPJ.
    cnpj = driver.find_element(By.XPATH, value="//label[@for='client_cnpj']/following-sibling::div[@class='col-md-12']").text

    # ~~ Retorna CNPJ.
    return cnpj

# ================================================== #

# ~~ Coleta valor do pedido.
def coletar_valor(driver: webdriver.Chrome) -> float:

    """
    Resumo:
    - Coleta o valor do pedido no site. Página do pedido deve estar aberta.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    
    Retorna:
    - valor_pedido (float)
    
    Exceções:
    - ===
    """

    # ~~ Coleta valor do pedido.
    valor_pedido = driver.find_element(By.XPATH, value="//label[@for='payment_value']/following-sibling::div[@class='col-md-12']").text 
    valor_pedido = valor_pedido.replace("R$", "").replace(".", "").replace(",", ".")
    valor_pedido = float(valor_pedido)

    # ~~ Retorna valor do pedido.
    return valor_pedido

# ================================================== #

# ~~ Coleta status do pedido.
def coletar_status(driver: webdriver.Chrome) -> str:

    """
    Resumo:
    - Coleta o status do pedido no site. Página do pedido deve estar aberta.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    
    Retorna:
    - status_pedido (str):
        - "CANCELADO"
        - "FATURADO"
        - "RECUSADO"
        - "LIBERADO"
        - "RECEBIDO"
    
    Exceções:
    - ===
    """

    # ~~ Coleta status do pedido.
    try: 
        status_pedido = driver.find_element(By.NAME, value="distribution_centers[1][status]")
    except: 
        try:
            status_pedido = driver.find_element(By.NAME, value="distribution_centers[2][status]")
        except:
            status_pedido = driver.find_element(By.NAME, value="distribution_centers[3][status]") 
    status_pedido = Select(status_pedido) 
    status_pedido = status_pedido.first_selected_option.text

    # ~~ Converte status.
    if status_pedido == "Cancelado pela positivo":
        status_pedido = "CANCELADO"
    elif status_pedido in ["Expedido", "Expedido parcial"]:
        status_pedido = "FATURADO"
    elif status_pedido == "Recusado pelo crédito":
        status_pedido = "RECUSADO"
    elif status_pedido in ["Pedido integrado", "Em separação", "Crédito aprovado", "Faturado"]:
        status_pedido = "LIBERADO"
    elif status_pedido == "Pedido recebido":
        status_pedido = "RECEBIDO"

    # ~~ Retorna status.
    return status_pedido

# ================================================== #

# ~~ Coleta razão social do pedido.
def coletar_razao_social(driver: webdriver.Chrome) -> str:

    """
    Resumo:
    - Coleta a razão social do pedido no site. Página do pedido deve estar aberta.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    
    Retorna:
    - razão_social (str)
    
    Exceções:
    - ===
    """

    # ~~ Coleta razão social.
    razão_social = driver.find_element(By.XPATH, value="//label[@for='client_name_corporate']/following-sibling::div[@class='col-md-12']").text
    try:
        razão_social = str(razão_social).split(" (")[0]
    except:
        pass

    # ~~ Retorna.
    return razão_social

# ================================================== #

# ~~ Coleta código ERP do pedido.
def coletar_codigo_erp(driver: webdriver.Chrome) -> str:

    """
    Resumo:
    - Coleta código ERP do pedido no site. Página do pedido deve estar aberta.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    
    Retorna:
    - código_erp (str)
    
    Exceções:
    - "Cliente sem código ERP.": Quando não há código ERP cadastrado no SAP, não aparece na página do pedido.
    """

    # ~~ Coleta razão social.
    código_erp = driver.find_element(By.XPATH, value="//label[@for='client_name_corporate']/following-sibling::div[@class='col-md-12']").text
    try:
        código_erp = str(código_erp).split(" (")[1]
        código_erp = str(código_erp).replace(")", "")
    except:
        raise Exception("Cliente sem código ERP.")

    # ~~ Retorna.
    return código_erp

# ================================================== #

# ~~ Coleta vendedor do pedido.
def coletar_vendedor(driver: webdriver.Chrome) -> str:

    """
    Resumo:
    - Coleta vendedor do pedido. Página do pedido deve estar aberta.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    
    Retorna:
    - vendedor (str)
    
    Exceções:
    - ===
    """
    
    # ~~ Coleta vendedor.
    cnpj = driver.find_element(By.XPATH, value="//label[@for='client_cnpj']/following-sibling::div[@class='col-md-12']").text 
    driver.get("https://www.revendedorpositivo.com.br/admin/clients")
    pesquisa = driver.find_element(By.ID, value="keyword") 
    pesquisa.clear()
    pesquisa.send_keys(cnpj)
    pesquisa.send_keys(Keys.ENTER)
    try:
        editar = driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
        editar = editar.get_attribute("href")
        driver.get(str(editar)) 
        time.sleep(2)
        carteira = driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[10].find_element(By.XPATH, value=".//a")
        carteira.click()
        carteira = driver.find_element(By.XPATH, value="(//select[@class='form-control select-multiple char_side2char_side-selected-options char_side2char_side-select-taller'])[1]")
        carteira = Select(carteira)
        carteira = carteira.options
        vendedor = carteira[0].text
    except:

        # ~~ Se não encontra vendedor 1105, tenta encontrar pelo 1101 nos ativos.
        try:
            driver.get("https://www.revendedorpositivo.com.br/admin/direct-billing-clients")
            pesquisa = driver.find_element(By.ID, value="keyword") 
            pesquisa.clear() 
            pesquisa.send_keys(cnpj) 
            ativo = driver.find_element(By.ID, value="active-1")
            ativo.click()
            pesquisa.send_keys(Keys.ENTER)
            editar = driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_element(By.XPATH, value="//td[contains(@data-title, 'Ações')]/a").get_attribute("href")
            driver.get(str(editar))
            cnpj = driver.find_element(By.ID, value="resale_cnpj").get_attribute("value")
            driver.get("https://www.revendedorpositivo.com.br/admin/clients")
            pesquisa = driver.find_element(By.ID, value="keyword")
            pesquisa.clear() 
            pesquisa.send_keys(cnpj) 
            pesquisa.send_keys(Keys.ENTER) 
            editar = driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
            editar = editar.get_attribute("href") 
            driver.get(str(editar)) 
            time.sleep(2)
            carteira = driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[10].find_element(By.XPATH, value=".//a") 
            carteira.click() 
            carteira = driver.find_element(By.XPATH, value="(//select[@class='form-control select-multiple char_side2char_side-selected-options char_side2char_side-select-taller'])[1]") 
            carteira = Select(carteira) 
            carteira = carteira.options 
            vendedor = carteira[0].text 
        
        # ~~ Se não encontrar 1101 ativos, procura nos inativos.
        except:
            driver.get("https://www.revendedorpositivo.com.br/admin/direct-billing-clients")
            pesquisa = driver.find_element(By.ID, value="keyword") 
            pesquisa.clear() 
            pesquisa.send_keys(cnpj) 
            inativo = driver.find_element(By.ID, value="active-0")
            inativo.click()
            pesquisa.send_keys(Keys.ENTER)
            editar = driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_element(By.XPATH, value="//td[contains(@data-title, 'Ações')]/a").get_attribute("href")
            driver.get(str(editar))
            cnpj = driver.find_element(By.ID, value="resale_cnpj").get_attribute("value")
            driver.get("https://www.revendedorpositivo.com.br/admin/clients")
            pesquisa = driver.find_element(By.ID, value="keyword")
            pesquisa.clear() 
            pesquisa.send_keys(cnpj) 
            pesquisa.send_keys(Keys.ENTER) 
            editar = driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
            editar = editar.get_attribute("href") 
            driver.get(str(editar)) 
            time.sleep(2)
            carteira = driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[10].find_element(By.XPATH, value=".//a") 
            carteira.click() 
            carteira = driver.find_element(By.XPATH, value="(//select[@class='form-control select-multiple char_side2char_side-selected-options char_side2char_side-select-taller'])[1]") 
            carteira = Select(carteira)
            carteira = carteira.options
            vendedor = carteira[0].text
    
    # ~~ Retorna.
    return vendedor

# ================================================== #

# ~~ Retorna escritório do vendedor.
def coletar_escritório(vendedor: str) -> int:

    """
    Resumo:
    - Retorna escritório do vendedor.

    Parâmetros:
    - vendedor (str)

    Retorna:
    - escritorio (int)

    Exceções:
    - "Vendedor {vendedor} não encontrado na lista."
    """

    # ~~ Cria DataFrame.
    df = pandas_tools.criar_df_planilha(diretorio_planilha=os.path.dirname(os.path.abspath(__file__)) + r"\comercial.xlsx", aba="COMERCIAL", linha_cabecalho=1, colunas_nomes=["NOME", "ESCRITÓRIO"])

    # ~~ Localiza vendedor.
    linha = df.index[df["NOME"] == str(vendedor)].tolist()

    # ~~ Coleta escritório.
    escritorio = df.iloc[linha]["ESCRITÓRIO"].values
    escritorio = int(escritorio)

    # ~~ Retorna escritório.
    return escritorio

# ================================================== #

# ~~ Coleta dados do pedido no site.
def coletar_dados_completos(driver: webdriver.Chrome, pedido: int) -> dict:

    """
    Resumo:
    - Coleta dados do pedido no site.
    
    Parâmetros:
    - driver (webdriver.Chrome)
    - pedido (int): Nº do pedido.
    
    Retorna:
    - dados_pedido (dict): Dicionário com os dados abaixo. 
        - ["pedido"]
        - ["data"]
        - ["condição_pagamento"]
        - ["razão_social"]
        - ["cnpj"]
        - ["código_erp"]
        - ["valor_pedido"]
        - ["status"]
        - ["vendedor"]
    
    Exceções:
    - "Pedido {pedido} não inserido no site ainda."
    """

    # ~~ Cria dicionário para os dados do pedido.
    dados_pedido = {}

    # ~~ Acessa página no site.
    acessar(driver=driver, pedido=pedido)

    # ~~ Coleta dados do pedido.
    dados_pedido["pedido"] = pedido
    dados_pedido["data"] = coletar_data(driver=driver)
    dados_pedido["forma_pagamento"] = coletar_forma_pagamento(driver=driver)
    dados_pedido["condição_pagamento"] = coletar_condição_pagamento(driver=driver)
    dados_pedido["razão_social"] = coletar_razao_social(driver=driver)
    dados_pedido["cnpj"] = coletar_cnpj(driver=driver)
    try:
        dados_pedido["código_erp"] = coletar_codigo_erp(driver=driver)
    except:
        dados_pedido["código_erp"] = "-"
    dados_pedido["valor_pedido"] = coletar_valor(driver=driver)
    dados_pedido["status"] = coletar_status(driver=driver)
    dados_pedido["vendedor"] = coletar_vendedor(driver=driver)

    # ~~ Retorna dados.
    return dados_pedido

# ================================================== #