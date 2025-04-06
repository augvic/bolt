# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Inicia setup Django.
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

# ================================================== #

# ~~ Bibliotecas.
import time
from scripts.navegador import Navegador
from scripts import sap
from scripts import utilitarios
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from app.models import Comercial, PedidosPendentes, DadosFinaceirosClientes
from django.shortcuts import get_object_or_404

# ================================================== #

# ~~ Classe Pedido.
class Pedido:

    """
    Resumo:
    - Coleta dados de pedido e realiza tarefas relacionas à ele.

    Atributos:
    - (navegador: Navegador): Instância do "Navegador".

    Métodos:
    - (armazenar_navegador): Cria atributo "navegador", armazenando instância da classe "Navegador".
    """

    # ~~ Atributos.
    navegador = None

    # ================================================== #

    # ~~ Armazena instância "Navegador."
    def armazenar_navegador(self, navegador: Navegador) -> None:

        """
        Resumo:
        - Armazena instância do "Navegador".

        Atributos:
        - (navegador: Navegador)
        """

        # ~~ Armazena instância.
        self.navegador = navegador

    # ================================================== #

    # ~~ Acessa pedido no site.
    def acessar(self, pedido: int) -> None:

        """
        Resumo:
        - Acessa a página do pedido no site.
        
        Parâmetros:
        - pedido (int)
        
        Retorna:
        - ===
        
        Exceções:
        - "Pedido {pedido} não inserido no site ainda."
        """

        # ~~ Acessa pedido.
        self.navegador.driver.get(f"https://www.revendedorpositivo.com.br/admin/orders/edit/id/{pedido}")

        # ~~ Coleta conteúdo da página.
        conteúdo_página = self.navegador.driver.find_element(By.TAG_NAME, value="body").text

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
        try:
            condição_pagamento = driver.find_element(By.XPATH, value="//label[@for='payment_slip_installments_description']/following-sibling::div[@class='col-md-12']").text
        except:
            condição_pagamento = driver.find_element(By.XPATH, value="//label[@for='payment_card_installments_description']/following-sibling::div[@class='col-md-12']").text

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
        - codigo_erp (str)
        
        Exceções:
        - "Cliente sem código ERP.": Quando não há código ERP cadastrado no SAP, não aparece na página do pedido.
        """

        # ~~ Coleta razão social.
        codigo_erp = driver.find_element(By.XPATH, value="//label[@for='client_name_corporate']/following-sibling::div[@class='col-md-12']").text
        try:
            codigo_erp = str(codigo_erp).split(" (")[1]
            codigo_erp = str(codigo_erp).replace(")", "")
        except:
            raise Exception("Cliente sem código ERP.")

        # ~~ Retorna.
        return codigo_erp

    # ================================================== #

    # ~~ Coleta vendedor do pedido.
    def coletar_vendedor(driver: webdriver.Chrome) -> str:

        """
        Resumo:
        - Coleta vendedor do pedido. Página do pedido deve estar aberta.
        
        Parâmetros:
        - (driver: webdriver.Chrome)
        
        Retorna:
        - (vendedor: str):
            - "{vendedor}"
            - "-"
        
        Exceções:
        - ===
        """
        
        # ~~ Valor padrão de vendedor.
        vendedor = "-"

        # ~~ Coleta vendedor.
        cnpj = driver.find_element(By.XPATH, value="//label[@for='client_cnpj']/following-sibling::div[@class='col-md-12']").text 
        driver.get("https://www.revendedorpositivo.com.br/admin/clients")
        pesquisa = driver.find_element(By.ID, value="keyword") 
        pesquisa.clear()
        pesquisa.send_keys(cnpj)
        pesquisa.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            editar = driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
            editar = editar.get_attribute("href")
            driver.get(str(editar)) 
            time.sleep(3)
            carteira = driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[10].find_element(By.XPATH, value=".//a")
            carteira.click()
            carteira = driver.find_element(By.XPATH, value="(//select[@class='form-control select-multiple side2side-selected-options side2side-select-taller'])[1]")
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
                time.sleep(3)
                editar = driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_element(By.XPATH, value="//td[contains(@data-title, 'Ações')]/a").get_attribute("href")
                driver.get(str(editar))
                cnpj = driver.find_element(By.ID, value="resale_cnpj").get_attribute("value")
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
                carteira = driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[10].find_element(By.XPATH, value=".//a") 
                carteira.click() 
                carteira = driver.find_element(By.XPATH, value="(//select[@class='form-control select-multiple side2side-selected-options side2side-select-taller'])[1]") 
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
                time.sleep(3)
                editar = driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_element(By.XPATH, value="//td[contains(@data-title, 'Ações')]/a").get_attribute("href")
                driver.get(str(editar))
                cnpj = driver.find_element(By.ID, value="resale_cnpj").get_attribute("value")
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
                carteira = driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[10].find_element(By.XPATH, value=".//a") 
                carteira.click() 
                carteira = driver.find_element(By.XPATH, value="(//select[@class='form-control select-multiple side2side-selected-options side2side-select-taller'])[1]") 
                carteira = Select(carteira)
                carteira = carteira.options
                vendedor = carteira[0].text
        
        # ~~ Retorna.
        return vendedor

    # ================================================== #

    # ~~ Retorna escritório do vendedor.
    def coletar_escritório(vendedor: str) -> str:

        """
        Resumo:
        - Retorna escritório do vendedor.

        Parâmetros:
        - (vendedor: str)

        Retorna:
        - (escritorio: str):
            - "{escritorio}"
            - "-"

        Exceções:
        - ===
        """

        # ~~ Coleta escritório do banco de dados.
        escritorio_query = Comercial.objects.filter(nome=vendedor).values_list("escritorio", flat=True)
        if not escritorio_query:
            escritorio = "-"
        else:
            for i in escritorio_query:
                escritorio = str(i)

        # ~~ Retorna escritório.
        return escritorio

    # ================================================== #

    # ~~ Coleta dados do pedido no site.
    def coletar_dados_completos(driver: webdriver.Chrome, pedido: int) -> dict:

        """
        Resumo:
        - Coleta dados do pedido no site.
        
        Parâmetros:
        - (driver: webdriver.Chrome)
        - (pedido: int)
        
        Retorna:
        - (dados_pedido: dict): 
            - (pedido: str)
            - (data: datetime)
            - (condição_pagamento: str)
            - (razão_social: str)
            - (cnpj: str)
            - (codigo_erp: str):
                - "{codigo_erp}"
                - "-"
            - (valor_pedido: float)
            - (status: str)
            - (vendedor: str):
                - "{vendedor}"
                - "-"
            - (escritorio: str):
                - "{escritorio}"
                - "-"
        
        Exceções:
        - ("Pedido {pedido} não inserido no site ainda.")
        """

        # ~~ Cria dicionário para os dados do pedido.
        dados_pedido = {}

        # ~~ Acessa página no site.
        acessar(driver=driver, pedido=pedido)

        # ~~ Coleta dados do pedido.
        dados_pedido["pedido"] = str(pedido)
        dados_pedido["data"] = coletar_data(driver=driver)
        dados_pedido["forma_pagamento"] = coletar_forma_pagamento(driver=driver)
        dados_pedido["condição_pagamento"] = coletar_condição_pagamento(driver=driver)
        dados_pedido["razão_social"] = coletar_razao_social(driver=driver)
        dados_pedido["cnpj"] = coletar_cnpj(driver=driver)
        dados_pedido["raiz_cnpj"] = dados_pedido["cnpj"][:8]
        try:
            dados_pedido["código_erp"] = coletar_codigo_erp(driver=driver)
        except:
            dados_pedido["código_erp"] = "-"
        dados_pedido["valor_pedido"] = coletar_valor(driver=driver)
        dados_pedido["status"] = coletar_status(driver=driver)
        dados_pedido["vendedor"] = coletar_vendedor(driver=driver)
        dados_pedido["escritorio"] = coletar_escritório(dados_pedido["vendedor"])

        # ~~ Retorna dados.
        return dados_pedido

    # ================================================== #

    # ~~ Faz análise de crédito do pedido.
    def analise_credito(dados_pedido: dict, printar_dados: bool = False, log_path: str = None) -> dict:

        """
        Resumo:
        - Faz análise de crédito do pedido.
        
        Parâmetros:
        - (dados_pedido: dict):
            - (raiz_cnpj: str)
            - (pedido: str)
            - (valor_pedido: float)
        - (printar_dados: bool): Padrão é False.
        - (log_path: str): Padrão é None.
        
        Retorna:
        - (resposta_analise: dict):
            - (mensagem: str)
            - (status: str):
                - "LIBERADO"
                - "NÃO LIBERADO"
        
        Exceções:
        - ("Não foi encontrado tela SAP disponível para conexão.")
        """

        # ~~ Cria dicionário para os dados da análise.
        resposta_análise = {}

        # ~~ Coleta dados financeiros do cliente.
        sessao_sap = sap.instanciar()
        dados_financeiros = sap.coletar_dados_financeiros_cliente(sap=sessao_sap, raiz_cnpj=dados_pedido["raiz_cnpj"], printar_dados=printar_dados, log_path=log_path)
        sap.ir_tela_inicial(sessao_sap)

        # ~~ Acessa database para verificar se há valores de pedidos pendentes.
        valores_pendentes = PedidosPendentes.objects.filter(raiz_cnpj=dados_pedido["raiz_cnpj"]).values_list("valor", flat=True)

        # ~~ Atualiza valor da margem de acordo com os valores pendentes.
        if dados_financeiros["margem"] != "Sem margem disponível.":
            if valores_pendentes:
                valores_pendentes_float = []
                for valor in valores_pendentes:
                    valores_pendentes_float.append(float(valor))
                valor_pendente_total = sum(valores_pendentes_float)
                margem = dados_financeiros["margem"] - valor_pendente_total
            else:
                margem = dados_financeiros["margem"]
        else:
            margem = "Sem margem disponível."

        # ~~ Verifica se vencimento é data ou não e converte ele caso seja.
        if dados_financeiros["vencimento"] == "Sem limite ativo.":
            vencimento = "Sem limite ativo."
        else:
            vencimento = datetime.strftime(dados_financeiros["vencimento"], "%d/%m/%Y")

        # ~~ Importa dados no database.
        cliente = DadosFinaceirosClientes.objects.filter(raiz_cnpj=dados_pedido["raiz_cnpj"]).first()
        if cliente:
            cliente.vencimento_limite = vencimento
            cliente.valor_limite = str(dados_financeiros["limite"])
            cliente.valor_em_aberto = str(dados_financeiros["em_aberto"])
            cliente.margem = str(margem)
            cliente.nfs_vencidas = str(dados_financeiros["nfs_vencidas"])
            cliente.save()
        else:
            novo_cliente = DadosFinaceirosClientes(
                raiz_cnpj=str(dados_pedido["raiz_cnpj"]),
                vencimento_limite=vencimento,
                valor_limite=str(dados_financeiros["limite"]),
                valor_em_aberto=str(dados_financeiros["em_aberto"]),
                margem=str(margem),
                nfs_vencidas=str(dados_financeiros["nfs_vencidas"])
            )
            novo_cliente.save()

        # ~~ Inicia análise definindo valores padrão.
        limite_ativo = True
        motivos = ""
        status = "LIBERADO"

        # ~~ Verifica se possui limite ativo.
        if dados_financeiros["limite"] == "Sem limite ativo." or dados_financeiros["vencimento"] == "Sem limite ativo.":
            motivos += "\n- Sem limite de crédito ativo."
            status = "NÃO LIBERADO"
            limite_ativo = False

        # ~~ Verifica vencimento do limite.
        elif dados_financeiros["vencimento"] < datetime.now().date():
            motivos += f"\n- Limite vencido em {datetime.strftime(dados_financeiros["vencimento"], "%d/%m/%Y")}."
            status = "NÃO LIBERADO"
            limite_ativo = False

        # ~~ Verifica se pedido está dentro da margem.
        if limite_ativo == True:
            if margem < dados_pedido["valor_pedido"]:
                motivos += f"\n- Valor do pedido excede a margem disponível. Valor do pedido: {f"R$ {dados_pedido["valor_pedido"]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")} / margem livre: {f"R$ {margem:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}."
                status = "NÃO LIBERADO"

        # ~~ Verifica se possui notas vencidas.
        if dados_financeiros["nfs_vencidas"] != "Sem vencidos.":
            motivos += f"\n- Possui vencidos: {dados_financeiros["nfs_vencidas"]}."
            status = "NÃO LIBERADO"

        # ~~ Verifica se pode ser liberado. Se puder, importa seu valor como pendente no database e atualiza margem do cliente.
        if status == "LIBERADO":
            resposta_análise["mensagem"] = f"Pedido {dados_pedido["pedido"]} liberado."
            resposta_análise["status"] = "LIBERADO"
            pedido_liberado = PedidosPendentes.objects.filter(pedido=dados_pedido["pedido"]).first()
            if not pedido_liberado:
                valor_pendente_novo = PedidosPendentes(
                    raiz_cnpj=dados_pedido["raiz_cnpj"],
                    pedido=dados_pedido["pedido"],
                    valor=dados_pedido["valor_pedido"]
                )
                valor_pendente_novo.save()
            margem_atualizada = margem - dados_pedido["valor_pedido"]
            cliente.margem = str(margem_atualizada)
            cliente.save()
        else:
            resposta_análise["mensagem"] = f"Pedido {dados_pedido["pedido"]} recusado:{motivos}"
            resposta_análise["status"] = "NÃO LIBERADO"

        # ~~ Printa dados.
        if printar_dados == True:
            utilitarios.printar_mensagem(mensagem=f"Valor do pedido: {f"R$ {dados_pedido["valor_pedido"]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}", char_type="=", char_qtd=50, char_side="bot", log_path=log_path)
            utilitarios.printar_mensagem(mensagem=resposta_análise["mensagem"], char_type="=", char_qtd=50, char_side="bot", log_path=log_path)

        # ~~ Retorna com dados de liberação.
        return resposta_análise

    # ================================================== #

    # ~~ Remove do database o valor de pedido pendente.
    def remover_pendente(numero_pedido: str, adicionar_ao_em_aberto: bool) -> dict:

        """
        Resumo:
        - Remove do database o valor de pedido pendente.
        
        Parâmetros:
        - (pedido: str):
        
        Retorna:
        - ===
        
        Exceções:
        - ===
        """

        # ~~ Coleta pedido pendente.
        pedido = get_object_or_404(PedidosPendentes, pedido=numero_pedido)

        # ~~ Coleta cliente.
        cliente = get_object_or_404(DadosFinaceirosClientes, raiz_cnpj=pedido.raiz_cnpj)

        # ~~ Coleta valores.
        margem = float(cliente.margem)
        valor_pedido = float(pedido.valor)
        if cliente.valor_em_aberto != "Sem valores em aberto.":
            em_aberto = float(cliente.valor_em_aberto)
        else:
            em_aberto = 0

        # ~~ Se for para adicionar o valor ao "em aberto".
        if adicionar_ao_em_aberto == True:
            cliente.valor_em_aberto = em_aberto + valor_pedido
        else:
            cliente.margem = margem + valor_pedido
        cliente.save()

        # ~~ Deleta pedido.
        pedido.delete()

    # ================================================== #

# ================================================== #