# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# ================================================== #

# ~~ Bibliotecas.
import time
from scripts.instancias.navegador import Navegador
from scripts.controladores.financeiro import Financeiro
from scripts.auxiliar.utilitarios import Utilitarios
from scripts.controladores.erros.pedido_erros import *
from scripts.auxiliar.database import Database
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# ================================================== #

# ~~ Classe Pedido.
class Pedido:

    """
    Resumo:
    - Coleta dados de pedido e realiza tarefas relacionas à ele.

    Atributos:
    - (navegador: Navegador): Instância do "Navegador".
    - (financeiro: Financeiro): Instância da classe "Financeiro".
    - (utilitarios: Utilitarios): Instância da classe "Utilitarios".
    - (database: Database): Instância da classe "Database".
    - (pedido: str)
    - (data: str)
    - (forma_pagamento: str) 
    - (condicao_pagamento: str)
    - (cliente: str)
    - (revenda: str)
    - (cnpj_cpf: str)
    - (raiz_cnpj: str)
    - (codigo_erp: str)
    - (valor_pedido: str)
    - (status: str)
    - (vendedor: str)
    - (escritorio: str)
    - (observacao: str)
    - (centros: str)
    - (analise_credito_mensagem: str)
    - (analise_credito_status):
        - ("LIBERADO": str)
        - ("NÃO LIBERADO": str)
    - (ordem: str)
    - (over: str)
    - (porcentagem_comissao: str)

    Métodos:
    - (__init__): Cria atributos.
    - (acessar): Acessa a página do pedido no site.
    - (coletar_data): Coleta a data do pedido no site.
    - (coletar_condicao_pagamento): Coleta a condição de pagamento do pedido no site.
    - (coletar_forma_pagamento): Coleta a forma de pagamento do pedido no site.
    - (coletar_cnpj): Coleta o CNPJ do cliente no site.
    - (coletar_valor): Coleta o valor do pedido no site.
    - (coletar_status): Coleta o status do pedido no site.
    - (coletar_cliente): Coleta a razão social do pedido no site.
    - (coletar_codigo_erp): Coleta código ERP do pedido no site.
    - (coletar_vendedor): Coleta vendedor do pedido.
    - (coletar_escritório): Retorna escritório do vendedor.
    - (coletar_dados_completos): Coleta dados do pedido no site.
    """

    # ================================================== #

    # ~~ Armazena instância "Navegador".
    def __init__(self, navegador: Navegador, financeiro: Financeiro, utilitarios: Utilitarios, database: Database) -> None:

        """
        Resumo:
        - Cria atributos.

        Parâmetros:
        - (navegador: Navegador): Instância da classe "Navegador".
        - (financeiro: Financeiro): Instância da classe "Financeiro".
        - (utilitarios: Utilitarios): Instância da classe "Utilitarios".
        - (database: Database): Instância da classe "Database".

        Atributos:
        - (navegador: Navegador): Instância da classe "Navegador".
        - (financeiro: Financeiro): Instância da classe "Financeiro".
        - (utilitarios: Utilitarios): Instância da classe "Utilitarios".
        - (database: Database): Instância da classe "Database".
        - Atributos para cada dado do pedido.
        """

        # ~~ Armazena instância.
        self.navegador = navegador
        self.financeiro = financeiro
        self.utilitarios = utilitarios
        self.database = database

        # ~~ Cria restante como None.
        self.pedido = None
        self.data = None
        self.forma_pagamento = None
        self.condicao_pagamento = None
        self.cliente = None
        self.revenda = None
        self.cnpj_cpf = None
        self.raiz_cnpj = None
        self.codigo_erp = None
        self.valor_total = None
        self.status = None
        self.vendedor = None
        self.escritorio = None
        self.observacao = None
        self.centros = None
        self.analise_credito_mensagem = None
        self.analise_credito_status = None
        self.ordem = None
        self.over = None
        self.porcentagem_comissao = None

        # ~~ Status de dados coletados.
        self.dados_coletados = False

    # ================================================== #

    # ~~ Acessa pedido no site.
    def acessar(self, pedido: int) -> None:

        """
        Resumo:
        - Acessa a página do pedido no site.
        
        Parâmetros:
        - (pedido: int)

        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Acessa pedido.
        self.navegador.driver.get(f"https://www.revendedorpositivo.com.br/admin/orders/edit/id/{pedido}")

        # ~~ Coleta conteúdo da página.
        conteúdo_página = self.navegador.driver.find_element(By.TAG_NAME, value="body").text

        # ~~ Se pedido não foi inputado ainda, retorna erro.
        if "Application error: Mysqli statement execute error" in conteúdo_página:
            raise PedidoNaoInseridoError(pedido)

    # ================================================== #

    # ~~ Coleta data do pedido.
    def coletar_data(self, pedido: int) -> str:

        """
        Resumo:
        - Coleta a data do pedido no site.

        Parâmetros:
        - (pedido: int)

        Retorna:
        - (data: str)

        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar caso página não esteja aberta.
        try:

            # ~~ Coleta data.
            data = self.navegador.driver.find_element(By.XPATH, value="//label[@for='order_date']/following-sibling::div[@class='col-md-12']").text
        
        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            data = self.coletar_data(pedido)

        # ~~ Retorna a data.
        return data

    # ================================================== #

    # ~~ Coleta condição de pagamento do pedido.
    def coletar_condicao_pagamento(self, pedido) -> str:

        """
        Resumo:
        - Coleta a condição de pagamento do pedido no site.
        
        Parâmetros:
        - (pedido: int)
        
        Retorna:
        - (condicao_pagamento: str)
        
        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Captura caso página não esteja aberta.
        try:

            # ~~ Coleta condição de pagamento.
            try:
                condicao_pagamento = self.navegador.driver.find_element(By.XPATH, value="//label[@for='payment_slip_installments_description']/following-sibling::div[@class='col-md-12']").text
            except:
                condicao_pagamento = self.navegador.driver.find_element(By.XPATH, value="//label[@for='payment_card_installments_description']/following-sibling::div[@class='col-md-12']").text

        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            condicao_pagamento = self.coletar_condicao_pagamento(pedido)

        # ~~ Retorna a condição de pagamento.
        return condicao_pagamento

    # ================================================== #

    # ~~ Coleta forma de pagamento do pedido.
    def coletar_forma_pagamento(self, pedido) -> str:

        """
        Resumo:
        - Coleta a forma de pagamento do pedido no site.
        
        Parâmetros:
        - (pedido: int)
        
        Retorna:
        - (forma_pagamento: str)
        
        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar se página não está aberta.
        try:

            # ~~ Coleta forma de pagamento.
            forma_pagamento = self.navegador.driver.find_element(By.XPATH, value="//label[@for='payment_name']/following-sibling::div[@class='col-md-12']").text
            lista_pagamentos_hífen = ["Boleto à Vista - Log - Imprimir", "Elo - Log", "Visa - Log", "Master - Log", "Pix - Log"]
            if forma_pagamento in lista_pagamentos_hífen:
                forma_pagamento = forma_pagamento.split(" - ")[0]

        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            forma_pagamento = self.coletar_forma_pagamento(pedido)

        # ~~ Retorna forma de pagamento.
        return forma_pagamento

    # ================================================== #

    # ~~ Coleta CNPJ do cliente.
    def coletar_cnpj(self, pedido: int) -> str:

        """
        Resumo:
        - Coleta o CNPJ do cliente no site.
        
        Parâmetros:
        - (pedido: int)
        
        Retorna:
        - (cnpj: str)
        
        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar caso página não esteja aberta.
        try:

            # ~~ Coleta CNPJ.
            cnpj = self.navegador.driver.find_element(By.XPATH, value="//label[@for='client_cnpj']/following-sibling::div[@class='col-md-12']").text

        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            cnpj = self.coletar_cnpj(pedido)

        # ~~ Retorna CNPJ.
        return cnpj

    # ================================================== #

    # ~~ Coleta valor do pedido.
    def coletar_valor(self, pedido: int) -> str:

        """
        Resumo:
        - Coleta o valor do pedido no site.
        
        Parâmetros:
        - (pedido: int)
        
        Retorna:
        - (valor_pedido: str)
        
        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar caso página não esteja aberta.
        try:

            # ~~ Coleta valor do pedido.
            valor_pedido = self.navegador.driver.find_element(By.XPATH, value="//label[@for='payment_value']/following-sibling::div[@class='col-md-12']").text 
            valor_pedido = valor_pedido.replace("R$", "").replace(".", "").replace(",", ".")

        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            valor_pedido = self.coletar_valor(pedido)

        # ~~ Retorna valor do pedido.
        return valor_pedido

    # ================================================== #

    # ~~ Coleta status do pedido.
    def coletar_status(self, pedido) -> str:

        """
        Resumo:
        - Coleta o status do pedido no site.
        
        Parâmetros:
        - (pedido: int)
        
        Retorna:
        - (status_pedido):
            - ("CANCELADO": str)
            - OU ("FATURADO": str)
            - OU ("RECUSADO": str)
            - OU ("LIBERADO": str)
            - OU ("RECEBIDO": str)
        
        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar caso página não esteja aberta.
        try:

            # ~~ Coleta status do pedido.
            try: 
                status_pedido = self.navegador.driver.find_element(By.NAME, value="distribution_centers[1][status]")
            except: 
                try:
                    status_pedido = self.navegador.driver.find_element(By.NAME, value="distribution_centers[2][status]")
                except:
                    status_pedido = self.navegador.driver.find_element(By.NAME, value="distribution_centers[3][status]") 
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

        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            status = self.coletar_status(pedido)

        # ~~ Retorna status.
        return status_pedido

    # ================================================== #

    # ~~ Coleta razão social do pedido.
    def coletar_cliente(self, pedido: int) -> str:

        """
        Resumo:
        - Coleta a razão social do pedido no site.
        
        Parâmetros:
        - (pedido: int)
        
        Retorna:
        - (razao_social: str)
        
        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar caso página não esteja aberta.
        try:

            # ~~ Coleta razão social.
            razao_social = self.navegador.driver.find_element(By.XPATH, value="//label[@for='client_name_corporate']/following-sibling::div[@class='col-md-12']").text
            try:
                razao_social = str(razao_social).split(" (")[0]
            except:
                pass

        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            razao_social = self.coletar_cliente(pedido)

        # ~~ Retorna.
        return razao_social

    # ================================================== #

    # ~~ Coleta revenda do pedido.
    def coletar_revenda(self, pedido: int) -> str:

        """
        Resumo:
        - Coleta a revenda do pedido no site.
        
        Parâmetros:
        - (pedido: int)
        
        Retorna:
        - (revenda)
            - (revenda: str)
            - OU ("-": str)
        
        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar caso página não esteja aberta.
        try:

            # ~~ Coleta revenda.
            try:
                revenda = self.navegador.driver.find_element(By.XPATH, value="//label[@for='resale_name_corporate']/following-sibling::div[@class='col-md-12']").text
            except:
                revenda = "-"
                return revenda
            try:
                revenda = str(revenda).split(" (")[0]
            except:
                pass

        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            revenda = self.coletar_revenda(pedido)

        # ~~ Retorna.
        return revenda

    # ================================================== #

    # ~~ Coleta código ERP do pedido.
    def coletar_codigo_erp(self, pedido: int) -> str:

        """
        Resumo:
        - Coleta código ERP do pedido no site.
        
        Parâmetros:
        - (pedido: int)
        
        Retorna:
        - (codigo_erp):
            - (codigo_erp: str)
            - OU ("-": str)
        
        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar caso página não esteja aberta.
        try:

            # ~~ Coleta razão social.
            codigo_erp = self.navegador.driver.find_element(By.XPATH, value="//label[@for='client_name_corporate']/following-sibling::div[@class='col-md-12']").text
            try:
                codigo_erp = str(codigo_erp).split(" (")[1]
                codigo_erp = str(codigo_erp).replace(")", "")
            except:
                codigo_erp = "-"
            
        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            codigo_erp = self.coletar_codigo_erp(pedido)

        # ~~ Retorna.
        return codigo_erp

    # ================================================== #

    # ~~ Coleta vendedor do pedido.
    def coletar_vendedor(self, pedido: int) -> str:

        """
        Resumo:
        - Coleta vendedor do pedido.
        
        Parâmetros:
        - (pedido: int)
        
        Retorna:
        - (vendedor):
            - (vendedor: str)
            - OU ("-": str)
        
        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar caso página não esteja aberta.
        try:

            # ~~ Valor padrão de vendedor.
            vendedor = "-"

            # ~~ Coleta vendedor.
            cnpj = self.navegador.driver.find_element(By.XPATH, value="//label[@for='client_cnpj']/following-sibling::div[@class='col-md-12']").text 
            self.navegador.driver.get("https://www.revendedorpositivo.com.br/admin/clients")
            pesquisa = self.navegador.driver.find_element(By.ID, value="keyword") 
            pesquisa.clear()
            pesquisa.send_keys(cnpj)
            pesquisa.send_keys(Keys.ENTER)
            time.sleep(3)
            try:
                editar = self.navegador.driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
                editar = editar.get_attribute("href")
                self.navegador.driver.get(str(editar)) 
                time.sleep(3)
                carteira = self.navegador.driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[10].find_element(By.XPATH, value=".//a")
                carteira.click()
                carteira = self.navegador.driver.find_element(By.XPATH, value="(//select[@class='form-control select-multiple side2side-selected-options side2side-select-taller'])[1]")
                carteira = Select(carteira)
                carteira = carteira.options
                vendedor = carteira[0].text
            except:

                # ~~ Se não encontra vendedor 1105, tenta encontrar pelo 1101 nos ativos.
                try:
                    self.navegador.driver.get("https://www.revendedorpositivo.com.br/admin/direct-billing-clients")
                    pesquisa = self.navegador.driver.find_element(By.ID, value="keyword") 
                    pesquisa.clear() 
                    pesquisa.send_keys(cnpj) 
                    ativo = self.navegador.driver.find_element(By.ID, value="active-1")
                    ativo.click()
                    pesquisa.send_keys(Keys.ENTER)
                    time.sleep(3)
                    editar = self.navegador.driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_element(By.XPATH, value="//td[contains(@data-title, 'Ações')]/a").get_attribute("href")
                    self.navegador.driver.get(str(editar))
                    cnpj = self.navegador.driver.find_element(By.ID, value="resale_cnpj").get_attribute("value")
                    self.navegador.driver.get("https://www.revendedorpositivo.com.br/admin/clients")
                    pesquisa = self.navegador.driver.find_element(By.ID, value="keyword")
                    pesquisa.clear() 
                    pesquisa.send_keys(cnpj) 
                    pesquisa.send_keys(Keys.ENTER)
                    time.sleep(3)
                    editar = self.navegador.driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
                    editar = editar.get_attribute("href") 
                    self.navegador.driver.get(str(editar)) 
                    time.sleep(3)
                    carteira = self.navegador.driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[10].find_element(By.XPATH, value=".//a") 
                    carteira.click() 
                    carteira = self.navegador.driver.find_element(By.XPATH, value="(//select[@class='form-control select-multiple side2side-selected-options side2side-select-taller'])[1]") 
                    carteira = Select(carteira) 
                    carteira = carteira.options 
                    vendedor = carteira[0].text 
                
                # ~~ Se não encontrar 1101 ativos, procura nos inativos.
                except:
                    self.navegador.driver.get("https://www.revendedorpositivo.com.br/admin/direct-billing-clients")
                    pesquisa = self.navegador.driver.find_element(By.ID, value="keyword") 
                    pesquisa.clear() 
                    pesquisa.send_keys(cnpj) 
                    inativo = self.navegador.driver.find_element(By.ID, value="active-0")
                    inativo.click()
                    pesquisa.send_keys(Keys.ENTER)
                    time.sleep(3)
                    editar = self.navegador.driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_element(By.XPATH, value="//td[contains(@data-title, 'Ações')]/a").get_attribute("href")
                    self.navegador.driver.get(str(editar))
                    cnpj = self.navegador.driver.find_element(By.ID, value="resale_cnpj").get_attribute("value")
                    self.navegador.driver.get("https://www.revendedorpositivo.com.br/admin/clients")
                    pesquisa = self.navegador.driver.find_element(By.ID, value="keyword")
                    pesquisa.clear() 
                    pesquisa.send_keys(cnpj) 
                    pesquisa.send_keys(Keys.ENTER)
                    time.sleep(3)
                    editar = self.navegador.driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
                    editar = editar.get_attribute("href") 
                    self.navegador.driver.get(str(editar)) 
                    time.sleep(3)
                    carteira = self.navegador.driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[10].find_element(By.XPATH, value=".//a") 
                    carteira.click() 
                    carteira = self.navegador.driver.find_element(By.XPATH, value="(//select[@class='form-control select-multiple side2side-selected-options side2side-select-taller'])[1]") 
                    carteira = Select(carteira)
                    carteira = carteira.options
                    vendedor = carteira[0].text
        
        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            vendedor = self.coletar_vendedor(pedido)
        
        # ~~ Retorna.
        return vendedor

    # ================================================== #

    # ~~ Retorna escritório do vendedor.
    def coletar_escritório(self, vendedor: str) -> str:

        """
        Resumo:
        - Retorna escritório do vendedor.

        Parâmetros:
        - (vendedor: str)

        Retorna:
        - (escritorio):
            - (escritorio: str)
            - OU ("-": str)
        """

        # ~~ Coleta escritório do banco de dados.
        escritorio_query = self.database.coletar_escritorio(vendedor)
        if not escritorio_query:
            escritorio = "-"
        else:
            for i in escritorio_query:
                escritorio = str(i)

        # ~~ Retorna escritório.
        return escritorio

    # ================================================== #

    # ~~ Coleta centro(s) do pedido.
    def coletar_centros(self, pedido: int) -> str:

        """
        Resumo:
        - Coleta centros do pedido no site.

        Parametros:
        - (pedido: int)
        
        Retorna:
        - (centros: str)

        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar caso página não esteja aberta.
        try:

            # ~~ Coleta centro.
            centro_1 = self.navegador.driver.find_element(By.XPATH, value="(//div[@class='panel distribution-center']/div[@class='panel-heading'])[1]").text 
            try:
                centro_2 = self.navegador.driver.find_element(By.XPATH, value="(//div[@class='panel distribution-center']/div[@class='panel-heading'])[2]").text
                centro = centro_1 + " - " + centro_2
            except:
                centro = centro_1
        
        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            centro = self.coletar_centros(pedido)

        # ~~ Retorna.
        return centro

    # ================================================== #

    # ~~ Coleta observação do pedido.
    def coletar_observacao(self, pedido) -> str:

        """
        Resumo:
        - Coleta a observação do pedido no site.

        Parâmetros:
        - (pedido: int)

        Retorna:
        - (observacao_pedido)
            - (observacao_pedido: str)
            - OU ("-": str)

        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar caso página não esteja aberta.
        try:

            # ~~ Coleta observação.
            observacao_pedido = self.navegador.driver.find_element(By.XPATH, value="//label[@for='client_comment']/following-sibling::div[@class='col-md-12']").text 
            if observacao_pedido == "":
                observacao_pedido = "-"
        
        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            observacao_pedido = self.coletar_observacao(pedido)
        
        # ~~ Retorna.
        return observacao_pedido

    # ================================================== #

    # ~~ Coleta ordem do pedido.
    def coletar_ordem(self, pedido: int) -> int:

        """
        Resumo:
        - Coleta a ordem do pedido no site.

        Parâmetros:
        - (pedido: int)

        Retorna:
        - (ordem)
            - (ordem: str)
            - OU ("-": str)

        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar caso página não esteja aberta.
        try:

            # ~~ Coleta ordem.
            try:
                ordem = self.navegador.driver.find_element(By.ID, value="distribution_centers-3-external_id")
            except:
                try:
                    ordem = self.navegador.driver.find_element(By.ID, value="distribution_centers-2-external_id")
                except:
                    ordem = self.navegador.driver.find_element(By.ID, value="distribution_centers-1-external_id")
            ordem = ordem.get_attribute("value")
            if ordem == "":
                ordem = "-"

        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            ordem = self.coletar_ordem(pedido)

        # ~~ Retorna.
        return ordem

    # ================================================== #

    # ~~ Coleta comissão over do pedido.
    def coletar_over(self, pedido: int) -> str:

        """
        Resumo:
        - Coleta o over do pedido no site.

        Parâmetros:
        - (pedido: int)

        Retorna:
        - (comissao_over):
            - ("SIM": str)
            - ("NÃO": str)

        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Para capturar caso página não esteja aberta.
        try:

            # ~~ Coleta comissão over.
            comissao_over = self.navegador.driver.find_element(By.XPATH, value="//div[@class='panel distribution-center']").text 
            if "Comissão total (comissão unitários)" in comissao_over:
                comissao_over = "SIM"
            else: 
                comissao_over = "NÃO"

        # ~~ Usa recursão.
        except:
            self.acessar(pedido)
            comissao_over = self.coletar_over(pedido)

        # ~~ Retorna.
        return comissao_over

    # ================================================== #

    # ~~ Retorna porcentagem Z6.
    def coletar_porcentagem_comissao(self, escritorio: str) -> str:

        """
        Resumo:
        - Retorna porcentagem de comissão.

        Parâmetros:
        - (escritorio: str)

        Retorna:
        - (porcentagem):
            - ("0,50": str)
            - ("2,50": str)

        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Retorna porcentagem com base no escritorio.
        if escritorio == "1105":
            return "0,50"
        else:
            return "2,50"

    # ================================================== #

    # ~~ Coleta dados do pedido no site.
    def coletar_dados_completos(self, pedido: int) -> None:

        """
        Resumo:
        - Coleta dados do pedido no site e importa no database.
        
        Parâmetros:
        - (pedido: int)
        
        Atributos:
        - (pedido: str)
        - (data: str)
        - (forma_pagamento: str)
        - (condicao_pagamento: str)
        - (cliente: str)
        - (revenda: str)
        - (razao_social: str)
        - (cnpj: str)
        - (raiz_cnpj: str)
        - (codigo_erp):
            - (codigo_erp: str)
            - OU ("-": str)
        - (valor_pedido: str)
        - (status: str)
        - (vendedor):
            - (vendedor: str)
            - OU ("-": str)
        - (escritorio):
            - (escritorio: str)
            - OU ("-": str)
        - (centros: str)
        - (observacao: str)
        - (ordem: str)
        - (over: str)
        - (porcentagem_comissao: str)
        
        Exceções:
        - (PedidoNaoInseridoError): Quando pedido não foi inserido no site ainda.
        """

        # ~~ Acessa página no site.
        self.acessar(pedido)

        # ~~ Coleta dados do pedido.
        self.pedido = str(pedido)
        self.data = self.coletar_data(pedido)
        self.forma_pagamento = self.coletar_forma_pagamento(pedido)
        self.condicao_pagamento = self.coletar_condicao_pagamento(pedido)
        self.cliente = self.coletar_cliente(pedido)
        self.revenda = self.coletar_revenda(pedido)
        self.cnpj_cpf = self.coletar_cnpj(pedido)
        self.raiz_cnpj = self.cnpj_cpf[:8]
        self.codigo_erp = self.coletar_codigo_erp(pedido)
        self.valor_total = self.coletar_valor(pedido)
        self.status = self.coletar_status(pedido)
        self.centros = self.coletar_centros(pedido)
        self.observacao = self.coletar_observacao(pedido)
        self.ordem = self.coletar_ordem(pedido)
        self.over = self.coletar_over(pedido)
        self.vendedor = self.coletar_vendedor(pedido)
        self.escritorio = self.coletar_escritório(self.vendedor)
        self.porcentagem_comissao = self.coletar_porcentagem_comissao(self.escritorio)

        # ~~ Altera status para True.
        self.dados_coletados = True

        # ~~ Importa dados no database.
        self.database.importar_pedido_database(
            self.pedido, self.status, self.data, self.forma_pagamento, self.condicao_pagamento,
            self.vendedor, self.escritorio, self.revenda, self.cliente, self.cnpj_cpf,
            self.codigo_erp, self.over, self.porcentagem_comissao, self.valor_total, self.observacao,
            self.centros, self.ordem
        )

    # ================================================== #

    # ~~ Faz análise de crédito do pedido.
    def analise_credito(self, printar_dados: bool = False, log_path: str = None, liberar_tela: bool = False) -> None:

        """
        Resumo:
        - Faz análise de crédito do pedido.
        
        Parâmetros:
        - (printar_dados): 
            - (False: bool): Padrão.
            - OU (True: bool): Printa dados.
        - (log_path: str): Caso passado um diretório, transfere texto printado para um arquivo ".txt". O parâmetro "printar_dados" deve ser True.
        - (liberar_tela):
            - (False: bool): Padrão. 
            - (True: bool): Libera tela do SAP.

        Atributos:
        - (analise_credito_mensagem: str)
        - (analise_credito_status):
            - ("LIBERADO": str)
            - ("NÃO LIBERADO": str)

        Exceções:
        - (PedidoDadosNaoColetadosError): Quando dados do pedido não foram coletados para analisar.
        """

        # ~~ Verifica se há dados coletados.
        if self.dados_coletados == False:
            raise PedidoDadosNaoColetadosError()

        # ~~ Coleta dados financeiros do cliente.
        dados_financeiros = self.financeiro.coletar_dados_financeiros_cliente(raiz_cnpj=self.raiz_cnpj, printar_dados=printar_dados, log_path=log_path, liberar_tela=liberar_tela)

        # ~~ Acessa database para verificar se há valores de pedidos pendentes.
        valores_pendentes = self.database.coletar_pedidos_pendentes(self.raiz_cnpj)

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
            vencimento_str = "Sem limite ativo."
        else:
            vencimento_str = datetime.strftime(dados_financeiros["vencimento"], "%d/%m/%Y")

        # ~~ Importa dados no database.
        self.database.importar_dados_financeiros_cliente(str(self.raiz_cnpj), str(vencimento_str), str(dados_financeiros["limite"]), str(dados_financeiros["em_aberto"]), str(margem), str(dados_financeiros["nfs_vencidas"]))

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
            if margem < float(self.valor_total):
                motivos += f"\n- Valor do pedido excede a margem disponível. Valor do pedido: {f"R$ {float(self.valor_total):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")} / Margem livre: {f"R$ {margem:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}."
                status = "NÃO LIBERADO"

        # ~~ Verifica se possui notas vencidas.
        if dados_financeiros["nfs_vencidas"] != "Sem vencidos.":
            motivos += f"\n- Possui vencidos: {dados_financeiros["nfs_vencidas"]}."
            status = "NÃO LIBERADO"

        # ~~ Verifica se pode ser liberado. Se puder, importa seu valor como pendente no database e atualiza margem do cliente.
        if status == "LIBERADO":

            # ~~ Salva retorno.
            self.analise_credito_mensagem = f"Pedido {self.pedido} liberado."
            self.analise_credito_status = "LIBERADO"

            # ~~ Importa pedido pendente.
            self.database.importar_pedido_pendente(self.raiz_cnpj, self.pedido, self.valor_total)

            # ~~ Atualiza margem do cliente.
            margem_atualizada = margem - float(self.valor_total)
            self.database.importar_dados_financeiros_cliente(raiz_cnpj=self.raiz_cnpj, margem=margem_atualizada)
        
        # ~~ Se não for liberado.
        else:
            self.analise_credito_mensagem = f"Pedido {self.pedido} recusado:{motivos}"
            self.analise_credito_status = "NÃO LIBERADO"

        # ~~ Printa dados.
        if printar_dados == True:
            self.utilitarios.printar_mensagem(mensagem=f"Valor do pedido: {f"R$ {float(self.valor_total):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}", char_type="=", char_qtd=50, char_side="bot", log_path=log_path)
            self.utilitarios.printar_mensagem(mensagem=self.analise_credito_mensagem, char_type="=", char_qtd=50, char_side="bot", log_path=log_path)

    # ================================================== #

# ================================================== #

from scripts.instancias.sap import Sap
sap = Sap()
database = Database()
utilitarios = Utilitarios()
navegador = Navegador(utilitarios)
financeiro = Financeiro(sap, utilitarios)
pedido = Pedido(navegador, financeiro, utilitarios, database)

navegador.acessar_godeep()
pedido.coletar_dados_completos(13583)
pedido.analise_credito(True, None, True)