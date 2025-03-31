# ================================================== #

# ~~ Encerramento do RPA.
def encerrar_rpa(self) -> None:

    """
    Resumo:
    * Encerra RPA.
    
    Parâmetros:
    * ===
    
    Retorna:
    * ===
    
    Erros:
    * ===
    
    Erros tratados localmente:
    * ===
    
    Erros levantados:
    * ===
    """

    # ~~ Encerra instância Driver.
    self.driver.quit()

    # ~~ Encerra instância SAP.
    while True:
        if self.session.ActiveWindow.Text == "SAP Easy Access":
            break
        else:
            self.session.findById("wnd[0]").sendVKey(3)
    self.session = None
    
    # ~~ Salva controle.
    self.salvar_controle()

    # ~~ Encerra execução do RPA.
    self.printar_mensagens("Encerrando execução do RPA...", "=", 30, "bot")
    self.exportar_log()
    exit()

# ================================================== #

# ~~ Cria instância do navegador, utilizando o webdriver.
def instanciar_navegador(self) -> webdriver:

    """
    Resumo:
    * Cria instância do navegador, utilizando o webdriver.
    
    Parâmetros:
    * ===
    
    Retorna:
    * Driver -> Navegador instanciado.
    
    Erros:
    * ===
    
    Erros tratados localmente:
    * ===
    
    Erros levantados:
    * ===
    """

    # ~~ Path do Profile.
    caminho_script = os.path.abspath(__file__)
    caminho_perfil = caminho_script.split(r"script_faturamento.py")[0] + r"\profile"

    # ~~ Definindo configurações.
    options = opt()
    options.add_argument(f"user-data-dir={caminho_perfil}")
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

    # ~~ Acessando site e fazendo login.
    driver.get(f"https://www.revendedorpositivo.com.br/admin/")
    login_microsoft_button = None
    try:
        login_microsoft_button = driver.find_element(By.ID, value="login-ms-azure-ad") 
        login_microsoft_button.click()
        time.sleep(5)
        body = driver.find_element(By.TAG_NAME, value="body").text
        if "Because you're accessing sensitive info, you need to verify your password." in body:
            self.printar_mensagens("*** Necessário logar conta Microsoft. ***", "=", 30, "bot")
            time.sleep(60)
        if "Approve sign in request" in body:
            time.sleep(2)
            código = driver.find_element(By.ID, value="idRichContext_DisplaySign").text
            self.printar_mensagens(f"*** Necessário authenticator Microsoft para continuar: {código} ***", "=", 30, "bot")
            time.sleep(60)
    except:
        driver.get(f"https://www.revendedorpositivo.com.br/admin/index/")

    # ~~ Retorna instância do webdriver.
    return driver

# ================================================== #

# ~~ Acessa pedido.
def acessar_pedido(self, pedido: int) -> None:

    """
    Resumo:
    * Acessa a página do pedido no site.
    
    Parâmetros:
    * pedido -> Número do pedido.
    
    Retorna:
    * ===
    
    Erros:
    * ===
    
    Erros tratados localmente:
    * ===
    
    Erros levantados:
    * ===
    """

    # ~~ Acessa pedido.
    self.driver.get(f"https://www.revendedorpositivo.com.br/admin/orders/edit/id/{pedido}")

# ================================================== #

# ~~ Coleta data do pedido.
def coletar_data_site(self) -> datetime:

    """
    Resumo:
    * Coleta data do pedido.
    
    Parâmetros:
    * ===
    
    Retorna:
    * data -> Data de inputação do pedido como objeto datetime.
    
    Erros:
    * ===
    
    Erros tratados localmente:
    * ===
    
    Erros levantados:
    * ===
    """

    # ~~ Coleta data.
    data = self.driver.find_element(By.XPATH, value = "//label[@for='order_date']/following-sibling::div[@class='col-md-12']").text
    data = data[:10]
    data = datetime.strptime(data, "%d/%m/%Y").date()
    data = datetime.strftime(data, "%d/%m/%Y")

    # ~~ Retorna.
    return data

# ================================================== #

# ~~ Coleta forma de pagamento do pedido.
def ColetarFormaPagamentoSite(self) -> str:

    """
    Resumo:
    * Coleta a forma de pagamento do pedido no site.
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * FormaPagamento -> Forma de pagamento.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Coleta forma de pagamento.
    FormaPagamento = self.Driver.find_element(By.XPATH, value="//label[@for='payment_name']/following-sibling::div[@class='col-md-12']").text
    ListaPags = ["Boleto à Vista - Log - Imprimir", "Elo - Log", "Visa - Log", "Master - Log", "Pix - Log"]
    if FormaPagamento in ListaPags:
        FormaPagamento = FormaPagamento.split(" - ")[0]

    # ~~ Retorna.
    return FormaPagamento

# ================================================== #

# ~~ Coleta vendedor do pedido.
def ColetarVendedorSite(self) -> str:

    """
    Resumo:
    * Coleta o vendedor do pedido no site.
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * Vendedor -> Nome do vendedor.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """
    
    # ~~ Coleta vendedor.
    Cnpj = self.Driver.find_element(By.XPATH, value="//label[@for='client_cnpj']/following-sibling::div[@class='col-md-12']").text 
    self.Driver.get("https://www.revendedorpositivo.com.br/admin/clients")
    Pesquisa = self.Driver.find_element(By.ID, value="keyword") 
    Pesquisa.clear()
    Pesquisa.send_keys(Cnpj)
    Pesquisa.send_keys(Keys.ENTER)
    try:
        Editar = self.Driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
        Editar = Editar.get_attribute("href")
        self.Driver.get(str(Editar)) 
        time.sleep(2)
        Carteira = self.Driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[10].find_element(By.XPATH, value=".//a")
        Carteira.click()
        Carteira = self.Driver.find_element(By.XPATH, value="(//select[@class='form-control select-multiple side2side-selected-options side2side-select-taller'])[1]")
        Carteira = Select(Carteira)
        Carteira = Carteira.options
        Vendedor = Carteira[0].text
    except:

        # ~~ Se não encontra vendedor 1105, tenta encontrar pelo 1101 nos ativos.
        try:
            self.Driver.get("https://www.revendedorpositivo.com.br/admin/direct-billing-clients")
            Pesquisa = self.Driver.find_element(By.ID, value="keyword") 
            Pesquisa.clear() 
            Pesquisa.send_keys(Cnpj) 
            Ativo = self.Driver.find_element(By.ID, value="active-1")
            Ativo.click()
            Pesquisa.send_keys(Keys.ENTER)
            Editar = self.Driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_element(By.XPATH, value="//td[contains(@data-title, 'Ações')]/a").get_attribute("href")
            self.Driver.get(str(Editar))
            Cnpj = self.Driver.find_element(By.ID, value="resale_cnpj").get_attribute("value")
            self.Driver.get("https://www.revendedorpositivo.com.br/admin/clients")
            Pesquisa = self.Driver.find_element(By.ID, value="keyword")
            Pesquisa.clear() 
            Pesquisa.send_keys(Cnpj) 
            Pesquisa.send_keys(Keys.ENTER) 
            Editar = self.Driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
            Editar = Editar.get_attribute("href") 
            self.Driver.get(str(Editar)) 
            time.sleep(2)
            Carteira = self.Driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[10].find_element(By.XPATH, value=".//a") 
            Carteira.click() 
            Carteira = self.Driver.find_element(By.XPATH, value="(//select[@class='form-control select-multiple side2side-selected-options side2side-select-taller'])[1]") 
            Carteira = Select(Carteira) 
            Carteira = Carteira.options 
            Vendedor = Carteira[0].text 
        
        # ~~ Se não encontrar 1101 ativos, procura nos inativos.
        except:
            self.Driver.get("https://www.revendedorpositivo.com.br/admin/direct-billing-clients")
            Pesquisa = self.Driver.find_element(By.ID, value="keyword") 
            Pesquisa.clear() 
            Pesquisa.send_keys(Cnpj) 
            Inativo = self.Driver.find_element(By.ID, value="active-0")
            Inativo.click()
            Pesquisa.send_keys(Keys.ENTER)
            Editar = self.Driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_element(By.XPATH, value="//td[contains(@data-title, 'Ações')]/a").get_attribute("href")
            self.Driver.get(str(Editar))
            Cnpj = self.Driver.find_element(By.ID, value="resale_cnpj").get_attribute("value")
            self.Driver.get("https://www.revendedorpositivo.com.br/admin/clients")
            Pesquisa = self.Driver.find_element(By.ID, value="keyword")
            Pesquisa.clear() 
            Pesquisa.send_keys(Cnpj) 
            Pesquisa.send_keys(Keys.ENTER) 
            Editar = self.Driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
            Editar = Editar.get_attribute("href") 
            self.Driver.get(str(Editar)) 
            time.sleep(2)
            Carteira = self.Driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[10].find_element(By.XPATH, value=".//a") 
            Carteira.click() 
            Carteira = self.Driver.find_element(By.XPATH, value="(//select[@class='form-control select-multiple side2side-selected-options side2side-select-taller'])[1]") 
            Carteira = Select(Carteira)
            Carteira = Carteira.options
            Vendedor = Carteira[0].text
    
    # ~~ Retorna.
    return Vendedor

# ================================================== #

# ~~ Coleta escritório do pedido.
def VerificarEscritório(self, Vendedor: str) -> int:

    """
    Resumo:
    * Verifica escritório do vendedor passado como parâmetro.
    ---
    Parâmetros:
    * Vendedor -> Nome do vendedor.
    ---
    Retorna:
    * Escritório -> Número do escritório.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Verifica se vendedor está na lista da planilha.
    for Linha in range(2, 99999):
        Célula = self.Controle["VENDEDORES"].range("A" + str(Linha)).value
        if Célula is None:
            return "-"
        elif Célula == Vendedor:
            Escritório = self.Controle["VENDEDORES"].range("B" + str(Linha)).value
            Escritório = int(Escritório)
            return Escritório

# ================================================== #

# ~~ Coleta cliente do pedido.
def ColetarClienteSite(self) -> dict:

    """
    Resumo:
    * Coleta o cliente do pedido no site.
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * DadosCliente -> Dicionário contendo: ["Razão"] - ["CNPJ/CPF"] - ["CódigoERP"]
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Cria dicionário.
    DadosCliente = {}

    # ~~ Coleta CNPJ.
    DadosCliente["CNPJ/CPF"] = self.Driver.find_element(By.XPATH, value="//label[@for='client_cnpj']/following-sibling::div[@class='col-md-12']").text

    # ~~ Acessa SAP para coletar razão social e código ERP.
    self.Session.findById("wnd[0]/tbar[0]/okcd").text = "/NXD03"
    self.Session.findById("wnd[0]").sendVKey(0)
    self.Session.findById("wnd[1]").sendVKey(4)
    self.Session.findById("wnd[2]/usr/tabsG_SELONETABSTRIP/tabpTAB006").select()
    self.Session.findById("wnd[2]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[0,24]").text = DadosCliente["CNPJ"]
    self.Session.findById("wnd[2]/tbar[0]/btn[0]").press()
    MsgBar = self.Session.findById("wnd[0]/sbar").text
    if "Nenhum valor" in MsgBar:
        DadosCliente["CódigoERP"] = "-"
        DadosCliente["Razão"] = "-"
        self.Session.findById("wnd[2]").close()
        self.Session.findById("wnd[1]").close()
        return DadosCliente
    self.Session.findById("wnd[2]").sendVKey(2)
    DadosCliente["CódigoERP"] = self.Session.findById("wnd[1]/usr/ctxtRF02D-KUNNR").text
    self.Session.findById("wnd[1]/usr/ctxtRF02D-BUKRS").text = "1000"
    self.Session.findById("wnd[1]").sendVKey(0)
    Razão1 = self.Session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0201/subAREA1:SAPMF02D:7111/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/txtADDR1_DATA-NAME1").text
    Razão2 = self.Session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0201/subAREA1:SAPMF02D:7111/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/txtADDR1_DATA-NAME2").text
    if Razão2 != "":
        DadosCliente["Razão"] = f"{Razão1} {Razão2}"
    else:
        DadosCliente["Razão"] = Razão1

    # ~~ Retorna.
    return DadosCliente

# ================================================== #

# ~~ Coleta comissão over do pedido.
def VerificarOverSite(self) -> str:

    """
    Resumo:
    * Coleta o over do pedido no site.
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * ComissãoOver -> Se possui comissão over.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Coleta comissão over.
    ComissãoOver = self.Driver.find_element(By.XPATH, value="//div[@class='panel distribution-center']").text 
    if "Comissão total (comissão unitários)" in ComissãoOver:
        ComissãoOver = "SIM"
    else: 
        ComissãoOver = "NÃO"

    # ~~ Retorna.
    return ComissãoOver

# ================================================== #

# ~~ Coleta valor do pedido.
def ColetarValorSite(self) -> str:

    """
    Resumo:
    * Coleta o valor do pedido no site.
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * ValorPedido -> Valor do pedido.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Coleta valor do pedido.
    ValorPedido = self.Driver.find_element(By.XPATH, value="//label[@for='payment_value']/following-sibling::div[@class='col-md-12']").text 
    ValorPedido = ValorPedido.replace("R$", "").replace(".", "").replace(",", ".")
    ValorPedido = float(ValorPedido)

    # ~~ Retorna.
    return ValorPedido

# ================================================== #

# ~~ Coleta observação do pedido.
def ColetarObservaçãoSite(self) -> str:

    """
    Resumo:
    * Coleta a observação do pedido no site.
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * ObservaçãoPedido -> Observação do pedido.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Coleta observação.
    ObservaçãoPedido = self.Driver.find_element(By.XPATH, value="//label[@for='client_comment']/following-sibling::div[@class='col-md-12']").text 
    if ObservaçãoPedido == "":
        ObservaçãoPedido = "-"
    
    # ~~ Retorna.
    return ObservaçãoPedido

# ================================================== #

# ~~ Coleta ordem do pedido.
def ColetarOrdemSite(self) -> int:

    """
    Resumo:
    * Coleta a ordem do pedido no site.
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * Ordem -> Número da ordem SAP.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Coleta ordem.
    try:
        Ordem = self.Driver.find_element(By.ID, value="distribution_centers-3-external_id")
    except:
        try:
            Ordem = self.Driver.find_element(By.ID, value="distribution_centers-2-external_id")
        except:
            Ordem = self.Driver.find_element(By.ID, value="distribution_centers-1-external_id")
    Ordem = Ordem.get_attribute("value")
    if Ordem == "":
        Ordem = "-"

    # ~~ Retorna.
    return Ordem

# ================================================== #

# ~~ Coleta status do pedido.
def ColetarStatusSite(self) -> str:

    """
    Resumo:
    * Coleta o status do pedido no site.
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * StatusPedido -> Status do pedido.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Coleta status do pedido.
    try: 
        StatusPedido = self.Driver.find_element(By.NAME, value="distribution_centers[1][status]")
    except: 
        try:
            StatusPedido = self.Driver.find_element(By.NAME, value="distribution_centers[2][status]")
        except:
            StatusPedido = self.Driver.find_element(By.NAME, value="distribution_centers[3][status]") 
    StatusPedido = Select(StatusPedido) 
    StatusPedido = StatusPedido.first_selected_option.text

    # ~~ Converte status.
    if StatusPedido in {"Crédito aprovado", "Pagamento aprovado"}:
        StatusPedido = "AGUARDANDO ORDEM"
    elif StatusPedido == "Pedido integrado":
        StatusPedido = "ANALISAR ORDEM"
    elif StatusPedido == "Em separação":
        StatusPedido = "AGUARDANDO FATURAR"
    elif StatusPedido in ["Expedido", "Expedido parcial", "Faturado"]:
        StatusPedido = "FATURADO"

    # ~~ Retorna.
    return StatusPedido

# ================================================== #

