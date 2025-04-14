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