# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

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