# ~~ Coleta centro(s) do pedido.
def ColetarCentroSite(self) -> str:

    """
    Resumo:
    * Coleta o centro do pedido no site.
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * Centro -> Centros que sairão o pedido.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Coleta centro.
    Centro1 = self.Driver.find_element(By.XPATH, value="(//div[@class='panel distribution-center']/div[@class='panel-heading'])[1]").text 
    try:
        Centro2 = self.Driver.find_element(By.XPATH, value="(//div[@class='panel distribution-center']/div[@class='panel-heading'])[2]").text 
        Centro = Centro1 + " - " + Centro2
    except:
        Centro = Centro1

    # ~~ Retorna.
    return Centro

# ================================================== #

# ~~ Coleta itens do pedido.
def ColetarItensSite(self) -> list:

    """
    Resumo:
    * Coleta os itens do pedido no site.
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * ItensPedido -> Lista com os itens e valores.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Coleta itens.
    self.Driver.execute_script("document.body.style.zoom='75%'")
    ListItems = []
    Tables = self.Driver.find_elements(By.XPATH, value="//div[@class='panel distribution-center']")
    for Table in Tables:
        if "Ilhéus" in Table.text:
            Centro = "3010"
        elif "Manaus" in Table.text:
            Centro = "1910"
        else:
            Centro = "1099"
        Footer = Table.find_element(By.XPATH, value="./div[@class='panel-footer']/table[@class='table table-striped']")
        Items = Footer.find_elements(By.XPATH, value=".//tbody/tr")
        for Item in Items:
            ItemData = {}
            ItemData["CENTRO"] = Centro
            ItemData["SKU"] = Item.find_elements(By.XPATH, value=".//td")[2].text
            ItemData["VALOR"] = Item.find_elements(By.XPATH, value=".//td")[17].text
            ListItems.append(ItemData)
    Df = pd.DataFrame(ListItems)
    Df["VALOR"] = Df["VALOR"].str.replace("R$", "").str.replace(" ", "")
    Df["SKU"] = Df["SKU"].str.lstrip("0")
    TotalLinhas = Df.shape[0]
    ItensPedido = []
    for Linha in range(0, TotalLinhas):
        Item = Df.iloc[Linha]["CENTRO"] + " - " + Df.iloc[Linha]["SKU"] + " - " + Df.iloc[Linha]["VALOR"]
        ItensPedido.append(Item)

    # ~~ Retorna.
    return ItensPedido

# ================================================== #

# ~~ Abre Controle.
def abrir_controle(self) -> dict:

    """
    Resumo:
    * Abre Controle (planilha do Excel).
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * Controle -> Dicionário contendo: ["BOOK"] - ["PEDIDOS"] - ["VENDEDORES"].
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Cria dicionário.
    Controle = {}

    # ~~ Se Table já estiver aberta, retorna.
    CaminhoScript = os.path.abspath(__file__)
    CaminhoControle = CaminhoScript.split(r"\ScriptFaturamento.py")[0] + r"\ControleFaturamento.xlsx"
    Controle["BOOK"] = xw.Book(CaminhoControle)
    Controle["PEDIDOS"] = Controle["BOOK"].sheets["PEDIDOS"]
    Controle["VENDEDORES"] = Controle["BOOK"].sheets["VENDEDORES"]

    # ~~ Retorna.
    return Controle

# ================================================== #

# ~~ Salva Controle.
def salvar_controle(self) -> None:

    """
    Resumo:
    * Salva o Controle.
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * ===
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Tenta salvar até 10x, se der, retorna.
    Tentativa = 0
    while Tentativa != 10:
        try:
            self.Controle["BOOK"].save()
            return
        except:
            Tentativa += 1
            time.sleep(2)

# ================================================== #

# ~~ Coletar última linha preenchida em coluna.
def ÚltimaLinhaPreenchida(self, Aba: str, Coluna: str) -> int:

    """
    Resumo:
    * Retorna última linha preenchida na coluna. Parâmetros são o nome da aba e a coluna.
    ---
    Parâmetros:
    * Aba -> Nome da aba.
    * Coluna -> Coluna.
    ---
    Retorna:
    * ÚltimaLinha -> Número da última linha preenchida.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Coleta última linha.
    ÚltimaLinha = self.Controle[Aba].range(Coluna + str("99999")).end("up").row

    # ~~ Retorna.
    return ÚltimaLinha

# ================================================== #

# ~~ Insere dados do pedido no Controle.
def InserirDadosPedidoNoControle(self, DadosPedido: dict) -> None:

    """
    Resumo:
    * Insere dados do pedido no Controle.
    ---
    Parâmetros:
    * DadosPedido -> Dicionário contendo os dados do pedido.
    ---
    Retorna:
    * ===
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Coleta última linha.
    Linha = self.ÚltimaLinhaPreenchida("PEDIDOS", "A")

    # ~~ Lista de colunas.
    Colunas = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL"]

    # ~~ Loop para inserir dados.
    for Coluna in Colunas:
        ColunaAtual = self.Controle["PEDIDOS"].range(Coluna + "1").value
        if ColunaAtual == "DATA DO PEDIDO":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["DATA"]
        if ColunaAtual == "PEDIDO":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["PEDIDO"]
        if ColunaAtual == "FORMA DE PAGAMENTO":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["FORMA DE PAGAMENTO"]
        if ColunaAtual == "VENDEDOR":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["VENDEDOR"]
        if ColunaAtual == "ESCRITÓRIO":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ESCRITÓRIO"]
        if ColunaAtual == "RAZÃO SOCIAL":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["CLIENTE"]["Razão"]
        if ColunaAtual == "CNPJ / CPF":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["CLIENTE"]["CNPJ/CPF"]
        if ColunaAtual == "CÓDIGO ERP":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["CLIENTE"]["CódigoERP"]
        if ColunaAtual == "POSSUI COMISSÃO OVER?":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["OVER"]
        if ColunaAtual == "COMISSÃO Z6":
            ComissãoZ6 = DadosPedido["Z6"]
            ComissãoZ6 = ComissãoZ6.replace(",", ".")
            ComissãoZ6 = float(ComissãoZ6)
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = ComissãoZ6
        if ColunaAtual == "VALOR DO PEDIDO":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["VALOR"]
        if ColunaAtual == "OBSERVAÇÃO":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["OBSERVAÇÃO"]
        if ColunaAtual == "ORDEM":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ORDEM"]
        if ColunaAtual == "STATUS":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["STATUS"]
        if ColunaAtual == "LIBERAÇÃO":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["LIBERAÇÃO"]
        if ColunaAtual == "CENTRO(S)":
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["CENTRO(S)"]
        if ColunaAtual == "ITEM 10":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][0]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 20":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][1]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 30":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][2]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 40":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][3]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 50":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][4]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 60":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][5]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 70":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][6]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 80":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][7]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 90":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][8]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 100":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][9]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 110":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][10]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 120":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][11]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 130":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][12]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 140":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][13]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"
        if ColunaAtual == "ITEM 150":
            try:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = DadosPedido["ITENS"][14]
            except:
                self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"

        # ~~ Coleta valor da célula, se for nula, insere "-".
        Célula = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
        if Célula is None:
            self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value = "-"

# ================================================== #

# ~~ Inicia SAP.
def iniciar_sap(self) -> object:

    """
    Resumo:
    * Cria vínculo com o SAP, acessando a SAPScriptingEngine.
    ---
    Parâmetros:
    * ===
    ---
    Retorna:
    * Session -> Conexão com SAP.
    ---
    Erros:
    * Não foi encontrado tela SAP disponível para conexão.
    ---
    Erros tratados localmente:
    * Não foi encontrado tela SAP disponível para conexão.
    ---
    Erros levantados:
    * ===
    """

    # ~~ Tenta conexão.
    try:
        Gui = win32com.client.GetObject("SAPGUI")
        App = Gui.GetScriptingEngine
        Con = App.Children(0)
        for Id in range(0, 4):
            Session = Con.Children(Id)
            if Session.ActiveWindow.Text == "SAP Easy Access":
                return Session
            else:
                continue

        # ~~ Se não encontrar tela disponível.
        else:
            self.printar_mensagens("Não foi encontrado tela SAP disponível para conexão.", "=", 30, "bot")
            self.encerrar_rpa()
    
    # ~~ Se não encontrar tela logada no SAP.
    except:
        self.printar_mensagens("Não foi encontrado tela SAP disponível para conexão.", "=", 30, "bot")
        self.encerrar_rpa()

# ================================================== #

# ~~ Abrir transação.
def AbrirTransação(self, Transação: str) -> None:

    """
    Resumo:
    * Abre transação no SAP.
    ---
    Parâmetros:
    * Transação -> Código da transação SAP.
    ---
    Retorna:
    * ===
    ---
    Erros:
    * Sem acesso à {Transação}.
    ---
    Erros tratados localmente:
    * Sem acesso à {Transação}.
    ---
    Erros levantados:
    * Sem acesso à {Transação}.
    """

    # ~~ Acessa transação.
    self.Session.findById("wnd[0]/tbar[0]/okcd").text = "/N" + Transação
    self.Session.findById("wnd[0]").sendVKey(0)
    StatusBarMsg = None
    StatusBarMsg = self.Session.findById("wnd[0]/sbar").text
    if "Sem autorização" in StatusBarMsg:
        Erro = f"Sem acesso à {Transação}."
        self.printar_mensagens(Erro, "=", 30, "bot")
        self.encerrar_rpa()

# ================================================== #

# ~~ Coleta dados do pedido direto do Controle.
def ColetarDadosPedidoControle(self, Pedido: int = None, Ordem: int = None) -> dict:

    """
    Resumo:
    * Coleta dados do pedido diretamente do Controle.
    ---
    Parâmetros:
    * Pedido (opcional) -> Forma de busca: pedido ou ordem.
    * Ordem (opcional) -> Forma de busca: pedido ou ordem.
    ---
    Retorna:
    * DadosPedido -> Dicionário com dados do pedido.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Lê planilha e encontra index do pedido ou ordem no Controle.
    Path = self.Controle["BOOK"].fullname
    self.salvar_controle()
    Df = pd.read_excel(Path, "PEDIDOS")
    if Pedido:
        Linha = Df.index[Df['PEDIDO'] == Pedido].tolist()
    elif Ordem:
        Linha = Df.index[Df['ORDEM'] == Ordem].tolist()
    Linha = int(Linha[0])
    Linha = Linha + 2

    # ~~ Cria dicionário novo.
    DadosPedido = {}

    # ~~ Lista de colunas para busca.
    Colunas = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL"]
    for Coluna in Colunas:

        # ~~ Pega coluna.
        ColunaAtual = self.Controle["PEDIDOS"].range(Coluna + "1").value

        # ~~ Data.
        if ColunaAtual == "DATA DO PEDIDO":
            DadosPedido["DATA"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value

        # ~~ Pedido.
        if ColunaAtual == "PEDIDO":
            PedidoN = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            try:
                DadosPedido["PEDIDO"] = int(PedidoN)
            except:
                pass
        
        # ~~ Forma de pagamento.
        if ColunaAtual == "FORMA DE PAGAMENTO":
            DadosPedido["FORMA DE PAGAMENTO"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value

        # ~~ Vendedor.
        if ColunaAtual == "VENDEDOR":
            DadosPedido["VENDEDOR"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
        
        # ~~ Escritório.
        if ColunaAtual == "ESCRITÓRIO":
            Escritório = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            try:
                Escritório = int(Escritório)
                Escritório = str(Escritório)
            except:
                pass
            DadosPedido["ESCRITÓRIO"] = Escritório
        
        # ~~ Razão social.
        if ColunaAtual == "RAZÃO SOCIAL":
            DadosPedido["RAZÃO"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value

        # ~~ CNPJ / CPF.
        if ColunaAtual == "CNPJ / CPF":
            DadosPedido["CNPJ/CPF"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value

        # ~~ Código ERP.
        if ColunaAtual == "CÓDIGO ERP":
            DadosPedido["CÓDIGO-ERP"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value

        # ~~ Status Cliente.
        if ColunaAtual == "STATUS CLIENTE":
            DadosPedido["STATUS-CLIENTE"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value

        # ~~ Over.
        if ColunaAtual == "POSSUI COMISSÃO OVER?":
            DadosPedido["OVER"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
        
        # ~~ Z6.
        if ColunaAtual == "COMISSÃO Z6":
            DadosPedido["Z6"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value

        # ~~ Valor.
        if ColunaAtual == "VALOR DO PEDIDO":
            Valor = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            DadosPedido["VALOR"] = float(Valor)

        # ~~ Observação.
        if ColunaAtual == "OBSERVAÇÃO":
            DadosPedido["OBSERVAÇÃO"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
        
        # ~~ Ordem.
        if ColunaAtual == "ORDEM":
            OrdemN = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            try:
                DadosPedido["ORDEM"] = int(OrdemN)
            except:
                pass
        
        # ~~ Status.
        if ColunaAtual == "STATUS":
            DadosPedido["STATUS"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
        
        # ~~ Liberação.
        if ColunaAtual == "LIBERAÇÃO":
            DadosPedido["LIBERAÇÃO"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value

        # ~~ Centro.
        if ColunaAtual == "CENTRO(S)":
            DadosPedido["CENTRO(S)"] = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value

        # ~~ Item 10.
        if ColunaAtual == "ITEM 10":
            Item10 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item10 != "-":
                DadosPedido["ITEM10-CENTRO"] = str(Item10).split(" - ")[0]
                DadosPedido["ITEM10-ITEM"] = str(Item10).split(" - ")[1]
                Item10Valor = str(Item10).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM10-VALOR"] = float(Item10Valor)
            else:
                DadosPedido["ITEM10-CENTRO"] = "-"
                DadosPedido["ITEM10-ITEM"] = "-"
                DadosPedido["ITEM10-VALOR"] = "-"
        
        # ~~ Item 20.
        if ColunaAtual == "ITEM 20":
            Item20 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item20 != "-":
                DadosPedido["ITEM20-CENTRO"] = str(Item20).split(" - ")[0]
                DadosPedido["ITEM20-ITEM"] = str(Item20).split(" - ")[1]
                Item20Valor = str(Item20).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM20-VALOR"] = float(Item20Valor)
            else:
                DadosPedido["ITEM20-CENTRO"] = "-"
                DadosPedido["ITEM20-ITEM"] = "-"
                DadosPedido["ITEM20-VALOR"] = "-"
        
        # ~~ Item 30.
        if ColunaAtual == "ITEM 30":
            Item30 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item30 != "-":
                DadosPedido["ITEM30-CENTRO"] = str(Item30).split(" - ")[0]
                DadosPedido["ITEM30-ITEM"] = str(Item30).split(" - ")[1]
                Item30Valor = str(Item30).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM30-VALOR"] = float(Item30Valor)
            else:
                DadosPedido["ITEM30-CENTRO"] = "-"
                DadosPedido["ITEM30-ITEM"] = "-"
                DadosPedido["ITEM30-VALOR"] = "-"

        # ~~ Item 40.
        if ColunaAtual == "ITEM 40":
            Item40 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item40 != "-":
                DadosPedido["ITEM40-CENTRO"] = str(Item40).split(" - ")[0]
                DadosPedido["ITEM40-ITEM"] = str(Item40).split(" - ")[1]
                Item40Valor = str(Item40).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM40-VALOR"] = float(Item40Valor)
            else:
                DadosPedido["ITEM40-CENTRO"] = "-"
                DadosPedido["ITEM40-ITEM"] = "-"
                DadosPedido["ITEM40-VALOR"] = "-"

        # ~~ Item 50.
        if ColunaAtual == "ITEM 50":
            Item50 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item50 != "-":
                DadosPedido["ITEM50-CENTRO"] = str(Item50).split(" - ")[0]
                DadosPedido["ITEM50-ITEM"] = str(Item50).split(" - ")[1]
                Item50Valor = str(Item50).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM50-VALOR"] = float(Item50Valor)
            else:
                DadosPedido["ITEM50-CENTRO"] = "-"
                DadosPedido["ITEM50-ITEM"] = "-"
                DadosPedido["ITEM50-VALOR"] = "-"
        
        # ~~ Item 60.
        if ColunaAtual == "ITEM 60":
            Item60 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item60 != "-":
                DadosPedido["ITEM60-CENTRO"] = str(Item60).split(" - ")[0]
                DadosPedido["ITEM60-ITEM"] = str(Item60).split(" - ")[1]
                Item60Valor = str(Item60).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM60-VALOR"] = float(Item60Valor)
            else:
                DadosPedido["ITEM60-CENTRO"] = "-"
                DadosPedido["ITEM60-ITEM"] = "-"
                DadosPedido["ITEM60-VALOR"] = "-"

        # ~~ Item 70.
        if ColunaAtual == "ITEM 70":
            Item70 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item70 != "-":
                DadosPedido["ITEM70-CENTRO"] = str(Item70).split(" - ")[0]
                DadosPedido["ITEM70-ITEM"] = str(Item70).split(" - ")[1]
                Item70Valor = str(Item70).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM70-VALOR"] = float(Item70Valor)
            else:
                DadosPedido["ITEM70-CENTRO"] = "-"
                DadosPedido["ITEM70-ITEM"] = "-"
                DadosPedido["ITEM70-VALOR"] = "-"
        
        # ~~ Item 80.
        if ColunaAtual == "ITEM 80":
            Item80 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item80 != "-":
                DadosPedido["ITEM80-CENTRO"] = str(Item80).split(" - ")[0]
                DadosPedido["ITEM80-ITEM"] = str(Item80).split(" - ")[1]
                Item80Valor = str(Item80).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM80-VALOR"] = float(Item80Valor)
            else:
                DadosPedido["ITEM80-CENTRO"] = "-"
                DadosPedido["ITEM80-ITEM"] = "-"
                DadosPedido["ITEM80-VALOR"] = "-"

        # ~~ Item 90.
        if ColunaAtual == "ITEM 90":
            Item90 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item90 != "-":
                DadosPedido["ITEM90-CENTRO"] = str(Item90).split(" - ")[0]
                DadosPedido["ITEM90-ITEM"] = str(Item90).split(" - ")[1]
                Item90Valor = str(Item90).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM90-VALOR"] = float(Item90Valor)
            else:
                DadosPedido["ITEM90-CENTRO"] = "-"
                DadosPedido["ITEM90-ITEM"] = "-"
                DadosPedido["ITEM90-VALOR"] = "-"

        # ~~ Item 100.
        if ColunaAtual == "ITEM 100":
            Item100 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item100 != "-":
                DadosPedido["ITEM100-CENTRO"] = str(Item100).split(" - ")[0]
                DadosPedido["ITEM100-ITEM"] = str(Item100).split(" - ")[1]
                Item100Valor = str(Item100).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM100-VALOR"] = float(Item100Valor)
            else:
                DadosPedido["ITEM100-CENTRO"] = "-"
                DadosPedido["ITEM100-ITEM"] = "-"
                DadosPedido["ITEM100-VALOR"] = "-"

        # ~~ Item 110.
        if ColunaAtual == "ITEM 110":
            Item110 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item110 != "-":
                DadosPedido["ITEM110-CENTRO"] = str(Item110).split(" - ")[0]
                DadosPedido["ITEM110-ITEM"] = str(Item110).split(" - ")[1]
                Item110Valor = str(Item110).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM110-VALOR"] = float(Item110Valor)
            else:
                DadosPedido["ITEM110-CENTRO"] = "-"
                DadosPedido["ITEM110-ITEM"] = "-"
                DadosPedido["ITEM110-VALOR"] = "-"

        # ~~ Item 120.
        if ColunaAtual == "ITEM 120":
            Item120 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item120 != "-":
                DadosPedido["ITEM120-CENTRO"] = str(Item120).split(" - ")[0]
                DadosPedido["ITEM120-ITEM"] = str(Item120).split(" - ")[1]
                Item120Valor = str(Item120).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM120-VALOR"] = float(Item120Valor)
            else:
                DadosPedido["ITEM120-CENTRO"] = "-"
                DadosPedido["ITEM120-ITEM"] = "-"
                DadosPedido["ITEM120-VALOR"] = "-"
        
        # ~~ Item 130
        if ColunaAtual == "ITEM 130":
            Item130 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item130 != "-":
                DadosPedido["ITEM130-CENTRO"] = str(Item130).split(" - ")[0]
                DadosPedido["ITEM130-ITEM"] = str(Item130).split(" - ")[1]
                Item130Valor = str(Item130).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM130-VALOR"] = float(Item130Valor)
            else:
                DadosPedido["ITEM130-CENTRO"] = "-"
                DadosPedido["ITEM130-ITEM"] = "-"
                DadosPedido["ITEM130-VALOR"] = "-"
        
        # ~~ Item 140.
        if ColunaAtual == "ITEM 140":
            Item140 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item140 != "-":
                DadosPedido["ITEM140-CENTRO"] = str(Item140).split(" - ")[0]
                DadosPedido["ITEM140-ITEM"] = str(Item140).split(" - ")[1]
                Item140Valor = str(Item140).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM140-VALOR"] = float(Item140Valor)
            else:
                DadosPedido["ITEM140-CENTRO"] = "-"
                DadosPedido["ITEM140-ITEM"] = "-"
                DadosPedido["ITEM140-VALOR"] = "-"
        
        # ~~ Item 150.
        if ColunaAtual == "ITEM 150":
            Item150 = self.Controle["PEDIDOS"].range(Coluna + str(Linha)).value
            if Item150 != "-":
                DadosPedido["ITEM150-CENTRO"] = str(Item150).split(" - ")[0]
                DadosPedido["ITEM150-ITEM"] = str(Item150).split(" - ")[1]
                Item150Valor = str(Item150).split(" - ")[2].replace(".", "").replace(",", ".")
                DadosPedido["ITEM150-VALOR"] = float(Item150Valor)
            else:
                DadosPedido["ITEM150-CENTRO"] = "-"
                DadosPedido["ITEM150-ITEM"] = "-"
                DadosPedido["ITEM150-VALOR"] = "-"

    # ~~ Retorna.
    return DadosPedido

# ================================================== #

# ~~ Coleta dados do pedido no site.
def ColetarDadosPedidoSite(self, Pedido: int) -> dict:

    """
    Resumo:
    * Coleta dados do pedido direto no site.
    ---
    Parâmetros:
    * Pedido -> Número do pedido.
    ---
    Retorna:
    * DadosPedido -> Dicionário com dados do pedido.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Cria novo dicionário.
    DadosPedido = {}

    # ~~ Coleta dados.
    self.acessar_pedido(Pedido)
    DadosPedido["DATA"] = self.coletar_data_site()
    DadosPedido["PEDIDO"] = Pedido
    DadosPedido["FORMA DE PAGAMENTO"] = self.ColetarFormaPagamentoSite()
    DadosPedido["VENDEDOR"] = self.ColetarVendedorSite()
    DadosPedido["ESCRITÓRIO"] = self.VerificarEscritório(DadosPedido["VENDEDOR"])
    DadosPedido["CLIENTE"] = self.ColetarClienteSite(Pedido)
    DadosPedido["OVER"] = self.VerificarOverSite()
    if DadosPedido["ESCRITÓRIO"] == 1101:
        DadosPedido["Z6"] = "2,50"
    else:
        DadosPedido["Z6"] = "0,50"
    DadosPedido["VALOR"] = self.ColetarValorSite()
    DadosPedido["OBSERVAÇÃO"] = self.ColetarObservaçãoSite()
    DadosPedido["ORDEM"] = self.ColetarOrdemSite()
    DadosPedido["STATUS"] = self.ColetarStatusSite()
    DadosPedido["LIBERAÇÃO"] = "-"
    DadosPedido["CENTRO(S)"] = self.ColetarCentroSite()
    DadosPedido["ITENS"] = self.ColetarItensSite()

    # ~~ Retorna.
    return DadosPedido

