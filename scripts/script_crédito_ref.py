# ================================================== #

# ~~ Faz análise de crédito do pedido.
def análise_crédito_pedido(self, pedido: int, raiz_cnpj: int, valor: float) -> dict:

    """
    Resumo:
    * Faz análise de crédito do pedido.
    
    Parâmetros:
    * pedido: int -> Nº do pedido.
    * raiz_cnpj: int -> Raiz do CNPJ.
    * valor: float -> valor do pedido.
    
    Retorna:
    * resposta_análise -> Dicionário contendo: ["mensagem"] - ["status"].
    
    Erros:
    * ===
    
    Erros tratados localmente:
    * ===
    
    Erros levantados:
    * ===
    """

    # ~~ Cria dicionário para os dados da análise.
    resposta_análise = {}

    # ~~ Coleta dados financeiros do cliente.
    dados_financeiros = self.coletar_dados_financeiros(raiz_cnpj = raiz_cnpj)

    # ~~ Organiza dados para análise.
    cliente = str(raiz_cnpj)
    data_atual = datetime.now().date()
    vencimento = dados_financeiros["vencimento"] 
    limite = dados_financeiros["limite"]
    nfs_vencidas = dados_financeiros["nfs_vencidas"]
    em_aberto = dados_financeiros["em_aberto"]
    valor_pedidopedido = valor
    valor_pedido_str = f"R$ {valor_pedidopedido:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # ~~ Printa valor do pedido.
    self.printar_mensagem(f"valor do pedido: {valor_pedido_str}", "=", 30, "bot")

    # ~~ Converte vencimento de datetime para string.
    if vencimento == "-":
        vencimento_str = "-"
    else:
        vencimento_str = datetime.strftime(vencimento, "%d/%m/%Y")

    # ~~ Importa dados financeiros do cliente no controle.
    self.importar_dados_financeiros(cliente, vencimento, limite, em_aberto)

    # ~~ Verifica margem.
    margem = self.coletar_margem(cliente)
    margem = round(margem, 2)
    margem_str = f"R$ {margem:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    self.printar_mensagem(f"margem: {margem_str}", "=", 30, "bot")

    # ~~ Inicia análise.
    limite_ativo = True
    motivos = ""
    status = "LIBERADO"

    # ~~ Verifica se possui limite ativo.
    if limite == 0.0 or vencimento == "-":
        motivos += "\n- Sem limite de crédito ativo."
        status = "NÃO LIBERADO"
        limite_ativo = False

    # ~~ Verifica vencimento do limite.
    elif vencimento < data_atual:
        motivos += f"\n- limite vencido em {vencimento_str}."
        status = "NÃO LIBERADO"
        limite_ativo = False

    # ~~ Verifica se pedido está dentro da margem.
    if limite_ativo == True:
        if margem < valor_pedidopedido:
            motivos += f"\n- valor do pedido excede a margem disponível. valor do pedido: {valor_pedido_str} / margem livre: {margem_str}."
            status = "NÃO LIBERADO"

    # ~~ Verifica se possui notas vencidas.
    if nfs_vencidas != "":
        motivos += f"\n- Possui vencidos: {nfs_vencidas}."
        status = "NÃO LIBERADO"

    # ~~ Verifica se pode ser liberado. Se puder, importa seus dados no controle.
    if status == "LIBERADO":
        resposta_análise["mensagem"] = f"pedido {pedido} liberado."
        resposta_análise["status"] = "LIBERADO"
        self.importar_dados_financeiros(cliente = cliente, pedido = pedido, valor_pedidopedido = valor_pedidopedido)
    else:
        resposta_análise["mensagem"] = f"pedido {pedido} recusado:{motivos}"
        resposta_análise["status"] = "NÃO LIBERADO"

    # ~~ Retorna com dados de liberação.
    self.printar_mensagem(resposta_análise["mensagem"], "=", 30, "bot")
    return resposta_análise

# ================================================== #

