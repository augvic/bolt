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

# ~~ Imports.
import pandas
from datetime import datetime
from scripts.sap import Sap

# ================================================== #

# ~~ Classe Financeiro.
class Financeiro:

    """
    Resumo:
    - Controla tarefas relacionadas ao financeiro.

    Atributos:
    - (sap: Sap): Instância da classe "Sap".
    """

    # ================================================== #

    # ~~ Atributos.
    sap = None

    # ================================================== #

    # ~~ Armazena instância "Sap".
    def armazenar_sap(self, sap: Sap) -> None:

        """
        Resumo:
        - Armazena instância "Sap".

        Atributos:
        - (sap: Sap)
        """

        # ~~ Faz composição.
        self.sap = sap

    # ================================================== #

    # ~~ Coleta dados financeiros do cliente.
    def coletar_dados_financeiros_cliente(self, raiz_cnpj: str, printar_dados: str = False, log_path: str = None) -> dict:

        """
        Resumo:
        - Coleta dados financeiros do cliente: notas vencidas, valor em aberto, limite, vencimento e margem.
        
        Parâmetros:
        - (raiz_cnpj: str)
        - (printar_dados: bool | Opcional): Padrão é False. Passar True para printar dados.
        - (log_path (str | opcional): Caso passado um diretório, transfere texto printado para um arquivo ".txt".
        
        Retorna:
        - (dados: dict):
            - (nfs_vencidas):
                - (nfs_vencidas: str)
                - ("Sem vencidos.": str)
            - (em_aberto)
                - (em_aberto: float)
                - ("Sem valores em aberto.": str)
            - (limite):
                - (limite: float)
                - ("Sem limite ativo.": str)
            - (margem):
                - (margem: float)
                - ("Sem margem disponível.": str)
            - (vencimento):
                - (vencimento: datetime)
                - ("Sem limite ativo.": str)
            - (tabela_fbl5n):
                - (tabela_fbl5n: DataFrame)
                - ("Sem tabela FBL5N.": str)
        
        Exceções:
        - (SapVinculoError): Quando não há vínculo com SAP criado.
        - (SapTransacaoError): Quando não há acesso à transação.
        """

        # ~~ Cria dicionário novo para armazenar dados.
        dados = {}

        # ~~ Acessa transação FD33..
        self.sap.abrir_transacao("FD33")
        
        # ~~ Abre tela para colocar raiz do CNPJ.
        self.sap.session.findById("wnd[0]").sendVKey(4)
        self.sap.session.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006").select()

        # ~~ Itera raiz mais "i" até encontrar conta do cliente.
        i = 1
        while True:
            self.sap.session.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[0,24]").text = ""
            self.sap.session.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[0,24]").text = f"{raiz_cnpj}000{i}*"
            self.sap.session.findById("wnd[1]/tbar[0]/btn[0]").press()
            msg_bar = self.sap.session.findById("wnd[0]/sbar").text
            if "Nenhum valor para esta seleção" in msg_bar:
                i += 1
            else:
                break
        
        # ~~ Após achar conta, preenche restante dos campos.
        self.sap.session.findById("wnd[1]").sendVKey(2)
        self.sap.session.findById("wnd[0]/usr/ctxtRF02L-KKBER").text = "1000"
        self.sap.session.findById("wnd[0]/usr/chkRF02L-D0210").selected = True
        self.sap.session.findById("wnd[0]").sendVKey(0)

        # ~~ Coleta dados.
        limite = self.sap.session.findById("wnd[0]/usr/txtKNKK-KLIMK").text
        limite = limite.replace(".", "").replace(",", ".")
        limite = float(limite)
        vencimento = self.sap.session.findById("wnd[0]/usr/ctxtKNKK-NXTRV").text
        if not vencimento == "":
            vencimento = datetime.strptime(vencimento, "%d.%m.%Y").date()
        else:
            limite = 0.0
            vencimento = "Sem limite ativo."

        # ~~ Acessa transação FBL5N.
        abrir_transacao(self.sap.session=self.sap.session, transacao="FBL5N")

        # ~~ Preenche dados.
        self.sap.session.findById("wnd[0]/tbar[1]/btn[17]").press()
        self.sap.session.findById("wnd[1]/usr/txtENAME-LOW").text = "72776"
        self.sap.session.findById("wnd[1]/tbar[0]/btn[8]").press()
        self.sap.session.findById("wnd[0]").sendVKey(4)
        self.sap.session.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006").select()
        self.sap.session.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[0,24]").text = f"{raiz_cnpj}*"
        self.sap.session.findById("wnd[1]").sendVKey(0)

        # ~~ Coleta cada conta de acordo com a raiz do CNPJ.
        contas = []
        for linha in range(3, 50):
            try:
                conta = self.sap.session.findById(f"wnd[1]/usr/lbl[119,{linha}]").text
            except:
                continue
            if conta != "":
                contas.append(conta)
            else:
                break
        self.sap.session.findById("wnd[1]/tbar[0]/btn[0]").press()

        # ~~ Valores padrão para análise.
        frms_pagamentos = ["7", "2", "M", "G", "J", "Z", "V", "A", "P", "S", "*"]
        cnds_pagamentos = ["0001", "0002", "Z576", "Z577"]
        textos_ignorar = ["NEGOCIADO", "negociado", "CONCILIACAO", "conciliacao", "CONCILIAÇÃO", "conciliação", "CONCILIAÇÃO CR", "conciliação cr", "CONCILIACAO CR", "conciliacao cr",
                        "NAO COBRAR", "nao cobrar", "NÃO COBRAR", "não cobrar",
                        "EXTRAVIO", "extravio", "DEVOLUÇÃO", "devolução", "DEVOLUCAO", "devolucao", "EM DEVOLUCAO", "em devolucao", "EM DEVOLUÇÃO", "em devolução", "EM DEV", "em dev"]

        # ~~ Cria tabela para adicionar as partidas do cliente para depois criar um data frame.
        tabela = []

        # ~~ Define cada empresa para consultar as partidas.
        empresas = ["1000", "3500"]

        # ~~ Primeiro loop será para cada conta de cliente.
        for conta in contas:

            # ~~ Segundo loop será para cada conta de cliente em cada empresa.
            for empresa in empresas:

                # ~~ Preenche dados da transação.
                self.sap.session.findById("wnd[0]/usr/ctxtDD_KUNNR-LOW").text = conta
                self.sap.session.findById("wnd[0]/usr/ctxtDD_BUKRS-LOW").text = empresa
                self.sap.session.findById("wnd[0]/tbar[1]/btn[8]").press()
                msg_bar = self.sap.session.findById("wnd[0]/sbar").text
                
                # ~~ Valor padrão da forma de busca será "SCROLL".
                forma_busca = "SCROLL"

                # ~~ Se cliente tem partidas em aberto.
                if msg_bar not in ["Nenhuma partida selecionada (ver texto descritivo)", "Nenhuma conta preenche as condições de seleção"]:

                    # ~~ Verificando se forma de busca será por scroll na barra ou não.
                    for linha in range(10, 100):
                        try:
                            célula = self.sap.session.findById(f"wnd[0]/usr/lbl[0,{linha}]").text
                            if célula == " Cliente":
                                forma_busca = "ESTÁTICO"
                                break
                        except:
                            continue

                    # ~~ Define números iniciais das linhas.
                    linha_scroll = 0
                    linha = 10

                    # ~~ Loop para manter análise rodando até lista de partidas terminar.
                    while True:

                        # ~~ Se a forma de busca for "SCROLL", redefine a rolagem vertical para a linha atual. Se não for, sempre será 0 (padrão).
                        self.sap.session.findById("wnd[0]/usr").verticalScrollbar.position = linha_scroll

                        # ~~ Cria dicionário para armazenar as partidas.
                        tabela_dicionário = {}

                        # ~~ Try para ao terminar lista de partidas, ele dará erro, e com o erro sai do loop de coleta de partidas.
                        try:

                            # ~~ Verifica se são partidas em aberto, caso não, sai do loop.
                            situação = self.sap.session.findById(f"wnd[0]/usr/lbl[6,{linha}]").IconName
                            if situação != "S_LEDR":
                                self.sap.session.findById("wnd[0]").sendVKey(3)
                                break

                            # ~~ Verifica se há data de vencimento prorrogada no campo atribuição.
                            data_vencimento = self.sap.session.findById(f"wnd[0]/usr/lbl[9,{linha}]").text
                            data_vencimento = utilitarios.extrair_data_da_string(data_vencimento)

                            # ~~ Tenta converter para objeto datetime. Em caso de sucesso, é porque é uma data de prorrogação. 
                            try:
                                datetime.strptime(data_vencimento, "%d/%m/%Y")
                            
                            # ~~ Em caso de falha na conversão, não é prorrogação, então é considerado a data de vencimento padrão.
                            except:
                                data_vencimento = self.sap.session.findById(f"wnd[0]/usr/lbl[28,{linha}]").text
                                data_vencimento = str(data_vencimento).replace(".", "/")
                            
                            # ~~ Após verificar se há prorrogação ou não, verifica se data de vencimento está dentro da margem de 2 dias.
                            resultado = utilitarios.verificar_vencimento_boleto(data_vencimento)
                            if resultado == "Vencido":
                                situação = "Vencido"
                            else:
                                situação = "No prazo"
                            
                            # ~~ Coleta nº da NF.
                            nf = self.sap.session.findById(f"wnd[0]/usr/lbl[45,{linha}]").text

                            # ~~ Coleta os campos atribuição e texto e verifica se estão dentre os que devem ser ignorados para atualizar a situação.
                            atribuição = self.sap.session.findById(f"wnd[0]/usr/lbl[9,{linha}]").text
                            texto = self.sap.session.findById(f"wnd[0]/usr/lbl[81,{linha}]").text
                            if any(texto_procurado in atribuição for texto_procurado in textos_ignorar) or any(texto_procurado in texto for texto_procurado in textos_ignorar):
                                situação = "Outros"

                            # ~~ Coleta valor e verifica se o mesmo é crédito. Se for, atualiza a situação.
                            valor = self.sap.session.findById(f"wnd[0]/usr/lbl[62,{linha}]").text
                            valor = valor.replace(" ", "")
                            if valor.endswith("-"):
                                valor = "-" + valor[:-1]
                                situação = "Crédito"

                            # ~~ Coleta forma e condição de pagamento.
                            frm_pag = self.sap.session.findById(f"wnd[0]/usr/lbl[39,{linha}]").text
                            cond_pag = self.sap.session.findById(f"wnd[0]/usr/lbl[132,{linha}]").text

                            # ~~ Verifica se forma e condição estão na lista dos que devem ser ignorados.
                            if frm_pag in frms_pagamentos or cond_pag in cnds_pagamentos:

                                # ~~ Se não for crédito, ignora e continua loop.
                                if not situação == "Crédito":

                                    # ~~ Itera de acordo com a forma de busca definida acima.
                                    if forma_busca == "ESTÁTICO":
                                        linha += 1
                                    else:
                                        linha_scroll += 1
                                    continue

                            # ~~ Adiciona dados no dicionário.
                            tabela_dicionário["CONTA"] = conta
                            tabela_dicionário["SITUAÇÃO"] = situação
                            tabela_dicionário["FRM_PAGAMENTO"] = frm_pag
                            tabela_dicionário["CND_PAGAMENTO"] = cond_pag
                            tabela_dicionário["VENCIMENTO"] = data_vencimento
                            tabela_dicionário["NF"] = nf
                            tabela_dicionário["VALOR"] = valor

                            # ~~ Adiciona dicionário no array.
                            tabela.append(tabela_dicionário)
                        
                            # ~~ Itera de acordo com a forma de busca definida acima.
                            if forma_busca == "ESTÁTICO":
                                linha += 1
                            else:
                                linha_scroll += 1

                        # ~~ Quando lista terminar, dará erro, voltará para página inicial da FBL5N e sairá do loop.
                        except:
                            self.sap.session.findById("wnd[0]").sendVKey(3)
                            break

        # ~~ Cria um data frame das partidas, utilizando pandas.
        if tabela:
            df = pandas.DataFrame(tabela)

            # ~~ Remove espaços da coluna valor e converte para float.
            df["VALOR"] = df["VALOR"].str.replace(".", "").str.replace(",", ".")
            df["VALOR"] = df["VALOR"].astype(float)

            # ~~ Faz soma do total em aberto e adiciona no data frame.
            soma_total = df.loc[df["SITUAÇÃO"] != "Outros", "VALOR"].sum()
            em_aberto = float(soma_total)
            em_aberto_str = f"R$ {em_aberto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            df["VALOR"] = df["VALOR"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            nova_linha = pandas.DataFrame({"CONTA": [""], "SITUAÇÃO": [""], "FRM_PAGAMENTO": [""], "CND_PAGAMENTO": [""], "VENCIMENTO": [""], "NF": ["TOTAL"], "VALOR": [em_aberto_str]})
            df = pandas.concat([df, nova_linha])

            # ~~ Verifica quais partidas estão vencidas para adicionar numa lista.
            nfs_vencidas = ""
            total_linhas = df.shape[0]
            for linha in range(0, total_linhas):
                if df.iloc[linha]["SITUAÇÃO"] == "Vencido":
                    if nfs_vencidas == "":
                        nfs_vencidas += df.iloc[linha]["NF"]
                    else:
                        nfs_vencidas += " | " + df.iloc[linha]["NF"]
            if nfs_vencidas == "":
                nfs_vencidas = "Sem vencidos."

        # ~~ Se não consegue criar data frame, é porque cliente não possui nada em aberto.
        else:
            nfs_vencidas = "Sem vencidos."
            em_aberto = 0.0

        # ~~ Calcula margem.
        margem = limite - em_aberto

        # ~~ Após calcular margem, converte variáveis de limite, vencimento, em_aberto e margem, caso não haja limite ativo ou nada em aberto.
        if limite == 0.0 or vencimento == "Sem limite ativo.":
            limite = "Sem limite ativo."
            vencimento = "Sem limite ativo."
        if em_aberto == 0.0:
            em_aberto = "Sem valores em aberto."
        if margem <= 0.0:
            margem = "Sem margem disponível."

        # ~~ Adiciona tudo no dicionário.
        dados["nfs_vencidas"] = nfs_vencidas
        dados["em_aberto"] = em_aberto
        dados["limite"] = limite
        dados["margem"] = margem
        dados["vencimento"] = vencimento
        if tabela:
            dados["tabela_fbl5n"] = df
        else:
            dados["tabela_fbl5n"] = "Sem tabela FBL5N."

        # ~~ Printa dados. 
        if printar_dados == True:

            # ~~ Configura pandas para printar todas as linhas.
            pandas.set_option("display.max_rows", None)

            # ~~ Printa dados.
            utilitarios.printar_mensagem(mostrar_data_hora="Only", log_path=log_path)
            if isinstance(dados["tabela_fbl5n"], pandas.DataFrame):
                utilitarios.printar_dataframe(df=dados["tabela_fbl5n"], log_path=log_path)
                utilitarios.printar_mensagem(char_type="=", char_qtd=50, log_path=log_path)
                utilitarios.printar_mensagem(mostrar_data_hora="Only", log_path=log_path)
            if "Sem limite ativo." in [dados["limite"], dados["vencimento"]]:
                utilitarios.printar_mensagem(mensagem="Sem limite ativo. Margem indisponível.", mostrar_data_hora="False", log_path=log_path)
            else:
                utilitarios.printar_mensagem(mensagem=f"Vencimento do limite: {datetime.strftime(dados["vencimento"], "%d/%m/%Y")}", mostrar_data_hora="False", log_path=log_path)
                utilitarios.printar_mensagem(mensagem=f"Limite: {f"R$ {dados["limite"]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}", mostrar_data_hora="False", log_path=log_path)
            if dados["em_aberto"] == "Sem valores em aberto.":
                utilitarios.printar_mensagem(mensagem="Sem valores em aberto.", mostrar_data_hora="False", log_path=log_path)
            else:
                utilitarios.printar_mensagem(mensagem=f"Valor total em aberto: {f"R$ {dados["em_aberto"]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}", mostrar_data_hora="False", log_path=log_path)
            if dados["margem"] != "Sem margem disponível.":
                utilitarios.printar_mensagem(mensagem=f"Margem: {f"R$ {dados["margem"]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}", mostrar_data_hora="False", log_path=log_path)
            if dados["nfs_vencidas"] == "Sem vencidos.":
                utilitarios.printar_mensagem(mensagem="Sem vencidos.", char_type="=", char_qtd=50, char_side="bot", mostrar_data_hora="False", log_path=log_path)
            else:
                utilitarios.printar_mensagem(mensagem=f"Notas vencidas: {dados["nfs_vencidas"]}", char_type="=", char_qtd=50, char_side="bot", mostrar_data_hora="False", log_path=log_path)

        # ~~ Retorna.
        return dados

    # ================================================== #

# ================================================== #