# ================================================== #

# ~~ Verifica se pedido está parado na ZSD290.
def VerificarPedidoParadoZSD290(self, Pedido: int) -> str:

    """
    Resumo:
    * Verifica se pedido está parado na ZSD290 e qual o erro.
    ---
    Parâmetros:
    * Pedido -> Número do pedido.
    ---
    Retorna:
    * Retorno -> Qual o erro do pedido parado.
    ---
    Erros:
    * Sem acesso à {Transação}.
    ---
    Erros tratados localmente:
    * Sem acesso à {Transação}.
    ---
    Erros levantados:
    * Sem acesso à {Transação}.
    """

    # ~~ Acessa ZSD290.
    self.AbrirTransação("ZSD290")
    self.Session.findById("wnd[0]/usr/txtSO_PDPOR-LOW").text = Pedido
    self.Session.findById("wnd[0]/tbar[1]/btn[8]").press()

    # ~~ Verifica se pedido está parado.
    Mensagem = self.Session.findById("wnd[0]/sbar").text
    if "Sem dados para exibição" in Mensagem:

        # ~~ Verifica se já passou 35m desde a integração.
        HoraAprovação = self.ColetarDataHoraAprovaçãoPedido(Pedido)
        HoraAprovação = datetime.strptime(HoraAprovação, "%d/%m/%Y %H:%M:%S")
        Dados = self.CompararDataHoraAprovação(HoraAprovação)
        if Dados["PassouReprocesso"] == "NÃO":
            Retorno = f"Pedido: {Pedido} não passou por período de reprocesso ainda. Aguardando."
            self.printar_mensagens(Retorno, "=", 30, "bot")
            return Retorno
        else:
            Retorno = f"Pedido: {Pedido} já passou por reprocesso. Verificar cadastro."
            self.printar_mensagens(Retorno, "=", 30, "bot")
            return Retorno

    # ~~ Se encontra pedido, verifica qual o erro.
    else:
        ListaErros = [
            "não existe no depósito", 
            "idioma PT não está previsto",
            "percentual máximo",
            "contas ZPPJ"
        ]

        # ~~ Printa mensagem.
        self.printar_mensagens(f"Pedido: {Pedido} está travado. Verificando erro.", "=", 30, "bot")

        # ~~ Tenta reprocessar.
        self.Session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").currentCellColumn = "ICO1"
        self.Session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").clickCurrentCell()
        try:
            self.Session.findById("wnd[1]/tbar[0]/btn[0]").press()
        except:
            pass
        try:
            self.Session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
            self.Session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
            self.Session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
            self.Session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
            self.Session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
        except:
            pass
        MsgBar = self.Session.findById("wnd[0]/sbar").text
        if "Sem dados para exibição" in MsgBar:
            self.printar_mensagens(f"Pedido: {Pedido} reprocessado com sucesso.", "=", 30, "bot")
            Retorno = "REPROCESSADO"
            return Retorno
        
        # ~~ Se não foi possível reprocessar, verifica qual o erro.
        self.Session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").currentCellColumn = "ICO2"
        self.Session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").clickCurrentCell()
        self.Session.findById("wnd[0]/tbar[1]/btn[40]").press()
        self.Session.findById("wnd[1]/usr/subSUB_DYN0500:SAPLSKBH:0610/cntlCONTAINER1_SORT/shellcont/shell").currentCellRow = 1
        self.Session.findById("wnd[1]/usr/subSUB_DYN0500:SAPLSKBH:0610/cntlCONTAINER1_SORT/shellcont/shell").selectedRows = "1"
        self.Session.findById("wnd[1]/usr/subSUB_DYN0500:SAPLSKBH:0610/btnAPP_WL_SING").press()
        self.Session.findById("wnd[1]/tbar[0]/btn[0]").press()
        MsgTudo = ""
        try:
            for Linha in range(0, 4):
                Msg = self.Session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").GetCellValue(Linha,"MENSAGEM")
                if MsgTudo == "":
                    MsgTudo = Msg
                else:
                    MsgTudo += "\n" + Msg
                for Expressao in ListaErros:
                    Erro = re.search(Expressao, Msg)
                    if Erro is not None:
                        Erro = Erro.group(0)
                        break
                if Erro is not None:
                    break
        except:
            pass

        # ~~ Verifica cada erro já catalogado e corrige.
        if Erro == "não existe no depósito":
            Retorno = "Material não existe no depósito 0175. Necessário cadastrá-lo na ZSD201."
            self.printar_mensagens(f"Erro: {Retorno}", "=", 30, "bot")
            return Retorno
        elif Erro == "idioma PT não está previsto":
            Material = Msg
            Material = re.search(r"Material (\d+)", Material)
            Material = Material.group(0)
            Material = re.search(r"(\d+)", Material)
            Material = Material.group(0)
            Retorno = f"Necessário ampliar material: {Material}."
            self.printar_mensagens(f"Erro: {Retorno}", "=", 30, "bot")
            return Retorno
        elif Erro == "percentual máximo":
            Retorno = "Erro de percentual comissão. Contatar pricing para correção."
            self.printar_mensagens(Retorno, "=", 30, "bot")
            return Retorno
        elif Erro == "contas ZPPJ":
            Retorno = "Alterar grupo ZPPJ para ZAGE."
            self.printar_mensagens(Retorno, "=", 30, "bot")
            return Retorno
        else:
            Retorno = "Erro não encontrado na lista dos catalogados: \n\n" + MsgTudo
            self.printar_mensagens(Retorno, "=", 30, "bot")
            return Retorno

# ================================================== #

# ~~ Verifica se cadastro do cliente está integrado.
def VerificarIntegraçãoCadastro(self, CódigoUrl: str, Escritório: str) -> str:

    """
    Resumo:
    * Verifica se cadastro do cliente está integrado no site.
    ---
    Parâmetros:
    * CódigoUrl -> Código URL do cliente.
    * Escritório -> Escritório.
    ---
    Retorna:
    * Cadastro -> Informa se cadastro foi integrado ou já estava.
    ---
    Erros:
    * Sem acesso à {Transação}.
    ---
    Erros tratados localmente:
    * Sem acesso à {Transação}.
    ---
    Erros levantados:
    * Sem acesso à {Transação}.
    """

    # ~~ Acessa ZSD262.
    self.AbrirTransação("ZSD262")

    # ~~ Insere informações.
    self.Session.findById("wnd[0]/usr/ctxtSO_CLI-LOW").text = CódigoUrl
    self.Session.findById("wnd[0]/tbar[1]/btn[8]").press()
    self.Session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").currentCellColumn = "ICO2"
    self.Session.findById("wnd[0]/usr/cntlGRID1/shellcont/shell").clickCurrentCell()
    Bar = self.Session.findById("wnd[0]/tbar[0]/okcd").text
    
    # ~~ Se na Bar estiver "/00", indica que o cadastro foi para tela de integração.
    if Bar == "/00":
        self.Session.findById("wnd[0]").sendVKey(0)
        self.Session.findById("wnd[0]/usr/ctxtKNVV-VKBUR").text = Escritório
        self.Session.findById("wnd[0]/usr/ctxtKNVV-VKGRP").text = "058"
        self.Session.findById("wnd[0]").sendVKey(0)
        self.Session.findById("wnd[0]").sendVKey(0)
        self.Session.findById("wnd[0]").sendVKey(0)
        self.Session.findById("wnd[0]").sendVKey(0)
        self.Session.findById("wnd[0]").sendVKey(0)
        MsgSucesso = self.Session.findById("wnd[0]/sbar").text
        self.printar_mensagens(f"Cadastro integrado: '{MsgSucesso}'.", "=", 30, "bot")
        Cadastro = "CADASTRO FOI INTEGRADO" 
        return Cadastro
    
    # ~~ Caso não tenha "/00" na Bar, cadastro já estava integrado.
    else:
        self.printar_mensagens(f"Cliente já está integrado.", "=", 30, "bot")
        Cadastro = "CADASTRO JÁ INTEGRADO"
        return Cadastro

# ================================================== #