# ~~ Função que fica em loop coletando pedidos e fazendo análises de crédito.
def loop(self) -> None:

    """
    Resumo:
    * Função que fica em loop coletando pedidos e fazendo análises de crédito.
    
    Parâmetros:
    * ===
    
    Retorna:
    * ===
    
    Erros:
    * Exception
    
    Erros tratados localmente:
    * Exception
    
    Erros levantados:
    * ===
    """

    # ~~ Loop while true, para manter automação funcionando.
    while True:

        # ~~ Bloco try-except para automação se auto reiniciar em caso de erros.
        try:

            # ~~ Cria loop para verificar linha a linha.
            for linha in range(2, 999999):

                # ~~ Verifica se foi alterado o encerramento global.
                if self.encerrar == True:
                    self.encerrarRPA()

                # ~~ Coleta nº do pedido.
                pedido = self.controle["PEDIDOS"].range("A" + str(linha)).value
                primeiro_pedido = self.controle["PEDIDOS"].range("B2").value

                # ~~ Se pedido for nulo, verifica se há novas inputações no site.
                if pedido is None or primeiro_pedido is None:

                    # ~~ Verifica se existe um primeiro pedido para verificar. Se existe, pega último pedido no controle + 1.
                    if primeiro_pedido is not None:
                        pedido = int(self.controle["PEDIDOS"].range("A" + str(linha - 1)).value)
                        pedido = pedido + 1
                    else:
                        pedido = int(pedido)

                    # ~~ Coleta dados do pedido no site.
                    dados_pedido = self.coletar_dados_pedido(pedido)

                    # ~~ Se não há inputação nova de pedido, reinicia loop.
                    if self.reiniciar_loop == True:
                        self.reiniciar_loop = False
                        break

                    # ~~ Insere dados no controle.
                    self.printar_mensagem(f"Inserindo dados do pedido {dados_pedido["pedido"]} no controle.", "=", 30, "bot")
                    self.controle["PEDIDOS"].range("A" + str(linha)).value = dados_pedido["pedido"]
                    self.controle["PEDIDOS"].range("B" + str(linha)).value = dados_pedido["Data"]
                    self.controle["PEDIDOS"].range("C" + str(linha)).value = dados_pedido["CondiçãoPagamento"]
                    self.controle["PEDIDOS"].range("D" + str(linha)).value = dados_pedido["vendedor"]
                    self.controle["PEDIDOS"].range("E" + str(linha)).value = dados_pedido["Razão"]
                    self.controle["PEDIDOS"].range("F" + str(linha)).value = dados_pedido["CNPJCliente"]
                    self.controle["PEDIDOS"].range("G" + str(linha)).value = dados_pedido["valor_pedido"]
                    self.controle["PEDIDOS"].range("H" + str(linha)).value = dados_pedido["status"]
                    self.controle["PEDIDOS"].range("I" + str(linha)).value = "-"
                    self.controle["PEDIDOS"].range("J" + str(linha)).value = "-"
                    self.controle["PEDIDOS"].range("K" + str(linha)).value = "-"

                # ~~ Coleta dados do pedido relevantes para análise de crédito.
                pedido = int(self.controle["PEDIDOS"].range("A" + str(linha)).value)
                data_pedido = self.controle["PEDIDOS"].range("B" + str(linha)).value
                vendedor = str(self.controle["PEDIDOS"].range("D" + str(linha)).value)
                raiz_cnpj = str(self.controle["PEDIDOS"].range("F" + str(linha)).value)
                valor_pedido = float(self.controle["PEDIDOS"].range("G" + str(linha)).value)
                status = str(self.controle["PEDIDOS"].range("H" + str(linha)).value)
                email = str(self.controle["PEDIDOS"].range("K" + str(linha)).value)

                # ~~ Se status for "LIBERADO".
                if status == "LIBERADO":

                    # ~~ Verifica se houve atualização de status para "FATURADO" ou "CANCELADO".
                    self.printar_mensagem(f"Verificando se houve atualização de status do pedido {pedido}.", "=", 30, "bot")
                    self.acessar_pedido(pedido)
                    status_novo = self.coletar_status_pedido()

                    # ~~ Se status novo for "FATURADO", adiciona valor de liberação ao em aberto do cliente.
                    if status_novo == "FATURADO":
                        self.printar_mensagem(f"status do {pedido} atualizado: {status} => {status_novo}.", "=", 30, "bot")
                        self.controle["PEDIDOS"].range("H" + str(linha)).value = status_novo
                        self.remover_valor_liberado(pedido = pedido, adicionar_em_aberto = True)

                    # ~~ Se status novo for "CANCELADO", remove valor de liberação do pedido.
                    elif status_novo == "CANCELADO":
                        self.printar_mensagem(f"status do {pedido} atualizado: {status} => {status_novo}.", "=", 30, "bot")
                        self.controle["PEDIDOS"].range("H" + str(linha)).value = status_novo
                        self.remover_valor_liberado(pedido = pedido, adicionar_em_aberto = False)

                    # ~~ Se não houve atualização de status.
                    else:
                        self.printar_mensagem(f"pedido {pedido} sem atualização de status.", "=", 30, "bot")

                # ~~ Se status for "RECEBIDO".
                if status == "RECEBIDO":

                    # ~~ Verifica se houve atualização de status para "CANCELADO".
                    self.printar_mensagem(f"Verificando se houve atualização de status do pedido {pedido}.", "=", 30, "bot")
                    self.acessar_pedido(pedido)
                    status_novo = self.coletar_status_pedido()

                    # ~~ Se status tiver atualizado para "CANCELADO", atualiza controle.
                    if status_novo == "CANCELADO":
                        self.printar_mensagem(f"status do {pedido} atualizado para {status_novo}.", "=", 30, "bot")
                        self.controle["PEDIDOS"].range("H" + str(linha)).value = status_novo

                    # ~~ Se não houve atualização de status, faz análise.
                    else:
                        self.printar_mensagem(f"Iniciando análise do pedido {pedido}. Possui status {status}.", "=", 30, "bot")
                        resposta_análise = self.análise_crédito_pedido(pedido = pedido, raiz_cnpj = raiz_cnpj, valor = valor_pedido)
                        self.controle["PEDIDOS"].range("I" + str(linha)).value = resposta_análise["mensagem"]
                        self.controle["PEDIDOS"].range("J" + str(linha)).value = datetime.now()

                        # ~~ Verifica resposta de liberação e atualiza status no controle e no site.
                        if resposta_análise["STATUS"] == "NÃO LIBERADO":
                            self.alterar_pedido_site(pedido = pedido, alterar_status = "Recusado pelo crédito", observação_interna = resposta_análise["mensagem"])
                            self.controle["PEDIDOS"].range("H" + str(linha)).value = "RECUSADO"
                        else:
                            self.alterar_pedido_site(pedido = pedido, alterar_status = "Crédito aprovado", observação_interna = resposta_análise["mensagem"])
                            self.controle["PEDIDOS"].range("H" + str(linha)).value = "LIBERADO"

                # ~~ Se status for "RECUSADO".
                if status == "RECUSADO":

                    # ~~ Verifica se houve atualização de status para "CANCELADO".
                    self.printar_mensagem(f"Verificando se houve atualização de status do pedido {pedido}.", "=", 30, "bot")
                    self.acessar_pedido(pedido)
                    status_novo = self.coletar_status_pedido()

                    # ~~ Se status tiver atualizado para "CANCELADO", atualiza controle.
                    if status_novo == "CANCELADO":
                        self.printar_mensagem(f"status do {pedido} atualizado para {status_novo}.", "=", 30, "bot")
                        self.controle["PEDIDOS"].range("H" + str(linha)).value = status_novo

                    # ~~ Se não houve atualização de status, faz reanálise.
                    else:
                        self.printar_mensagem(f"Iniciando reanálise do pedido {pedido}. status continua como {status}.", "=", 30, "bot")
                        resposta_análise = self.análise_crédito_pedido(pedido = pedido, raiz_cnpj = raiz_cnpj, valor = valor_pedido)
                        self.controle["PEDIDOS"].range("I" + str(linha)).value = resposta_análise["mensagem"]
                        self.controle["PEDIDOS"].range("J" + str(linha)).value = datetime.now()

                        # ~~ Verifica resposta de liberação e atualiza status no controle e no site.
                        if resposta_análise["STATUS"] == "NÃO LIBERADO":
                            self.alterar_pedido_site(pedido = pedido, observação_interna = resposta_análise["mensagem"])
                            self.controle["PEDIDOS"].range("H" + str(linha)).value = "RECUSADO"
                        else:
                            self.alterar_pedido_site(pedido = pedido, alterar_status = "Crédito aprovado", observação_interna = resposta_análise["mensagem"])
                            self.controle["PEDIDOS"].range("H" + str(linha)).value = "LIBERADO"

        # ~~ Se der erro, printa ele, espera 1m e reinicia loop.
        except Exception as erro:
            self.printar_mensagem(f"Ocorreu o seguinte erro na execução: {erro}. Aguardando 1m para reinício.", "=", 30, "bot")
            time.sleep(60)

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

    # ~~ Encerra instância driver.
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
    self.printar_mensagem("Encerrando execução do RPA...", "=", 30, "bot")
    self.exportar_log()
    exit()

