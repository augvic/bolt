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