# ~~ Coleta código URL do cliente.
def ColetarUrlCliente(self, Cnpj: str) -> dict:

    """
    Resumo:
    * Coleta código URL do cliente. Retorna código e escritório.
    ---
    Parâmetros:
    * Cnpj -> CNPJ.
    ---
    Retorna:
    * Dados -> Dicionário contendo: ["CódigoUrl"] - ["Escritório"].
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Cria dicionário.
    Dados = {}

    # ~~ Busca Código URL e escritório.
    self.Driver.get("https://www.revendedorpositivo.com.br/admin/clients")
    Pesquisa = self.Driver.find_element(By.ID, value="keyword") 
    Pesquisa.clear()
    Pesquisa.send_keys(Cnpj)
    Pesquisa.send_keys(Keys.ENTER)
    try:
        Editar = self.Driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
        Editar = Editar.get_attribute("href")
        EscCliente = "1105"
    except:
        self.Driver.get("https://www.revendedorpositivo.com.br/admin/direct-billing-clients")
        Inativo = self.Driver.find_element(By.ID, value="active-0")
        Inativo.click()
        Pesquisa = self.Driver.find_element(By.ID, value="keyword") 
        Pesquisa.clear() 
        Pesquisa.send_keys(Cnpj) 
        Pesquisa.send_keys(Keys.ENTER)
        Editar = self.Driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_element(By.XPATH, value="//td[contains(@data-title, 'Ações')]/a").get_attribute("href")
        EscCliente = "1101"
    Expressao = r"id/(\d+)"
    Editar = re.search(Expressao, Editar)
    Editar = Editar.group(1)

    # ~~ Insere dados no dicionário.
    Dados["CódigoUrl"] = Editar
    Dados["Escritório"] = EscCliente

    # ~~ Retorna.
    return Dados

# ================================================== #

# ~~ Altera pedido no site.
def AlterarPedidoSite(self, Pedido: int, AlterarStatus: str = None) -> None:

    """
    Resumo:
    * Salva pedido no site. Se "AlterarStatus" for passado, altera status do pedido no site.
    ---
    Parâmetros:
    * Pedido -> Número do pedido.
    * AlterarStatus (opcional) -> Status.
    ---
    Retorna:
    * None
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Acessa página.
    self.acessar_pedido(Pedido)
    if AlterarStatus is not None:

        # ~~ Encontra paineis e altera status em cada um.
        for i in range(1, 4):
            try: 
                StatusPedido = self.Driver.find_element(By.NAME, value=f"distribution_centers[{i}][status]")
                StatusPedido = Select(StatusPedido)
                StatusPedido.select_by_visible_text(AlterarStatus)
            except:
                continue

    # ~~ Salva.
    botãoSalvar = self.Driver.find_element(By.ID, value="save")
    botãoSalvar.click()

# ================================================== #

# ~~ Coleta data e hora de aprovação do pedido.
def ColetarDataHoraAprovaçãoPedido(self, Pedido: int) -> str:

    """
    Resumo.
    * Coleta data e hora da aprovação do pedido no site.
    ---
    Parâmetros:
    * Pedido -> Número do pedido.
    ---
    Retorna:
    * Alteração -> Data e hora da alteração no site.
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Acessa página.
    self.Driver.get(f"https://www.revendedorpositivo.com.br/admin/orders/detail/id/{Pedido}")

    # ~~ Encontra histórico de alteração de status.
    Alteração = self.Driver.find_element(By.ID, value="order-status-log")
    Alteração = Alteração.find_elements(By.XPATH, value=".//table/tbody/tr")[0]
    Alteração = Alteração.find_elements(By.XPATH, value=".//td")[4]
    Alteração = Alteração.find_element(By.XPATH, value=".//a").get_attribute("title")
    Alteração = Alteração.split("em ")[1].strip().replace(".", "")

    # ~~ Retorna.
    return Alteração

# ================================================== #

# ~~ Compara hora de aprovação com hora atual.
def CompararDataHoraAprovação(self, DataHoraAprovação: datetime) -> dict:

    """
    Resumo:
    * Compara data e hora da aprovação do pedido com data e hora atual.
    ---
    Parâmetros:
    * DataHoraAprovação -> Objeto datetime da hora à ser comparada.
    ---
    Retorna:
    * Dados -> Dicionário contendo: ["Diferença"] - ["PassouReprocesso"]
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Cria dicionário.
    Dados = {}

    # ~~ Coleta data e hora atual.
    HoraAtual = datetime.now()

    # ~~ Faz cálculo.
    Diferença = HoraAtual - DataHoraAprovação

    # ~~ Verifica diferença.
    if Diferença > timedelta(minutes=35):
        PassouReprocesso = "SIM"
    else:
        PassouReprocesso = "NÃO"

    # ~~ Insere no dicionário.    
    Dados["Diferença"] = Diferença
    Dados["PassouReprocesso"] = PassouReprocesso

    # ~~ Retorna.
    return Dados

# ================================================== #

# ~~ Verifica quem é revenda de cliente final.
def VerificarRevendedor(self, CnpjClienteFinal: str) -> dict:

    """
    Resumo:
    * Verifica qual é o revendedor de cliente final.
    ---
    Parâmetros:
    * CnpjClienteFinal -> CNPJ do cliente final.
    ---
    Retorna:
    * Dados -> Dicionário contendo: ["CnpjRevenda"] - ["IdErp"]
    ---
    Erros:
    * ===
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Cria dicionário.
    Dados = {}

    # ~~ Coleta dados do site.
    self.Driver.get("https://www.revendedorpositivo.com.br/admin/direct-billing-clients")
    Pesquisa = self.Driver.find_element(By.ID, value="keyword") 
    Pesquisa.clear() 
    Pesquisa.send_keys(CnpjClienteFinal) 
    Pesquisa.send_keys(Keys.ENTER)
    Ativo = self.Driver.find_element(By.ID, value="active-1")
    Ativo.click()
    Editar = self.Driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_element(By.XPATH, value="//td[contains(@data-title, 'Ações')]/a").get_attribute("href")
    self.Driver.get(str(Editar))
    Cnpj = self.Driver.find_element(By.ID, value="resale_cnpj").get_attribute("value")
    self.Driver.get("https://www.revendedorpositivo.com.br/admin/clients")
    Pesquisa = self.Driver.find_element(By.ID, value="keyword")
    Pesquisa.clear() 
    Pesquisa.send_keys(Cnpj) 
    Pesquisa.send_keys(Keys.ENTER) 
    Editar = self.Driver.find_elements(By.XPATH, value="//table/tbody/tr")[1].find_elements(By.XPATH, value=".//td")[10].find_element(By.XPATH, value=".//a") 
    Editar = Editar.get_attribute("href") 
    self.Driver.get(str(Editar))
    CnpjRevenda = self.Driver.find_element(By.ID, value="client-cnpj").text
    Moderação = self.Driver.find_element(By.XPATH, value="//section").find_elements(By.XPATH, value=".//ul/li")[5].find_element(By.XPATH, value=".//a") 
    Moderação.click()
    IdErp = self.Driver.find_element(By.ID, value="moderation-external_id").get_attribute("value")

    # ~~ Insere dados no dicionário.
    Dados["CnpjRevenda"] = CnpjRevenda
    Dados["IdErp"] = IdErp

    # ~~ Retorna.
    return Dados

# ================================================== #

# ~~ Obter código de fornecedor.
def ObterCódigoFornecedor(self, CódigoErp: str, Cnpj: str) -> str:

    """
    Resumo:
    * Retorna o código de fornecedor caso tenha.
    ---
    Parâmetros:
    * CódigoErp -> Código ERP.
    * Cnpj -> CNPJ.
    ---
    Retorna:
    * CódigoFornecedor -> Código de fornecedor.
    ---
    Erros:
    * Sem acesso à {Transação}.
    ---
    Erros tratados localmente:
    * Sem acesso à {Transação}.
    ---
    Erros levantados:
    * Sem acesso à {Transação}.
    """

    # ~~ Abre transação.
    self.AbrirTransação("XD03")
    
    # ~~ Coleta código de fornecedor.
    self.Session.findById(r"wnd[1]/usr/ctxtRF02D-KUNNR").text = CódigoErp
    self.Session.findById(r"wnd[1]/usr/ctxtRF02D-BUKRS").text = "1000"
    self.Session.findById("wnd[1]").sendVKey(0)
    self.Session.findById(r"wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02").select()
    CódigoFornecedor = self.Session.findById(r"wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02/ssubSUBSC:SAPLATAB:0200/subAREA1:SAPMF02D:7121/ctxtKNA1-LIFNR").text
    if CódigoFornecedor != "":
        return CódigoFornecedor
    else:
        self.Session.findById(r"wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02/ssubSUBSC:SAPLATAB:0200/subAREA1:SAPMF02D:7121/ctxtKNA1-LIFNR").SetFocus()
        self.Session.findById("wnd[0]").sendVKey(4)
        self.Session.findById(r"wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[0,24]").text = Cnpj
        self.Session.findById(r"wnd[1]/tbar[0]/btn[0]").press()
        MsgBar = self.Session.findById("wnd[0]/sbar").text
        if "Nenhum valor para esta seleção" in MsgBar:
            CódigoFornecedor = ""
            return CódigoFornecedor
        CódigoFornecedor = self.Session.findById(r"wnd[1]/usr/lbl[119,3]").text

        # ~~ Retorna.
        return CódigoFornecedor	

# ================================================== #

# ~~ Coleta código de comissão.
def ColetarCódigoComissão(self, Vendedor: str, TipoCódigo: str) -> str:

    """
    Resumo:
    * Retorna o código de fornecedor do vendedor para inserir na comissão.
    ---
    Parâmetros:
    * Vendedor -> Nome do vendedor.
    * TipoCódigo -> ["Assistente"] - ["Fornecedor].
    ---
    Retorna:
    * Código -> Código de comissão.
    ---
    Erros:
    * Vendedor não encontrado na lista de comissão. -> N1
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * Vendedor não encontrado na lista de comissão. -> N1
    """

    # ~~ Coleta código.
    Caminho = self.Controle["BOOK"].fullname
    Df = pd.read_excel(Caminho, "VENDEDORES")
    Linha = Df.index[Df['NOME'] == Vendedor].tolist()
    if Linha:
        Linha = int(Linha[0])
        Linha = Linha + 2
    else:
        raise ErrosN1(f"Vendedor não encontrado na lista de comissão.")
    if TipoCódigo == "Assistente":
        Código = self.Controle["VENDEDORES"].range("C" + str(Linha)).value
        Código = int(Código)
        Código = str(Código)
    else:
        Código = self.Controle["VENDEDORES"].range("D" + str(Linha)).value

    # ~~ Retorna.
    return Código

# ================================================== #

# ~~ Abre ordem no SAP.
def AbrirOrdemSAP(self, Ordem: int) -> None:

    """
    Resumo:
    * Abre ordem no SAP.
    ---
    Parâmetros:
    * Ordem -> Número da ordem.
    ---
    Retorna:
    * None
    ---
    Erros:
    * Sem acesso à {Transação}. -> N2
    ---
    Erros tratados localmente:
    * ===
    ---
    Erros levantados:
    * ===
    """

    # ~~ Abre ordem.
    self.AbrirTransação("VA02")
    self.Session.findById("wnd[0]/usr/ctxtVBAK-VBELN").text = ""
    self.Session.findById("wnd[0]/usr/ctxtVBAK-VBELN").text = Ordem
    self.Session.findById("wnd[0]").sendVKey(0)
    try:
        self.Session.findById("wnd[1]").sendVKey(0)
    except:
        pass

    # ~~ Retorna.
    return

# ================================================== #

# ~~ Abre ordem no SAP.
def AcessarCabeçalhoOrdem(self) -> None:

    """
    Resumo:
    * Acessa cabeçalho da ordem. Ordem deve estar aberta.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * None
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Abre cabeçalho.
    self.Session.findById("wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/btnBT_HEAD").press()

    # ~~ Retorna.
    return

# ================================================== #

# ~~ Coleta escritório da ordem.
def ColetarEscritórioOrdem(self) -> str:
    
    """
    Resumo:
    * Coleta escritório da ordem.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * EscritórioSap -> Número do escritório.
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Acessa cabeçalho.
    self.Session.findById("wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/btnBT_HEAD").press()

    # ~~ Coleta escritório.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01").select()
    EscritorioSap = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4301/ctxtVBAK-VKBUR").text
    self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()

    # ~~ Retorna.
    return EscritorioSap

# ================================================== #

# ~~ Modifica escritório na ordem.
def ModificarEscritórioOrdem(self, Escritório: str) -> None:

    """
    Resumo:
    * Insere escritório passado como parâmetro na ordem.
    ---
    Parâmetros:
    * Escritório -> Escritório.
    ---
    Retorna:
    * None
    ---
    Erros: 
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Acessa cabeçalho.
    self.Session.findById(r"wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/btnBT_HEAD").press()

    # ~~ Modifica escritório.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01").select()
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4301/ctxtVBAK-VKBUR").text = Escritório
    self.Session.findById(r"wnd[0]").sendVKey(0)
    self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
    self.printar_mensagens("Escritório corrigido.", "=", 30, "bot")

    # ~~ Retorna.
    return

# ================================================== #

# ~~ Verifica status de liberação.
def StatusLiberaçãoOrdem(self) -> str:

    """
    Resumo:
    * Retorna o status de liberação: Fiscal, Crédito e Pricing.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * Liberação -> Status de liberação: Fiscal, Crédito e Pricing.
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Verifica status do Pricing.
    Liberação = "FISCAL"
    Pricing = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/ssubHEADER_FRAME:SAPMV45A:4440/cmbVBAK-LIFSK").key
    if Pricing != " ":
        Liberação = Liberação + " - PRICING"

    # ~~ Acessa cabeçalho.
    self.Session.findById("wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/btnBT_HEAD").press()

    # ~~ Verifica status do Crédito.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\11").select()
    StatusCrédito = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\10/ssubSUBSCREEN_BODY:SAPMV45A:4305/txtVBSTT-CMGST_BEZ").text
    if "Operação não o.k." in StatusCrédito:
        Liberação = Liberação + " - CRÉDITO"

    # ~~ Volta para início.
    self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()

    # ~~ Retorna status.
    return Liberação

# ================================================== #

# ~~ Verifica se monitor irá sair de centro diferente e ajusta o Item Sup0.
def VerificarCentroMonitor(self) -> str:

    """
    Resumo:
    * Verifica se monitor irá sair de centro diferente e ajusta o Item Sup0.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * CorreçãoMonitor -> ["Item Sup do monitor corrigido."] - ["Monitor irá sair do mesmo centro que demais itens."] - ["Ordem sem monitor."]
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Verifica o centro que sairá o item pai.
    self.Session.findById("wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/btnBT_HEAD").press()
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01").select()
    CentroPai = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4301/ctxtVBAK-VKORG").text
    if CentroPai == "1600":
        CentroPai = "1910"
    elif CentroPai == "3100":
        CentroPai = "3010"
    else:
        CentroPai = "1099"
    self.Session.findById("wnd[0]/tbar[0]/btn[3]").press()

    # ~~ Acessando síntese de itens.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02").select()

    # ~~ Verifica se o monitor sairá de centro diferente.
    for Linha in range(0, 15):
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG").verticalScrollbar.position = Linha
        Denominação = self.Session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/txtVBAP-ARKTX[6,0]").text
        if Denominação == "":
            CorreçãoMonitor = "Ordem sem monitor."
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG").verticalScrollbar.position = 0
            self.printar_mensagens(CorreçãoMonitor, "=", 30, "bot")
            break
        if "MON" in Denominação:
            CentroMon = self.Session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtVBAP-WERKS[13,0]").text
            if CentroMon != CentroPai:
                self.Session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/txtVBAP-UEPOS[10,0]").text = "0"
                self.Session.findById("wnd[0]").sendVKey(0)
                self.Session.findById("wnd[0]").sendVKey(0)
                self.Session.findById("wnd[0]").sendVKey(0)
                CorreçãoMonitor = "Item Sup do monitor corrigido."
                self.printar_mensagens(CorreçãoMonitor, "=", 30, "bot")
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG").verticalScrollbar.position = 0
                break
            else:
                CorreçãoMonitor = "Monitor irá sair do mesmo centro que demais itens."
                self.printar_mensagens(CorreçãoMonitor, "=", 30, "bot")
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG").verticalScrollbar.position = 0
                break

    # ~~ Volta para início.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01").select()

    # ~~ Retorna.
    return CorreçãoMonitor

# ================================================== #

# ~~ Insere observação do pedido.
def InserirObservaçãoOrdem(self, Observação: str) -> None:

    """
    Resumo:
    * Insere observação nos dados adicionais da NF.
    ---
    Parâmetros:
    * Observação -> Observação.
    ---
    Retorna:
    * None
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Acessa cabeçalho.
    self.Session.findById("wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/btnBT_HEAD").press()

    # ~~ Insere texto em NF caso tenha.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\09").select()
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\09/ssubSUBSCREEN_BODY:SAPMV45A:4152/subSUBSCREEN_TEXT:SAPLV70T:2100/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[0]/shell").selectItem("9002","Column1")
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\09/ssubSUBSCREEN_BODY:SAPMV45A:4152/subSUBSCREEN_TEXT:SAPLV70T:2100/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[0]/shell").ensureVisibleHorizontalItem("9002","Column1")
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\09/ssubSUBSCREEN_BODY:SAPMV45A:4152/subSUBSCREEN_TEXT:SAPLV70T:2100/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[0]/shell").doubleClickItem("9002","Column1")
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\09/ssubSUBSCREEN_BODY:SAPMV45A:4152/subSUBSCREEN_TEXT:SAPLV70T:2100/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[1]/shell").text = Observação
    self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
    self.printar_mensagens(f"Inserido observação na ordem: {Observação}", "=", 30, "bot")

    # ~~ Retorna.
    return

# ================================================== #

# ~~ Insere código Supplier.
def InserirCódigoSupplier(self) -> None:

    """
    Resumo:
    * Insere código Supplier no cabeçalho da ordem.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * None
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Coleta forma de pagamento Supplier.
    FormaPagamentoSupplier = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/ssubHEADER_FRAME:SAPMV45A:4440/ctxtVBKD-ZTERM").text

    # ~~ Acessa cabeçalho.
    self.Session.findById("wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/btnBT_HEAD").press()

    # ~~ Acessa aba parceiro, modifica pagador e insere ZY.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08").select()
    for Linha in range(0, 99):
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW").verticalScrollbar.position = Linha
        Key = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW/cmbGVS_TC_DATA-REC-PARVW[0,0]").key
        if Key == "RG":
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW/ctxtGVS_TC_DATA-REC-PARTNER[1,0]").text = "1001401408"
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW").verticalScrollbar.position = 0
        if Key == " ":
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW/cmbGVS_TC_DATA-REC-PARVW[0,0]").key = "ZY"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW/ctxtGVS_TC_DATA-REC-PARTNER[1,0]").text = "1001401408"
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById("wnd[0]").sendVKey(0)
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW").verticalScrollbar.position = 0
            break

    # ~~ Volta para início.
    self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()

    # ~~ Devolve forma de pagamento.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/ssubHEADER_FRAME:SAPMV45A:4440/ctxtVBKD-ZTERM").text = FormaPagamentoSupplier
    self.Session.findById("wnd[0]").sendVKey(0)
    self.Session.findById("wnd[0]").sendVKey(0)
    try:
        self.Session.findById("wnd[0]/tbar[1]/btn[18]").press()
    except:
        pass

    # ~~ Mensagem.
    self.printar_mensagens("Inserido Supplier.", "=", 30, "bot")

    # ~~ Retorna.
    return