# ================================================== #

# ~~ Exporta log.
def exportar_log(self) -> None:

    """
    Resumo:
    * Exporta log do terminal em ".txt".
    
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

    # ~~ Pega data e hora atual para nomear arquivo.
    data_hora_fim = datetime.now().replace(microsecond = 0)
    data_hora_fim = data_hora_fim.strftime("%d-%m-%Y_%H-%M")

    # ~~ Path da pasta logs.
    caminho_script = os.path.abspath(__file__)
    caminho_logs = caminho_script.split(r"script_crédito.py")[0] + r"\logs"

    # ~~ Exporta Log.
    with open(fr"{caminho_logs}\{self.data_hora_início} & {data_hora_fim}.txt", "w", encoding = "utf-8") as log_file:
        log_file.write(self.log)

# ================================================== #

# ~~ Printa mensagem ASCII.
def printar_ascii(self) -> None:

    """
    Resumo:
    * Printa mensagem ASCII inicial.
    
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

    # ~~ Mensagem ASCII.
    ascii_1 =  r"""#########################################################"""
    ascii_2 =  r"""#                                                       #"""
    ascii_3 =  r"""#  ____  ____   _       ____       __     _ _ _         #"""
    ascii_4 =  r"""# |  _ \|  _ \ / \     / ___|_ __ /_/  __| (_) |_ ___   #"""
    ascii_5 =  r"""# | |_) | |_) / _ \   | |   | '__/ _ \/ _` | | __/ _ \  #"""
    ascii_6 =  r"""# |  _ <|  __/ ___ \  | |___| | |  __/ (_| | | || (_) | #"""
    ascii_7 =  r"""# |_| \_\_| /_/   \_\  \____|_|  \___|\__,_|_|\__\___/  #"""
    ascii_8 =  r"""#                                                       #"""
    ascii_9 =  r"""#########################################################"""
    ascii_completo = f"{ascii_1}\n{ascii_2}\n{ascii_3}\n{ascii_4}\n{ascii_5}\n{ascii_6}\n{ascii_7}\n{ascii_8}\n{ascii_9}"

    # ~~ Printa.
    self.printar_mensagem(ascii_completo, "=", 30, "bot")