# ================================================== #

# ~~ Corrige valor da ordem.
def CorrigirValorOrdem(self,
                        Centro10: str = None, Item10: str = None, Valor10: str = None, 
                        Centro20: str = None, Item20: str = None, Valor20: str = None,
                        Centro30: str = None, Item30: str = None, Valor30: str = None,
                        Centro40: str = None, Item40: str = None, Valor40: str = None,
                        Centro50: str = None, Item50: str = None, Valor50: str = None,
                        Centro60: str = None, Item60: str = None, Valor60: str = None, 
                        Centro70: str = None, Item70: str = None, Valor70: str = None, 
                        Centro80: str = None, Item80: str = None, Valor80: str = None, 
                        Centro90: str = None, Item90: str = None, Valor90: str = None, 
                        Centro100: str = None, Item100: str = None, Valor100: str = None,
                        Centro110: str = None, Item110: str = None, Valor110: str = None, 
                        Centro120: str = None, Item120: str = None, Valor120: str = None, 
                        Centro130: str = None, Item130: str = None, Valor130: str = None, 
                        Centro140: str = None, Item140: str = None, Valor140: str = None, 
                        Centro150: str = None, Item150: str = None, Valor150: str = None):

    """
    Resumo:
    * Corrige valor da ordem se estiver errado.
    ---
    Parâmetros:
    * Ordem -> Número da ordem.
    * Centro -> Centro do item.
    * Item -> SKU do item.
    * Valor -> Valor do item.
    ---
    Retorna:
    * Correção -> Se foi feita ou não foi necessária.
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Acessando síntese de itens.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02").select()

    # ~~ Criando lista com os Itens.
    Centros = [Centro10, Centro20, Centro30, Centro40, Centro50, Centro60, Centro70, Centro80, Centro90, Centro100, 
                Centro110, Centro120, Centro130, Centro140, Centro150]
    Itens = [Item10, Item20, Item30, Item40, Item50, Item60, Item70, Item80, Item90, Item100,
                Item110, Item120, Item130, Item140, Item150]
    Valores = [Valor10, Valor20, Valor30, Valor40, Valor50, Valor60, Valor70, Valor80, Valor90, Valor100, Valor110,
                Valor120, Valor130, Valor140, Valor150]

    # ~~ Checando valores.
    AlgumAjusteFeito = False
    for Item in range(0, 15):
        if Itens[Item] == "-" or Itens[Item] == None:
            break
        try:
            self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
        except:
            pass
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02").select()
        for Linha in range(0, 15):
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG").verticalScrollbar.position = Linha
            Código = self.Session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtRV45A-MABNR[1,0]").text
            Centro = self.Session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtVBAP-WERKS[13,0]").text
            if Código == Itens[Item] and Centro == Centros[Item]:
                self.Session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtRV45A-MABNR[1,0]").setFocus()
                break
        self.Session.findById("wnd[0]").sendVKey(2)
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06").select()
        while True:
            Quantidade = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/txtKOMP-MGAME").text
            Quantidade = int(Quantidade)
            Líquido = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/txtKOMP-NETWR").text
            Líquido = str(Líquido).replace(".", "").replace(",", ".")
            Líquido = float(Líquido)
            Imposto = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/txtKOMP-MWSBP").text
            Imposto = str(Imposto).replace(".", "").replace(",", ".")
            Imposto = float(Imposto)
            ValorTotal = Líquido + Imposto
            ValorTotal = round(ValorTotal, 2)
            if Valores[Item] == ValorTotal:
                break
            else:
                Diferença = Valores[Item] - ValorTotal
                Diferença = round(Diferença, 2)
                if 0 < Diferença <= 0.15 or -0.15 < Diferença <= 0:
                    for Linha in range(70, 90):
                        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN").verticalScrollbar.position = Linha
                        ZD15 = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/ctxtKOMV-KSCHL[1,0]").text
                        if ZD15 == "ZD15":
                            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/txtKOMV-KBETR[3,0]").text = Diferença
                            break
                    self.Session.findById("wnd[0]").sendVKey(0)
                    self.Session.findById("wnd[0]").sendVKey(0)
                    self.printar_mensagens(f"Ajustado ZD15 do item nº {Item + 1} para: {Diferença}.", "=", 30, "bot")
                    AlgumAjusteFeito = True
                else:
                    ValorZP13 = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/txtKOMV-KBETR[3,3]").text
                    ValorZP13 = str(ValorZP13).replace(".", "").replace(",", ".")
                    ValorZP13 = float(ValorZP13)
                    Diferença = Diferença / Quantidade
                    Diferença = round(Diferença, 2) 
                    NovoValorZP13 = Diferença + ValorZP13
                    NovoValorZP13 = round(NovoValorZP13, 2)
                    NovoValorZP13 = str(NovoValorZP13).replace(".", ",")
                    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN").verticalScrollbar.position = 0
                    try:
                        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/txtKOMV-KBETR[3,7]").text = ""
                    except:
                        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/txtKOMV-KBETR[3,8]").text = ""
                    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/txtKOMV-KBETR[3,3]").text = NovoValorZP13
                    self.Session.findById("wnd[0]").sendVKey(0)
                    self.Session.findById("wnd[0]").sendVKey(0)
                    self.printar_mensagens(f"Ajustado ZP13 do item nº {Item + 1} para: {NovoValorZP13}.", "=", 30, "bot")
                    AlgumAjusteFeito = True
    
    # ~~ Mensagem.
    if AlgumAjusteFeito == True:
        self.printar_mensagens("Valores corrigidos.", "=", 30, "bot")
        self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01").select()
        Correção = "Valores corrigidos." 
        return Correção
    else:
        self.printar_mensagens("Nenhum ajuste necessário.", "=", 30, "bot")
        self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01").select()
        Correção = "Nenhum ajuste necessário." 
        return Correção

# ================================================== #

# ~~ Corrige comissão.
def CorrigirComissãoOrdem(self, DadosPedido: dict) -> str:

    """
    Resumo:
    * Corrige comissão se necessário.
    ---
    Parâmetros:
    * DadosPedido -> Dicionário com dados do pedido.
    ---
    Retorna:
    * CorreçãoComissão -> Qual tipo de correção foi ou não efetuada.
    ---
    Erros:
    * Pedido tem comissão over mas revenda não tem código de fornecedor. -> N1
    * Vendedor não encontrado na lista de comissão. -> N1
    * Sem acesso à {Transação}. -> N2
    ---
    Níveis de erros tratados aqui:
    * N1
    """

    # ~~ Se pedido for do 1105, verifica se possui over e coleta código de fornecedor.
    if DadosPedido["OVER"] == "SIM" and DadosPedido["ESCRITÓRIO"] == "1105":
        DadosRevendedor = self.VerificarRevendedor(DadosPedido["CNPJ"])
        CódigoFornecedorRevenda = self.ObterCódigoFornecedor(DadosRevendedor["IdErp"], DadosRevendedor["CnpjRevenda"])
        if CódigoFornecedorRevenda == "":
            raise ErrosN1("Pedido tem comissão over mas revenda não tem código de fornecedor.")
        else:
            self.AbrirOrdemSAP(DadosPedido["ORDEM"])

    # ~~ Coleta códigos de comissão.
    try:
        CódigoZ1 = self.ColetarCódigoComissão(DadosPedido["VENDEDOR"], "Fornecedor")
        CódigoZ6 = self.ColetarCódigoComissão(DadosPedido["VENDEDOR"], "Assistente")
    except ErrosN1:
        self.FecharOrdemSap()
        raise

    # ~~ Define valor padrão.
    AlgumAjusteFeito = False
    TipoDeCorreção = ""

    # ~~ Acessando síntese de itens e clicando no primeiro item.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02").select()
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtRV45A-MABNR[1,0]").setFocus()
    self.Session.findById("wnd[0]").sendVKey(2)

    # ~~ Acessando Dados Adicionais B.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15").select()

    # ~~ Coleta dados de todos os campos.
    PrimeiraCélula = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-NAME1[2,0]").text
    SegundaCélula = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-NAME1[2,1]").text
    TerceiraCélula = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-NAME1[2,2]").text
    QuartaCélula = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-NAME1[2,3]").text
    QuintaCélula = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-NAME1[2,4]").text
    SextaCélula = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-NAME1[2,4]").text

    # ~~ Verifica se comissão está em branco.
    if PrimeiraCélula == "":

        # ~~ Para escritório 1101:
        if DadosPedido["ESCRITÓRIO"] == "1101":
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,0]").key = "Z1"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,1]").key = "Z2"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,2]").key = "Z3"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,3]").key = "Z5"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,4]").key = "Z6"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,5]").key = "Z7"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,0]").text = CódigoZ1
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,1]").text = "2000006653"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,2]").text = "5000002513"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,3]").text = "2000005674"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,4]").text = CódigoZ6
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,5]").text = "COMPROV"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,0]").text = "7,45"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,1]").text = "0,30"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,2]").text = "0,50"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,3]").text = "0,30"
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,4]").text = DadosPedido["Z6"]
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,5]").text = "0,30"

        # ~~ Para escritório 1105:
        if DadosPedido["ESCRITÓRIO"] == "1105":

            # ~~ Para pedido com over.
            if DadosPedido["OVER"] == "SIM":
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,0]").key = "Z1"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,1]").key = "Z2"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,2]").key = "Z5"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,3]").key = "Z6"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,4]").key = "Z7"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,0]").text = CódigoFornecedorRevenda
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,1]").text = "2000006653"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,2]").text = "2000005674"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,3]").text = CódigoZ6
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,4]").text = "COMPROV"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,0]").text = ""
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,1]").text = "0,32"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,2]").text = "0,32"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,3]").text = DadosPedido["Z6"]
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,4]").text = "0,30"

            # ~~ Para pedido sem over.
            else:
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,0]").key = "Z2"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,1]").key = "Z5"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,2]").key = "Z6"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,3]").key = "Z7"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,0]").text = "2000006653"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,1]").text = "2000005674"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,2]").text = CódigoZ6
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,3]").text = "COMPROV"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,0]").text = "0,32"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,1]").text = "0,32"
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,2]").text = DadosPedido["Z6"]
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,3]").text = "0,30"

        # ~~ Confirma.
        self.Session.findById("wnd[0]").sendVKey(0)

        # ~~ Replica comissão.
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnBT_REPL_COMISS").press()
        self.Session.findById(r"wnd[1]/usr/btnBUTTON_1").press()
        self.Session.findById(r"wnd[1]/tbar[0]/btn[0]").press()

        # ~~ Volta para início.
        self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01").select()

        # ~~ Salva tipo de alteração feita.
        AlgumAjusteFeito = True
        if TipoDeCorreção == "":
            TipoDeCorreção += "Inserido comissão inteira."
        else:
            TipoDeCorreção += " - Inserido comissão inteira."

    # ~~ Verifica se possui comissão no Z6.
    if "AGENTE" in [PrimeiraCélula, SegundaCélula, TerceiraCélula, QuartaCélula, QuintaCélula, SextaCélula]:

        # ~~ Para escritório 1101.
        if DadosPedido["ESCRITÓRIO"] == "1101":
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,4]").text = CódigoZ6

        # ~~ Para escritório 1105.
        if DadosPedido["ESCRITÓRIO"] == "1105":

            # ~~ Para pedido com over.
            if DadosPedido["OVER"] == "SIM":
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,3]").text = CódigoZ6

            # ~~ Para pedido sem over.
            else:
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,2]").text = CódigoZ6

        # ~~ Confirma.
        self.Session.findById("wnd[0]").sendVKey(0)

        # ~~ Replica comissão.
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnBT_REPL_COMISS").press()
        self.Session.findById(r"wnd[1]/usr/btnBUTTON_1").press()
        self.Session.findById(r"wnd[1]/tbar[0]/btn[0]").press()

        # ~~ Volta para início.
        self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01").select()

        # ~~ Salva tipo de alteração feita.
        AlgumAjusteFeito = True
        if TipoDeCorreção == "":
            TipoDeCorreção += "Inserido Z6."
        else:
            TipoDeCorreção += " - Inserido Z6."

    # ~~ Verifica se vendedor é o mesmo da carteira.
    if self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,2]").key == "Z6":
        LinhaZ6 = "2"
    if self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,3]").key == "Z6":
        LinhaZ6 = "3"
    if self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,4]").key == "Z6":
        LinhaZ6 = "4"
    VendedorSap = self.Session.findById(fr"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-NAME1[2,{LinhaZ6}]").text
    if DadosPedido["VENDEDOR"] != VendedorSap:
        self.Session.findById(fr"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,{LinhaZ6}]").text = CódigoZ6

        # ~~ Confirma.
        self.Session.findById("wnd[0]").sendVKey(0)

        # ~~ Replica comissão.
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnBT_REPL_COMISS").press()
        self.Session.findById(r"wnd[1]/usr/btnBUTTON_1").press()
        self.Session.findById(r"wnd[1]/tbar[0]/btn[0]").press()

        # ~~ Volta para início.
        self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01").select()

        # ~~ Salva tipo de alteração feita.
        AlgumAjusteFeito = True
        if TipoDeCorreção == "":
            TipoDeCorreção += "Alterado vendedor para o que consta em carteira."
        else:
            TipoDeCorreção += " - Alterado vendedor para o que consta em carteira."
    
    # ~~ Encontra Z6 e verifica % de comissão.
    for Linha in range(0,10):
        Key = self.Session.findById(fr"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,{Linha}]").key
        if Key == "Z6":
            Porcentagem = self.Session.findById(fr"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,{Linha}]").text
            Porcentagem = str(Porcentagem).replace(",", ".")
            Porcentagem = float(Porcentagem)

            # ~~ Se porcentagem for diferente, atualiza ela.
            if Porcentagem != DadosPedido["Z6"]:
                self.Session.findById(fr"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,{Linha}]").text = DadosPedido["Z6"]
                
                # ~~ Confirma.
                self.Session.findById("wnd[0]").sendVKey(0)

                # ~~ Replica comissão.
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnBT_REPL_COMISS").press()
                self.Session.findById(r"wnd[1]/usr/btnBUTTON_1").press()
                self.Session.findById(r"wnd[1]/tbar[0]/btn[0]").press()

                # ~~ Volta para início.
                self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01").select()

                # ~~ Salva tipo de alteração feita.
                AlgumAjusteFeito = True
                if TipoDeCorreção == "":
                    TipoDeCorreção += f"Alterado porcentagem de comissão: {Porcentagem} ==> {DadosPedido["Z6"]}."
                else:
                    TipoDeCorreção += f" - Alterado porcentagem de comissão: {Porcentagem} ==> {DadosPedido["Z6"]}."

            # ~~ Se porcentagem está correta, volta para início.
            else:
                self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01").select()

    # ~~ Verifica se foi feito algum ajuste na comissão.
    if AlgumAjusteFeito == True:
        self.printar_mensagens(TipoDeCorreção, "=", 30, "bot")
        return TipoDeCorreção
    else:
        TipoDeCorreção = "Sem correções necessárias."
        self.printar_mensagens(TipoDeCorreção, "=", 30, "bot")
        return TipoDeCorreção

# ================================================== #

# ~~ Verifica % da comissão.
def VerificarPorcentagemComissão(self, DadosPedido: dict) -> str:

    """
    Resumo: 
    * Altera % da comissão Z6.
    ---
    Parâmetros:
    * DadosPedido -> Dicionário com dados do pedido.
    ---
    Retorna:
    * Correção -> Tipo de correção feita ou não.
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Acessando síntese de itens e clicando no primeiro item.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02").select()
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtRV45A-MABNR[1,0]").setFocus()
    self.Session.findById("wnd[0]").sendVKey(2)

    # ~~ Acessando Dados Adicionais B.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15").select()

    # ~~ Encontra Z6 e verifica %.
    for linha in range(0,10):
        key = self.Session.findById(fr"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,{linha}]").key
        if key == "Z6":
            Porcentagem = self.Session.findById(fr"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,{linha}]").text
            Porcentagem = str(Porcentagem).replace(",", ".")
            Porcentagem = float(Porcentagem)
            if Porcentagem != DadosPedido["Z6"]:
                self.Session.findById(fr"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,{linha}]").text = DadosPedido["Z6"]
                Correção = f"Alterado porcentagem de comissão: {Porcentagem} ==> {DadosPedido["Z6"]}."
                self.printar_mensagens(Correção, "=", 30, "bot")
                self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01").select()
                return Correção
            else:
                Correção = "Sem ajuste necessário na %."
                self.printar_mensagens(Correção, "=", 30, "bot")
                self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
                self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01").select()
                return Correção
        else:
            continue