# ================================================== #

# ~~ Inicia RPA.
def iniciar_rpa(self) -> None

    """
    Resumo:
    * Inicia RPA.
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

    # ~~ Printa printar_ascii.
    self.printar_ascii()

    # ~~ Cria instâncias.
    self.session = self.instanciar_sap()
    self.driver = self.instanciar_navegador()
    self.controle = self.instanciar_controle()

    # ~~ Inicia loop do RPA.
    self.loop()

# ================================================== #

# ~~ Monitora o encerramento do RPA.
def monitorar_encerramento(self) -> None:

    """
    Resumo:
    * Monitora o encerramento do RPA ao pressionar CTRL + F12.
    
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

    # ~~ Mantém o script em execução, aguardando o pressionamento da tecla.
    while not self.encerrar == True:

        # ~~ Time sleep para reduzir uso de CPU.
        time.sleep(0.5)

        # ~~ Se pressionado "CTRL+F12", inicia encerramento.
        if keyboard.is_pressed("CTRL+F12"):
            self.DefinirEncerramento()

# ================================================== #

# ~~ Altera variável de encerramento global.
def DefinirEncerramento(self) -> None:

    """
    Resumo:
    * Altera variável de encerramento global.
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

    # ~~ Define encerramento global para True.
    self.encerrar = True

# ================================================== #

# ~~ Altera pedido no site.
def alterar_pedido_site(self, Pedido: int, AlterarStatus: str = None, observação_interna: str = None) -> None:

    """
    Resumo:
    * Altera pedido no site. Podendo alterar o status e inserir observação interna.
    ---
    Parâmetros:
    * Pedido -> Nº do pedido.
    * AlterarStatus -> Se passado algum status, altera para ele no site.
    * observação_interna -> Se passado alguma observação, insere ela nas observações do pedido.
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

    # ~~ Acessa página.
    self.acessar_pedido(Pedido)

    # ~~ Se for para alterar o status.
    if AlterarStatus is not None:

        # ~~ Encontra paineis e altera status em cada um.
        for i in range(1, 4):
            try: 
                StatusPedido = self.driver.find_element(By.NAME, value = f"distribution_centers[{i}][status]")
                StatusPedido = Select(StatusPedido)
                StatusPedido.select_by_visible_text(AlterarStatus)
            except:
                continue
    
    # ~~ Se for para inserir observação interna.
    if observação_interna is not None:
        CampoObservação = self.driver.find_element(By.ID, value = "comment")
        CampoObservação.clear()
        CampoObservação.send_keys(observação_interna)

    # ~~ Salva.
    botãoSalvar = self.driver.find_element(By.ID, value="save")
    botãoSalvar.click()

# ================================================== #