# ================================================== #

# ~~ Verifica alíquota PIS/COFINS.
def VerificarAlíquotaPisCofins(self) -> str:

    """
    Resumo:
    * Retorna a alíquota de PIS/COFINS da ordem.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * Declaração -> Se precisa ou não.
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Verifica se é PF.
    self.Session.findById("wnd[0]/tbar[1]/btn[6]").press()
    self.Session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02").select()
    try:
        CpfCnpj = self.Session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02/ssubSUBSC:SAPLATAB:0200/subAREA3:SAPMF02D:7122/lblKNA1-STCD2").text
    except:
        CpfCnpj = self.Session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02/ssubSUBSC:SAPLATAB:0200/subAREA3:SAPMF02D:7122/lblKNA1-STCD1").text
    self.Session.findById("wnd[0]/tbar[0]/btn[12]").press()
    if CpfCnpj == "CPF":
        Declaração = "NÃO PRECISA DECLARAÇÃO"
        self.printar_mensagens("Não precisa de declaração.", "=", 30, "bot")
        return Declaração

    # ~~ Acessando síntese de itens.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02").select()

    # ~~ Procura centro 1910.
    for Linha in range (0, 15):
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG").verticalScrollbar.position = Linha
        Centro = self.Session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtVBAP-WERKS[13,0]").text
        if Centro == "1910":
            self.Session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtRV45A-MABNR[1,0]").setFocus()
            self.Session.findById("wnd[0]").sendVKey(2)
            break 

    # ~~ Procura campo da alíquota.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06").select()
    for Linha in range(130, 150):
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN").verticalScrollbar.position = Linha
        YX72 = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/ctxtKOMV-KSCHL[1,0]").text
        if YX72 == "YX72":
            YX72Alíquota = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/txtKOMV-KBETR[3,0]").text
            YX72Alíquota = str(YX72Alíquota).replace(" ", "")
            self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01").select()
            break
    if YX72Alíquota == "7,600":
        Declaração = "PRECISA DECLARAÇÃO"
        self.printar_mensagens("Precisa de declaração.", "=", 30, "bot")
        return Declaração
    else:
        Declaração = "NÃO PRECISA DECLARAÇÃO"
        self.printar_mensagens("Não precisa de declaração.", "=", 30, "bot")
        return Declaração

# ================================================== #

# ~~ Verifica centros do teclado e mouse.
def VerificarCentrosTclMou(self) -> None:

    """
    Resumo:
    * Verifica se centros do teclado e mouse estão iguai ao centro do item pai.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * Alteração -> ["Alterado centros do teclado e mouse."] - ["Sem ajuste necessário."].
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Verifica o centro que sairá o item pai.
    self.Session.findById("wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/btnBT_HEAD").press()
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01").select()
    CentroPai = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4301/ctxtVBAK-VKORG").text
    if CentroPai == "1600":
        CentroPai = "1910"
    elif CentroPai == "3100":
        CentroPai = "3010"
    else:
        CentroPai = "1099"
    self.Session.findById("wnd[0]/tbar[0]/btn[3]").press()

    # ~~ Acessando síntese de itens.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02").select()

    # ~~ Verifica se o monitor sairá de centro diferente.
    Correção = "Sem ajuste necessário."
    for Linha in range(0, 15):
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG").verticalScrollbar.position = Linha
        Denominação = self.Session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/txtVBAP-ARKTX[6,0]").text
        if Denominação == "":
            self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG").verticalScrollbar.position = 0
            break
        if "TCL" in Denominação or "MOU" in Denominação:
            CentroItem = self.Session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtVBAP-WERKS[13,0]").text
            if CentroItem != CentroPai:
                self.Session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/txtVBAP-UEPOS[10,0]").text = "0"
                self.Session.findById("wnd[0]").sendVKey(0)
                self.Session.findById("wnd[0]").sendVKey(0)
                self.Session.findById("wnd[0]").sendVKey(0)
                Correção = "Alterado centros do teclado e mouse."
    self.printar_mensagens(Correção, "=", 30, "bot")

    # ~~ Volta para início.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01").select()

    # ~~ Retorna.
    return Correção

# ================================================== #

# ~~ Faz análise e correção de ordem.
def AnáliseCorreçãoOrdem(self, Pedido: int = None, Ordem: int = None) -> dict:

    """
    Resumo:
    * Faz correção da ordem com base nos dados do pedido coletados do Controle.
    ---
    Parâmetros:
    * Pedido -> Número do pedido.
    * Ordem -> Número da ordem.
    ---
    Retorna:
    * DadosAnálise -> Dicionário contendo: ["Alterações"] - ["SemAlterações"] - ["StatusLiberação"] - ["Resumo"]
    ---
    Erros:
    * Código ERP do cliente não encontrado. -> N1
    * Sem acesso à {Transação}. -> N2
    * Não foi possível salvar ordem. Possui erro de garantia. -> N1
    * Hierarquia não cadastrada. -> N1
    * Vendedor do pedido não localizado. -> N1
    * Pedido tem comissão over mas revenda não tem código de fornecedor. -> N1
    * Vendedor não encontrado na lista de comissão. -> N1
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Cria listas para salvar informações.
    Análise = {}
    Alterações = []
    SemAlterações = []
    StatusLiberação = None
    Resumo = None

    # ~~ Coleta dados do pedido.
    if Pedido:
        DadosPedido = self.ColetarDadosPedidoControle(Pedido = Pedido)
    elif Ordem:
        DadosPedido = self.ColetarDadosPedidoControle(Ordem = Ordem)

    # ~~ Verifica se possui vendedor.
    if DadosPedido["VENDEDOR"] == "SEM ATENDIMENTO":
        raise ErrosN1("Vendedor do pedido não localizado.")

    # ~~ Abre ordem.
    self.AbrirOrdemSAP(DadosPedido["ORDEM"])

    # ~~ Verifica se ordem possui hierarquia.
    self.printar_mensagens("Verificando se ordem possui hierarquia.", "=", 30, "bot")
    self.VerificarHierarquia()
    SemAlterações.append("Hierarquia")

    # ~~ Se for pedido Supplier.
    if DadosPedido["FORMA DE PAGAMENTO"] == "Boleto a Prazo Supplier":
        self.printar_mensagens("Pedido Supplier, ajustando ordem.", "=", 30, "bot")
        self.InserirCódigoSupplier()
        Alterações.append("Supplier")
    else:
        SemAlterações.append("Supplier")

    # ~~ Verifica escritório.
    self.printar_mensagens("Verificando escritório.", "=", 30, "bot")
    EscritorioSAP = self.ColetarEscritórioOrdem()
    if EscritorioSAP != DadosPedido["ESCRITÓRIO"]:
        self.ModificarEscritórioOrdem(DadosPedido["ESCRITÓRIO"])
        Alterações.append("Escritório")
    else:
        self.printar_mensagens("Escritório já está correto.", "=", 30, "bot")
        SemAlterações.append("Escritório")

    # ~~ Checa e corrige valores.
    self.printar_mensagens("Verificando valores da ordem.", "=", 30, "bot")
    CorreçãoValores = self.CorrigirValorOrdem(
                                            Centro10 = DadosPedido["ITEM10-CENTRO"], Item10 = DadosPedido["ITEM10-ITEM"], Valor10 = DadosPedido["ITEM10-VALOR"],
                                            Centro20 = DadosPedido["ITEM20-CENTRO"], Item20 = DadosPedido["ITEM20-ITEM"], Valor20 = DadosPedido["ITEM20-VALOR"],
                                            Centro30 = DadosPedido["ITEM30-CENTRO"], Item30 = DadosPedido["ITEM30-ITEM"], Valor30 = DadosPedido["ITEM30-VALOR"],
                                            Centro40 = DadosPedido["ITEM40-CENTRO"], Item40 = DadosPedido["ITEM40-ITEM"], Valor40 = DadosPedido["ITEM40-VALOR"],
                                            Centro50 = DadosPedido["ITEM50-CENTRO"], Item50 = DadosPedido["ITEM50-ITEM"], Valor50 = DadosPedido["ITEM50-VALOR"],
                                            Centro60 = DadosPedido["ITEM60-CENTRO"], Item60 = DadosPedido["ITEM60-ITEM"], Valor60 = DadosPedido["ITEM60-VALOR"],
                                            Centro70 = DadosPedido["ITEM70-CENTRO"], Item70 = DadosPedido["ITEM70-ITEM"], Valor70 = DadosPedido["ITEM70-VALOR"],
                                            Centro80 = DadosPedido["ITEM80-CENTRO"], Item80 = DadosPedido["ITEM80-ITEM"], Valor80 = DadosPedido["ITEM80-VALOR"],
                                            Centro90 = DadosPedido["ITEM90-CENTRO"], Item90 = DadosPedido["ITEM90-ITEM"], Valor90 = DadosPedido["ITEM90-VALOR"],
                                            Centro100 = DadosPedido["ITEM100-CENTRO"], Item100 = DadosPedido["ITEM10-ITEM"], Valor100 = DadosPedido["ITEM100-VALOR"],
                                            Centro110 = DadosPedido["ITEM110-CENTRO"], Item110 = DadosPedido["ITEM110-ITEM"], Valor110 = DadosPedido["ITEM110-VALOR"],
                                            Centro120 = DadosPedido["ITEM120-CENTRO"], Item120 = DadosPedido["ITEM120-ITEM"], Valor120 = DadosPedido["ITEM120-VALOR"],
                                            Centro130 = DadosPedido["ITEM130-CENTRO"], Item130 = DadosPedido["ITEM130-ITEM"], Valor130 = DadosPedido["ITEM130-VALOR"],
                                            Centro140 = DadosPedido["ITEM140-CENTRO"], Item140 = DadosPedido["ITEM140-ITEM"], Valor140 = DadosPedido["ITEM140-VALOR"],
                                            Centro150 = DadosPedido["ITEM150-CENTRO"], Item150 = DadosPedido["ITEM150-ITEM"], Valor150 = DadosPedido["ITEM150-VALOR"]
                                            )
    if CorreçãoValores == "Nenhum ajuste necessário.":
        SemAlterações.append("Valores")
    else:
        Alterações.append("Valores")

    # ~~ Insere observação se tiver.
    if DadosPedido["OBSERVAÇÃO"] != "-":
        self.InserirObservaçãoOrdem(DadosPedido["OBSERVAÇÃO"])
        Alterações.append("Observação")
    else:
        self.printar_mensagens("Pedido sem observação.", 30, "=", "bot")
        SemAlterações.append("Observação")

    # ~~ Verifica status de liberação.
    self.printar_mensagens("Verificando status de liberação.", "=", 30, "bot")
    StatusLiberação = self.StatusLiberaçãoOrdem()
    if not "CRÉDITO" in StatusLiberação:
        if DadosPedido["FORMA DE PAGAMENTO"] in ["Boleto a Prazo Supplier", "Cartão BNDES"]:
            StatusLiberação = StatusLiberação + " - CRÉDITO"
    self.printar_mensagens(f"Necessita liberação de: {StatusLiberação}.", "=", 30, "bot")

    # ~~ Verifica se monitor irá sair de centro diferente.
    self.printar_mensagens("Verificando se possui monitor e se precisa ajustar item sup.", "=", 30, "bot")
    CorreçãoMonitor = self.VerificarCentroMonitor()
    if CorreçãoMonitor == "Monitor irá sair do mesmo centro que demais itens." or CorreçãoMonitor == "Ordem sem monitor.":
        SemAlterações.append("Monitor item superior")
    else:
        Alterações.append("Monitor item superior")

    # ~~ Verifica se teclado e mouse estão com mesmo centro do item pai.
    self.printar_mensagens("Verificando se teclado e mouse estão com centro do item pai.", "=", 30, "bot")
    CorreçãoTclMou = self.VerificarCentrosTclMou()
    if CorreçãoTclMou == "Sem ajuste necessário.":
        SemAlterações.append("Centro teclado e mouse.")
    else:
        Alterações.append("Centro teclado e mouse.")

    # ~~ Comissão.
    self.printar_mensagens("Verificando comissão.", "=", 30, "bot")
    CorreçãoComissão = self.CorrigirComissãoOrdem(DadosPedido)
    if "Sem correções necessárias." in CorreçãoComissão:
        SemAlterações.append("Comissão")
    else:
        Alterações.append(f"Comissão: {CorreçãoComissão}")

    # ~~ Checa alíquota declaração de Manaus.
    if "Manaus" in DadosPedido["CENTRO(S)"]:
        self.printar_mensagens("Pedido com item saindo de MAO. Verificando alíquota.", "=", 30, "bot")
        Alíquota = self.VerificarAlíquotaPisCofins()
        StatusLiberação = StatusLiberação + f" - {Alíquota}"
    else:
        StatusLiberação = StatusLiberação + f" - NÃO PRECISA DECLARAÇÃO"
        self.printar_mensagens("Sem necessidade de checar alíquota.", "=", 30, "bot")

    # ~~ Salva ou fecha ordem.
    if Alterações:
        self.SalvarOrdem()
    else:
        self.FecharOrdemSap()

    # ~~ Montando resumo.
    MsgSemAlteração = "Segue etapas que não foram necessárias alterações:\n"
    for item in SemAlterações:
        MsgSemAlteração = MsgSemAlteração + "- " + item + "\n"
    MsgAlteração = "Segue etapas que foram feitas correções ou inserido informações:\n"
    for item in Alterações:
        MsgAlteração = MsgAlteração + "- " + item + "\n"
    if MsgSemAlteração == "Segue etapas que não foram necessárias alterações:\n":
        MsgSemAlteração = MsgSemAlteração + "-"
    if MsgAlteração == "Segue etapas que foram feitas correções ou inserido informações:\n":
        MsgAlteração = MsgAlteração + "-\n"
    Resumo = MsgSemAlteração + MsgAlteração
    Resumo = Resumo.strip()

    # ~~ Mensagem.
    self.printar_mensagens(Resumo, "=", 30, "bot")
    self.printar_mensagens(f"Necessita liberação de: {StatusLiberação}.", "=", 30, "bot")
    Análise["Alterações"] = Alterações
    Análise["SemAlterações"] = SemAlterações
    Análise["StatusLiberação"] = StatusLiberação
    Análise["Resumo"] = Resumo
    return Análise

# ================================================== #

# ~~ Verifica se ordem possui hierarquia.
def VerificarHierarquia(self) -> None:

    """
    Resumo:
    * Verifica se ordem possui hierarquia nos parceiros.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * None
    ---
    Erros:
    * Hierarquia não cadastrada. -> N1
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Acessa cabeçalho.
    self.Session.findById("wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/btnBT_HEAD").press()

    # ~~ Acessa aba parceiro.
    self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08").select()
    
    # ~~ Tenta encontrar hierarquia.
    for Linha in range(0, 99):
        self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW").verticalScrollbar.position = Linha
        Key = self.Session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW/cmbGVS_TC_DATA-REC-PARVW[0,0]").key
        if Key == "1A":
            self.printar_mensagens("Hierarquia cadastrada.", "=", 30, "bot")
            self.Session.findById("wnd[0]/mbar/menu[2]/menu[0]").select()
            return
        if Key == " ":
            self.printar_mensagens("Hierarquia não cadastrada.", "=", 30, "bot")
            self.Session.findById("wnd[0]/tbar[0]/btn[12]").press()
            raise ErrosN1("Hierarquia não cadastrada.")

# ================================================== #

# ~~ Salva ordem.
def SalvarOrdem(self) -> None:

    """
    Resumo:
    * Salva ordem. Ela deve estar aberta.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * None
    ---
    Erros:
    * Não foi possível salvar ordem. Possui erro de garantia. -> N1
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Salvar.
    self.Session.findById("wnd[0]/tbar[0]/btn[11]").press()
    try:
        self.Session.findById("wnd[0]/tbar[1]/btn[18]").press()
    except:
        pass
    MsgBar = self.Session.findById("wnd[0]/sbar").text
    if "sem garantia" in MsgBar:
        raise ErrosN1("Não foi possível salvar ordem. Possui erro de garantia.")
    elif "Não foi efetuada" in MsgBar:
        return
    elif "foi gravado" in MsgBar:
        return
    else:
        self.Session.findById("wnd[0]").sendVKey(0)
        try:
            self.Session.FindById("wnd[1]/usr/btnSPOP-VAROPTION1").press()
        except:
            pass
        return

# ================================================== #

# ~~ Insere resumo de correção de ordem no Controle.
def ImportarResumoCorreção(self, Pedido: int, Resumo: str = None, Status: str = None) -> None:

    """
    Resumo:
    * Insere o resumo da análise da ordem no Controle.
    ---
    Parâmetros:
    * Pedido -> Número do pedido.
    * Resumo -> Mensagem de resumo da correção.
    * Status -> Se status está corrigido ou não.
    ---
    Retorna:
    * None
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Importa correção.
    Caminho = self.Controle["BOOK"].fullname
    Df = pd.read_excel(Caminho, "CORREÇÕES")
    Linha = Df.index[Df['PEDIDO'] == Pedido].tolist()
    if Linha:
        Linha = int(Linha[0])
        Linha = Linha + 2
    else:
        Linha = self.ÚltimaLinhaPreenchida("Correções", "A")
        Linha = Linha + 1
    self.Controle["Correções"].range("A" + str(Linha)).value = Pedido
    DataHoraAtual = datetime.now()
    self.Controle["Correções"].range("C" + str(Linha)).value = DataHoraAtual
    if Resumo:
        self.Controle["Correções"].range("B" + str(Linha)).value = Resumo
    if Status:
        self.Controle["Correções"].range("D" + str(Linha)).value = Status

    # ~~ Retorna.
    return

# ================================================== #

# ~~ Altera grupo de ZPPJ para ZAGE.
def AlterarZppjParaZage(self, Pedido: int) -> None:

    """
    Resumo:
    * Altera grupo de contas do cliente de ZPPJ para ZAGE.
    ---
    Parâmetros:
    * Pedido -> Número do pedido.
    ---
    Retorna:
    * None
    ---
    Erros:
    * Sem acesso à {Transação}. -> N2
    ---
    Níveis de erros tratados aqui:
    * None
    """

    Cliente = self.ColetarClienteSite(Pedido)
    Cliente = re.search(r"\((\d+)\)", Cliente)
    Cliente = Cliente.group(1)
    self.AbrirTransação("XD07")
    self.Session.findById("wnd[0]/usr/ctxtRF02D-KUNNR").text = Cliente
    self.Session.findById("wnd[0]").sendVKey(0)
    self.Session.findById("wnd[1]/tbar[0]/btn[0]").press()
    self.Session.findById("wnd[1]/usr/cmbRF02D-KTOKD_NEW").key = "ZAGE"
    self.Session.findById("wnd[1]/tbar[0]/btn[0]").press()
    self.Session.findById("wnd[0]/tbar[0]/btn[11]").press()
    self.Session.findById("wnd[1]").sendVKey(0)
    Tentativa = 0
    while Tentativa != 3:
        Tentativa += 1
        MsgBar = self.Session.findById("wnd[0]/sbar").text
        if "As modificações foram executadas" in MsgBar:
            self.printar_mensagens(f"Alterado grupo de contas do cliente: {Cliente} para ZPPJ.", "=", 30, "bot")
            return
        else:
            self.Session.findById("wnd[1]").sendVKey(0)

# ================================================== #

# ~~ Verifica status atual do pedido no SAP.
def VerificarStatusPedidoSap(self, Pedido: int) -> str:

    """
    Resumo:
    * Verifica status atual do pedido na ZSD279.
    ---
    Parâmetros:
    * Pedido -> Número do pedido.
    ---
    Retorna:
    * Status -> Status do pedido.
    ---
    Erros:
    * Sem acesso à {Transação}. -> N2
    ---
    Níveis de erros tratados aqui:
    * None
    """

    self.AbrirTransação("ZSD279")
    self.Session.findById(r"wnd[0]/mbar/menu[3]/menu[0]").select()
    self.Session.findById(r"wnd[1]/usr/tblSAPLSVIXTCTRL_SEL_FLDS").getAbsoluteRow(6).selected = True
    self.Session.findById(r"wnd[1]/tbar[0]/btn[0]").press()
    self.Session.findById(r"wnd[1]/usr/tblSAPLSVIXTCTRL_QUERY/txtQUERY_TAB-BUFFER[3,0]").text = Pedido
    self.Session.findById(r"wnd[1]/tbar[0]/btn[8]").press()
    Status = self.Session.findById(r"wnd[0]/usr/tblSAPLZSD_F1_PEDLOGTCTRL_ZSD_F1_PEDLOG/cmbZSD_F1_PEDLOG-ETAPA[12,0]").key
    return Status

# ================================================== #

# ~~ Verifica se data de vencimento da nota é válida.
def VerificarSeEstáVencido(self, DataParaVerificar: str) -> str:

    """
    Resumo:
    * Verifica se data de vencimento da nota está vencida ou não.
    ---
    Parâmetros:
    * DataParaVerificar -> Data para verificar se está vencida.
    ---
    Retorna:
    * Resultado -> ["Vencido"] - ["Não vencido"]
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    DataVencido = datetime.strptime(DataParaVerificar, "%d/%m/%Y").date()
    DataAtual = datetime.now().date()
    if DataVencido < DataAtual:
        DiasVencidos = 0
        DataVencido = DataVencido + timedelta(days = 1)
        while DataVencido < DataAtual:
            if DataVencido.weekday() < 5:
                DiasVencidos += 1
            DataVencido = DataVencido + timedelta(days = 1)
        if DiasVencidos >= 2:
            return "Vencido"
        else:
            return "Não vencido"
    else:
        return "Não vencido"

# ================================================== #

# ~~ Coleta NF de ordem no SAP e verifica se está aprovada.
def ColetarNfSap(self, Ordem: int) -> dict:

    """
    Resumo:
    * Se ordem está faturada, coleta todas as notas no fluxo e verifica sua situação.
    ---
    Parâmetros:
    * Ordem -> Ordem.
    ----
    Retorna:
    * DadosNota -> Dicionário contendo: ["NF"] - ["Situação"] - ["Data"]
    ---
    Erros:
    * Sem acesso à {Transação}. -> N2
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Abre transação.
    self.AbrirTransação("VA02")

    # ~~ Insere ordem e acessa fluxo.
    self.Session.findById("wnd[0]/usr/ctxtVBAK-VBELN").text = Ordem
    self.Session.findById("wnd[0]/tbar[1]/btn[17]").press()

    # ~~ Procura NFs e salva elas em um array.
    Shell = self.Session.findById("wnd[0]/usr/shell/shellcont[1]/shell[1]")
    NodeNfs = []
    for Node in range(1, 10):
        Key = Shell.GetNodeTextByKey(f"          {Node}")
        if "Fatura - Venda" in Key:
            NodeNfs.append(Node)
            break
        else:
            continue
    for Node in range(10, 50):
        Key = Shell.GetNodeTextByKey(f"         {Node}")
        if "Fatura - Venda" in Key:
            NodeNfs.append(Node)
            break
        else:
            continue

    # ~~ Para cada NF encontrada, acessa ela e verifica sua situação.
    ListaNfs = []
    for Node in NodeNfs:
        DadosNf = {}
        if Node < 10:
            self.Session.findById("wnd[0]/usr/shell/shellcont[1]/shell[1]").selectItem(f"          {Node}", "&Hierarchy")
        else:
            self.Session.findById("wnd[0]/usr/shell/shellcont[1]/shell[1]").selectItem(f"         {Node}", "&Hierarchy")
        self.Session.findById("wnd[0]/tbar[1]/btn[8]").press()
        self.Session.findById("wnd[0]/tbar[1]/btn[16]").press()
        self.Session.findById("wnd[1]/usr/cntlCONTAINER/shellcont/shell").setCurrentCell(1, "OTEXT")
        self.Session.findById("wnd[1]/usr/cntlCONTAINER/shellcont/shell").selectedRows = "1"
        self.Session.findById("wnd[1]/usr/cntlCONTAINER/shellcont/shell").doubleClickCurrentCell()
        Nf = self.Session.findById("wnd[0]/usr/subNF_NUMBER:SAPLJ1BB2:2002/txtJ_1BDYDOC-NFENUM").text
        Série = self.Session.findById("wnd[0]/usr/txtJ_1BDYDOC-SERIES").text
        DadosNf["NF"] = Nf + "-" + Série
        self.Session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB8").select()
        DadosNf["Situação"] = self.Session.findById("wnd[0]/usr/tabsTABSTRIP1/tabpTAB8/ssubHEADER_TAB:SAPLJ1BB2:2800/subTIMESTAMP:SAPLJ1BB2:2803/cmbJ_1BDYDOC-DOCSTAT").text
        DadosNf["Situação"] = str(DadosNf["Situação"]).strip()
        DadosNf["Data"] = self.Session.findById("wnd[0]/usr/ctxtJ_1BDYDOC-PSTDAT").text
        DadosNf["Data"] = str(DadosNf["Data"]).replace(".", "/")
        self.Session.findById("wnd[0]/tbar[0]/btn[12]").press()
        self.Session.findById("wnd[1]").close()
        self.Session.findById("wnd[0]/tbar[0]/btn[3]").press()
        ListaNfs.append(DadosNf)
    self.Session.findById("wnd[0]/tbar[0]/btn[3]").press()
    self.printar_mensagens(f"Lista de NF:\n\n{ListaNfs}", "=", 30, "bot")

    # ~~ Retorna.
    return ListaNfs

# ================================================== #

# ~~ Fecha ordem SAP.
def FecharOrdemSap(self) -> None:

    """
    Resumo:
    * Fecha ordem que está aberta, sem salvar.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * None
    ---
    Erros:
    * None
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Fecha ordem.
    self.Session.findById("wnd[0]/tbar[0]/btn[12]").press()

    # ~~ Caso alterações tenham sido feitas, confirma sem salvar.
    try:
        self.Session.findById("wnd[1]/usr/btnSPOP-OPTION1").press()
    except:
        pass

# ================================================== #

    # ~~ Loop para cada linha.
    for Linha in range(2, 999999):

        # ~~ Verifica se foi alterado o encerramento global.
        if self.Encerrar == True:
            self.encerrar_rpa()

        # ~~ Coleta nº do pedido.
        Pedido = self.Controle["PEDIDOS"].range("A" + str(Linha)).value
        PrimeiroPedido = self.Controle["PEDIDOS"].range("B2").value

        # ~~ Se pedido for nulo, verifica se há novas inputações no site.
        if Pedido is None or PrimeiroPedido is None:

            # ~~ Verifica se existe um primeiro pedido para verificar. Se existe, pega último pedido no controle + 1.
            if PrimeiroPedido is not None:
                Pedido = int(self.Controle["PEDIDOS"].range("A" + str(Linha - 1)).value)
                Pedido = Pedido + 1
            else:
                Pedido = int(Pedido)

            DadosPedido = self.ColetarDadosPedidoSite(Pedido)

# ================================================== #

# ~~ Função main que controla todos as etapas.
def RotinaCompleta(self) -> None:

    """
    Resumo:
    * Controla todas as etapas do projeto.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * None
    ---
    Erros:
    * Sem acesso à {Transação}. -> N2
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Módulo 1: Atualizar Controle.
    self.AtualizarControle()

    # ~~ Módulo 2: Liberação de pedidos.
    self.LiberarPedidos()

    # ~~ Módulo 3: Verificação de pedidos parados na ZSD290.
    self.VerificarZSD290()
    
    # ~~ Módulo 4: Análise e correção de ordens.
    self.CorrigirOrdens()

    # ~~ Mensagem.
    self.printar_mensagens("Rotina encerrada.", "=", 30, "bot")

    # ~~ Retorna.
    return

# ================================================== #

# ~~ Módulo 1: Atualizar Controle.
def AtualizarControle(self) -> None:

    """
    Resumo:
    * Atualiza banco de dados com novos pedidos e seus dados.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * None
    ---
    Erros:
    * Sem acesso à {Transação}. -> N2
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Mensagem.
    self.printar_mensagens("Iniciando coleta de pedidos.", "=", 30, "bot")

    # ~~ Se há filtro ativo, desativa.
    if self.Controle["PEDIDOS"].api.AutoFilterMode:
        self.Controle["PEDIDOS"].api.AutoFilterMode = False

    # ~~ While True.
    while True:

        # ~~ Primeiro checa se há um primeiro pedido no Controle.
        while True:
            PrimeiroPedido = self.Controle["PEDIDOS"].range("B2").value
            if PrimeiroPedido is None:
                self.printar_mensagens("Não há pedido na primeira linha. Indique o primeiro pedido.", "=", 30, "bot")
                time.sleep(30)
            else:
                break

        # ~~ Checa se é o primeiro pedido que deve ser verificado, se não, coleta último pedido inserido.
        PrimeiroPedido = self.Controle["PEDIDOS"].range("A2").value
        if PrimeiroPedido is None:
            Pedido = int(self.Controle["PEDIDOS"].range("B2").value)
        else:
            Linha = self.ÚltimaLinhaPreenchida("Pedidos", "B")
            Pedido = int(self.Controle["PEDIDOS"].range("B" + str(Linha)).value) + 1
            Linha = Linha + 1
            self.Controle["PEDIDOS"].range("B" + str(Linha)).value = Pedido

        # ~~ Verifica se pedido está integrado no site. Se não estiver, encerra módulo.
        self.Driver.get(f"https://www.revendedorpositivo.com.br/admin/orders/edit/id/{Pedido}")
        PedidoInexistente = self.Driver.find_element(By.TAG_NAME, value="body").text 
        if "Application error: Mysqli statement execute error" in PedidoInexistente:
            self.printar_mensagens(f"Pedido: {Pedido} não inserido no site ainda. Coleta encerrada.", "=", 30, "bot")
            self.Controle["PEDIDOS"].range("B" + str(Linha)).value = ""
            break

        # ~~ Coleta dados do pedido e insere no Controle.
        DadosPedido = self.ColetarDadosPedidoSite(Pedido)
        self.InserirDadosPedidoNoControle(DadosPedido)

        # ~~ Printa dados.
        self.printar_mensagens(f"Pedido feito em:\n{DadosPedido["DATA"]}", "=", 30, "bot")
        self.printar_mensagens(f"O pedido é:\n{DadosPedido["PEDIDO"]}", "=", 30, "bot")
        self.printar_mensagens(f"A forma de pagamento é:\n{DadosPedido["FORMA DE PAGAMENTO"]}", "=", 30, "bot")
        self.printar_mensagens(f"O vendedor é:\n{DadosPedido["VENDEDOR"]}", "=", 30, "bot")
        self.printar_mensagens(f"Escritório:\n{DadosPedido["ESCRITÓRIO"]}", "=", 30, "bot")
        self.printar_mensagens(f"O cliente é:\n{DadosPedido["CLIENTE"]}", "=", 30, "bot")
        self.printar_mensagens(f"O status do cliente é:\n{DadosPedido["STATUS-CLIENTE"]}", "=", 30, "bot")
        self.printar_mensagens(f"Tem comissão over?:\n{DadosPedido["OVER"]}", "=", 30, "bot")
        self.printar_mensagens(f"Valor total do pedido:\n{DadosPedido["VALOR"]}", "=", 30, "bot")
        self.printar_mensagens(f"Observação do pedido:\n{DadosPedido["OBSERVAÇÃO"]}", "=", 30, "bot")
        self.printar_mensagens(f"A ordem é:\n{DadosPedido["ORDEM"]}", "=", 30, "bot")
        self.printar_mensagens(f"O status é:\n{DadosPedido["STATUS"]}", "=", 30, "bot")
        self.printar_mensagens(f"Centro(s) do pedido:\n{DadosPedido["CENTRO(S)"]}", "=", 30, "bot")
        self.printar_mensagens(f"Os itens do pedido são:\n{DadosPedido["ITENS"]}", "=", 30, "bot")

    # ~~ Atualiza dados dos pedidos.
    self.printar_mensagens("Iniciando atualizações de status.", "=", 30, "bot")

    # ~~ Loop para checar status linha a linha.
    for Linha in range(2, 99999):
        ListaDeStatusParaIgnorar = [
                                    "Cancelado pela positivo", 
                                    "Expedido", 
                                    "Cancelado falta de pagamento", 
                                    "Aguardando ajuste ordem.", 
                                    "Enviar para liberação.",
                                    "Aguardando liberação.",
                                    "Aprovado simbólico.",
                                    "Recusado simbólico.",
                                    "Erro ao analisar crédito."
                                    ]
        Pedido = self.Controle["PEDIDOS"].range("B" + str(Linha)).value
        Status = self.Controle["PEDIDOS"].range("M" + str(Linha)).value
        Ordem = self.Controle["PEDIDOS"].range("L" + str(Linha)).value
        FrmPagamento = self.Controle["PEDIDOS"].range("C" + str(Linha)).value
        VendedorAtual = self.Controle["PEDIDOS"].range("D" + str(Linha)).value
        Centros = self.Controle["PEDIDOS"].range("O" + str(Linha)).value
        StatusCliente = self.Controle["PEDIDOS"].range("G" + str(Linha)).value

        # ~~ Se pedido for nulo, é porque encerrou a lista de pedidos.
        if Pedido is None:
            self.printar_mensagens("Atualizações de status concluída.", "=", 30, "bot")
            return

        # ~~ Checa se status é relevante para atualizar.
        if Status in ListaDeStatusParaIgnorar:
            continue

        # ~~ Converte pedido.
        Pedido = int(Pedido)

        # ~~ Verifica centro.
        if "-" in Centros:
            Centros = "MISTO"
        else:
            Centros = "ÚNICO"

        # ~~ Printa mensagem.
        self.printar_mensagens(f"Atualizando status do pedido: {Pedido}.", "=", 30, "bot")

        # ~~ Acessa pedido.
        self.acessar_pedido(Pedido)

        # ~~ Coleta status atualizado e insere no controle.
        StatusNovo = self.ColetarStatusSite()
        self.Controle["PEDIDOS"].range("M" + str(Linha)).value = StatusNovo

        # ~~ Printa mensagem para a alteração de status.
        if Status != StatusNovo:
            self.printar_mensagens(f"Status atualizado: {Status} => {StatusNovo}", "=", 30, "bot")
        else:
            self.printar_mensagens("Sem alteração de status.", "=", 30, "bot")

        # ~~ Coleta ordem e insere no controle.
        if Ordem == "Ordem não integrada no SAP.":
            OrdemNova = self.ColetarOrdemSite()
            self.Controle["PEDIDOS"].range("L" + str(Linha)).value = OrdemNova

        # ~~ Se estiver sem vendedor, verifica se carteira foi atualizada.
        if VendedorAtual == "SEM ATENDIMENTO":
            Cliente = self.ColetarClienteSite()
            Vendedor = self.ColetarVendedorSite()
            Escritório = self.VerificarEscritório(Vendedor)
            self.Controle["PEDIDOS"].range("D" + str(Linha)).value = Vendedor
            self.Controle["PEDIDOS"].range("E" + str(Linha)).value = Escritório
            self.Controle["PEDIDOS"].range("F" + str(Linha)).value = Cliente

        # ~~ Se cliente estiver inativo, verifica integração do cadastro.
        if StatusCliente != "ATIVO":
            self.printar_mensagens(f"Cliente: {Cliente} consta inativo. Verificando se subiu seu código.", "=", 30, "bot")
            StatusClienteNovo = self.VerificarClienteAtivo(Pedido)
            if StatusClienteNovo == "INATIVO":
                self.printar_mensagens(f"Cliente: {Cliente} não está integrado. Verificando integração.", "=", 30, "bot")
                Cnpj = self.ColetarCnpjSite(self.Driver, Pedido)
                Retorno = self.ColetarUrlCliente(Cnpj)
                MsgRetorno = self.VerificarIntegraçãoCadastro(Retorno["CódigoUrl"], Retorno["Escritório"])
                if MsgRetorno == "CADASTRO FOI INTEGRADO":
                    self.printar_mensagens(f"Cadastro do cliente: {Cliente} foi integrado. Aguardando subir código.", "=", 30, "bot")
                else:
                    self.printar_mensagens(f"Cadastro do cliente: {Cliente} já estava integrado. Aguardando subir código.", "=", 30, "bot")
            else:
                self.printar_mensagens(f"Código do cliente: {Cliente} subiu. Alterando para ativo.", "=", 30, "bot")
                self.Controle["PEDIDOS"].range("G" + str(Linha)).value = StatusClienteNovo

        # ~~ Se status é "Expedido", remove valor da liberação do banco de dados e coleta NF e situação.
        if StatusNovo == "Expedido" or StatusNovo == "Expedido parcial":
            self.RemoverValorLiberadoDoControle(Pedido, True)
            ListaNfs = self.ColetarNfSap(Ordem)
            for Nf in ListaNfs:
                NfAtual = self.Controle["PEDIDOS"].range("AF" + str(Linha)).value
                SituaçãoAtual = self.Controle["PEDIDOS"].range("AG" + str(Linha)).value
                DataAtual = self.Controle["PEDIDOS"].range("AH" + str(Linha)).value
                if NfAtual == "-":
                    self.Controle["PEDIDOS"].range("AG" + str(Linha)).value = Nf["NF"]
                    self.Controle["PEDIDOS"].range("AH" + str(Linha)).value = Nf["Situação"]
                    self.Controle["PEDIDOS"].range("AI" + str(Linha)).value = datetime.strptime(Nf["Data"], "%d/%m/%Y")
                else:
                    self.Controle["PEDIDOS"].range("AG" + str(Linha)).value = NfAtual + " || " + Nf["NF"]
                    self.Controle["PEDIDOS"].range("AH" + str(Linha)).value = SituaçãoAtual + " || " + Nf["Situação"]
                    self.Controle["PEDIDOS"].range("AI" + str(Linha)).value = datetime.strftime(DataAtual, "%d/%m/%Y") + " || " + datetime.strptime(Nf["Data"], "%d/%m/%Y").strftime( "%d/%m/%Y")

            # ~~ Verifica se for ordem mista se ambos foram faturados.
            NfAtual = self.Controle["PEDIDOS"].range("AG" + str(Linha)).value
            if "||" in NfAtual:
                NfAtual = "MISTO"
            else:
                NfAtual = "ÚNICO"
            if Centros == "MISTO" and NfAtual == "ÚNICO":
                self.Controle["PEDIDOS"].range("M" + str(Linha)).value = "Expedido parcial"
            if Centros == "ÚNICO" and NfAtual == "ÚNICO" or Centros == "MISTO" and NfAtual == "MISTO":
                self.Controle["PEDIDOS"].range("M" + str(Linha)).value = "Expedido"

        # ~~ Se status é "Cancelado pela positivo", remove valor da liberação do banco de dados.
        if StatusNovo == "Cancelado pela positivo" and FrmPagamento == "Boleto a Prazo":
            self.RemoverValorLiberadoDoControle(Pedido, False)

        # ~~ Verifica se status está bugado no site.
        if StatusNovo in ["Pagamento aprovado", "Crédito aprovado"] and Ordem != "Ordem não integrada no SAP.":
            self.printar_mensagens(f"Pedido: {Pedido} está com o status errado. Iniciando atualização no site.", "=", 30, "bot")
            if Status == "Em separação":
                self.AlterarPedidoSite(Pedido, "Em separação")
                self.Controle["PEDIDOS"].range("M" + str(Linha)).value = "Em separação"
            else:
                self.AlterarPedidoSite(Pedido, "Pedido integrado")
                self.Controle["PEDIDOS"].range("L" + str(Linha)).value = "Pedido integrado"
            self.printar_mensagens("Status atualizado.", "=", 30, "bot")

# ================================================== #

# ~~ Módulo 2: Liberação de pedidos.
def LiberarPedidos(self) -> None:

    """
    Resumo:
    * Faz liberações ou recusas de crédito aos pedidos do site.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * None
    ---
    Erros:
    * Sem acesso à {Transação}. -> N2
    ---
    Níveis de erros tratados aqui:
    * N1
    """

    # ~~ Mensagem.
    self.printar_mensagens("Iniciando liberação de pedidos.", "=", 30, "bot")

    # ~~ For para checar linha a linha.
    for Linha in range(2, 99999):
        Pedido = self.Controle["PEDIDOS"].range("B" + str(Linha)).value
        Status = self.Controle["PEDIDOS"].range("M" + str(Linha)).value
        FormaPagamento = self.Controle["PEDIDOS"].range("C" + str(Linha)).value

        # ~~ Se pedido for nulo, é porque encerrou a lista de pedidos.
        if Pedido is None:
            self.printar_mensagens("Liberações de pedidos concluída.", "=", 30, "bot")
            return

        # ~~ Se status for "Pedido recebido" ou "Recusado pelo crédito".
        if Status not in ["Pedido recebido", "Recusado pelo crédito"] or FormaPagamento == "Boleto a Prazo Supplier":
            continue

        # ~~ Faz análise do pedido.
        Pedido = int(Pedido)
        self.printar_mensagens(f"Iniciando análise do pedido: {Pedido}.", "=", 30, "bot")
        try:
            Resposta = self.AnálisePedido(Pedido)
        except ErrosN1 as Erro:
            self.printar_mensagens(f"Ocorreu o seguinte erro na análise do pedido {Pedido}: {Erro.Message}", "=", 30, "bot")
            self.ImportarRespostaLiberação(Pedido, Erro.Message)
            self.Controle["PEDIDOS"].range("M" + str(Linha)).value = "Erro ao analisar crédito."
            continue

        # ~~ Insere dados de liberação na aba liberações.
        self.ImportarRespostaLiberação(Pedido, Resposta["MENSAGEM"])

        # ~~ Atualiza status no Controle.
        if Resposta["STATUS"] == "NÃO LIBERADO":	
            self.Controle["PEDIDOS"].range("M" + str(Linha)).value = "Recusado simbólico."
        else:
            self.Controle["PEDIDOS"].range("M" + str(Linha)).value = "Aprovado simbólico."

# ================================================== #

# ~~ Módulo 3: Pedidos parados na ZSD290.
def VerificarZSD290(self):

    """
    Resumo:
    * Verifica pedidos parados na ZSD290 e corrige eles se possível.
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * None
    ---
    Erros:
    * Sem acesso à {Transação}. -> N2
    ---
    Níveis de erros tratados aqui:
    * None
    """

    # ~~ Mensagens.
    self.printar_mensagens("Iniciando verificação de pedidos parados.", "=", 30, "bot")

    # ~~ For para checar linha a linha.
    for Linha in range(2, 99999):
        Pedido = self.Controle["PEDIDOS"].range("B" + str(Linha)).value
        Status = self.Controle["PEDIDOS"].range("M" + str(Linha)).value
        Ordem = self.Controle["PEDIDOS"].range("L" + str(Linha)).value

        # ~~ Se pedido for nulo, é porque encerrou a lista de pedidos.
        if Pedido is None:
            self.printar_mensagens("Verificação de pedidos parados concluída.", "=", 30, "bot")
            return

        # ~~ Converte pedido.
        Pedido = int(Pedido)

        # ~~ Se status for relevante e não possuir ordem ainda.
        if Status in ["Pagamento aprovado", "Crédito aprovado"] and Ordem == "Ordem não integrada no SAP.":
            self.printar_mensagens(f"Verificando possível trava do pedido: {Pedido}", "=", 30, "bot")

            # ~~ Verifica erro e corrige se possível.
            RetornoVerificação = self.VerificarPedidoParadoZSD290(Pedido)

            # ~~ Importa dados no Controle.
            if RetornoVerificação["CORRIGIDO?"] != "REPROCESSADO":
                self.ImportarDadosTravados(Pedido, RetornoVerificação["ERRO"], RetornoVerificação["CORRIGIDO?"])

# ================================================== #

# ~~ Módulo 4: Análise e correção de ordem.
def CorrigirOrdens(self) -> None:

    """
    Resumo:
    * Analisa e corrigem ordens que estão como "Pedido integrado".
    ---
    Parâmetros:
    * None
    ---
    Retorna:
    * None
    ---
    Erros:
    * Sem acesso à {Transação}. -> N2
    ---
    Níveis de erros tratados aqui:
    * N1
    """

    # ~~ Loop para checar linha a linha.
    self.printar_mensagens("Iniciando análise e correção de ordens.", "=", 30, "bot")
    for Linha in range(2, 99999):
        Pedido = self.Controle["PEDIDOS"].range("B" + str(Linha)).value
        Status = self.Controle["PEDIDOS"].range("M" + str(Linha)).value
        Ordem = self.Controle["PEDIDOS"].range("L" + str(Linha)).value

        # ~~ Se pedido for nulo, é porque encerrou a lista de pedidos.
        if Pedido is None:
            self.printar_mensagens("Análise e correção de ordens concluída.", "=", 30, "bot")
            return

        # ~~ Se status não for "Pedido integrado" prossegue.
        if Status != "Pedido integrado":
            continue

        # ~~ Começa análise.
        Pedido = int(Pedido)
        Ordem = int(Ordem)
        self.printar_mensagens(f"Iniciando análise e correção da ordem: {Ordem} referente pedido: {Pedido}.", "=", 30, "bot")
        try:
            DadosAnálise = self.AnáliseCorreçãoOrdem(Pedido)
        except ErrosN1 as Erro:
            self.printar_mensagens(f"Ocorreu o seguinte erro durante a correção da ordem: {Ordem} ({Pedido}): {Erro.Message}", "=", 30, "bot")
            self.Controle["PEDIDOS"].range("M" + str(Linha)).value = "Aguardando ajuste ordem."
            self.ImportarResumoCorreção(Pedido, Erro.Message, "Aguardando ajuste ordem.")
            continue

        # ~~ Se análise e correção for feita sem erros, insere "Aguardando liberação" na table Pedidos.
        self.Controle["PEDIDOS"].range("M" + str(Linha)).value = "Enviar para liberação."
        self.Controle["PEDIDOS"].range("N" + str(Linha)).value = DadosAnálise["StatusLiberação"]
        self.ImportarResumoCorreção(Pedido, DadosAnálise["Resumo"], "OK")

# ================================================== #