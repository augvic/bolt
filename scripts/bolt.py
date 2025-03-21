# ================================================== #

# ~~ Bibliotecas.
import xlwings as xw
import time
import pandas as pd
import win32com.client
import pandas as pd
import os
import time
import requests
import urllib3
import unicodedata
import locale
import re
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By as By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as opt
from selenium.webdriver.support.ui import Select
from tabulate import tabulate
from dotenv import load_dotenv
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table

# ================================================== #

# ~~ Variáveis de ambiente.
load_dotenv()

# ================================================== #

# ~~ Cria instancia do Excel utilizando o xlwings.
def excel_instanciar(diretorio_planilha: str, abas: list) -> dict:

    """
    Resumo:
    - Cria instancia do Excel.
    
    Parâmetros:
    - diretorio_planilha (str)
    - abas (list): Lista contendo o nome de cada aba.
    
    Retorna:
    - planilha (dict):
        - ["BOOK"] (xw.Book): Chave vinculada diretamente à planilha.
        - [abas] (xw.sheets): Cada aba vinculada é uma chave.
    
    Exceções:
    - ===
    """

    # ~~ Dicionário para armazenar planilha e abas.
    planilha = {}

    # ~~ Armazena planilha.
    planilha["BOOK"] = xw.Book(diretorio_planilha)

    # ~~ Armazena abas.
    for aba in abas:
        planilha[aba] = planilha["BOOK"].sheets[aba]

    # ~~ Retorna planilha e abas.
    return planilha

# ================================================== #

# ~~ Insere dados na planilha.
def excel_inserir_dados(planilha: xw.Book, dado: any, aba_nome: str, coluna_nome: str, linha: int, linha_cabecalho: int) -> None:

    """
    Resumo:
    - Insere dados na planilha.
    
    Parâmetros:
    - planilha (xw.Book)
    - dado (any): Dado que será inserido na célula.
    - aba_nome (str): Nome da aba que será incluído o dado.
    - coluna_nome (str): Nome da coluna que será incluído o dado.
    - linha (int): Número da linha que será incluído o dado.
    - linha_cabecalho (int): Número da linha que está o cabeçalho (nome das colunas).
    
    Retorna:
    - ===
    
    Exceções:
    - "Coluna '{coluna_nome} não encontrada na aba '{aba_nome}'." 
    """

    # ~~ Cria lista de colunas de A à Z e depois concatena com outra lista de AA à AZ.
    letras = [chr(65 + i) for i in range(26)] + [f"A{chr(65 + i)}" for i in range(26)]

    # ~~ Cria dicionário com a chave sendo a "coluna" e o valor sendo a "letra".
    colunas = {
        planilha[aba_nome].range(f"{letra}{linha_cabecalho}").value: letra for letra in letras
    }

    # ~~ Coleta indice da coluna passado como parâmetro.
    coluna_a_ser_usada = colunas.get(coluna_nome)
    if not coluna_a_ser_usada:
        raise Exception(f"Coluna '{coluna_nome} não encontrada na aba '{aba_nome}'.")

    # ~~ Insere dado.
    planilha[aba_nome].range(f"{coluna_a_ser_usada}{linha}").value = dado

# ================================================== #

# ~~ Coleta dados da planilha.
def excel_coletar_dados(planilha: xw.Book, aba_nome: str, coluna_nome: str, linha: int, linha_cabecalho: int) -> any:

    """
    Resumo:
    - Coleta dados da planilha.
    
    Parâmetros:
    - planilha (xw.Book)
    - dado (any): Dado que será coletado da célula.
    - aba_nome (str): Nome da aba que será coletado o dado.
    - coluna_nome (str): Nome da coluna que será coletado o dado.
    - linha (int): Número da linha que será coletado o dado.
    - linha_cabecalho (int): Número da linha que está o cabeçalho (nome das colunas).
    
    Retorna:
    - dado (any): Pode ser str, int, float, datetime, etc.
    
    Exceções:
    - "Coluna '{coluna_nome} não encontrada na aba '{aba_nome}'."
    """

    # ~~ Cria lista de colunas de A à Z e depois concatena com outra lista de AA à AZ.
    letras = [chr(65 + i) for i in range(26)] + [f"A{chr(65 + i)}" for i in range(26)]

    # ~~ Cria dicionário com a chave sendo a "coluna" e o valor sendo a "letra".
    colunas = {
        planilha[aba_nome].range(f"{letra}{linha_cabecalho}").value: letra for letra in letras
    }

    # ~~ Coleta indice da coluna passado como parâmetro.
    coluna_a_ser_usada = colunas.get(coluna_nome)
    if not coluna_a_ser_usada:
        raise Exception(f"Coluna '{coluna_nome} não encontrada na aba '{aba_nome}'.")

    # ~~ Coleta dado.
    dado = planilha[aba_nome].range(f"{coluna_a_ser_usada}{linha}").value

    # ~~ Retorna dado.
    return dado

# ================================================== #

# ~~ Salva planilha.
def excel_salvar_planilha(planilha: xw.Book) -> None:

    """
    Resumo:
    - Salva a planilha.
    
    Parâmetros:
    - planilha (xw.Book)
    
    Retorna:
    - ===
    
    Exceções:
    - "Erro ao salvar planilha."
    """

    # ~~ Tenta salvar até 10x.
    tentativa = 0
    while tentativa != 10:
        try:
            planilha["BOOK"].save()
            return
        except:
            tentativa += 1
            time.sleep(2)
    
    # ~~ Se chegou ao limite de tentativas, exibe erro.
    if tentativa == 10:
        raise Exception("Erro ao salvar planilha.")

# ================================================== #

# ~~ Coleta última linha preenchida na coluna.
def excel_ultima_linha_preenchida(planilha: xw.Book, aba: str, coluna: str) -> int:

    """
    Resumo:
    - Retorna última linha preenchida na coluna.

    Parâmetros:
    - planilha (xw.Book)
    - aba (str)
    - coluna (str): "A", "B", "C", etc.
    
    Retorna:
    - ultima_linha (int)

    Exceções:
    - ===
    """

    # ~~ Coleta última linha.
    ultima_linha = planilha[aba].range(coluna + str("99999")).end("up").row

    # ~~ Retorna.
    return ultima_linha

# ================================================== #

# ~~ Utiliza pandas para ler planilha e localizar o index de um dado.
def pandas_localizar_index(df: pd.DataFrame, coluna_nome: str, localizar: str, linha_cabecalho: int) -> list:

    """
    Resumo:
    - Utiliza pandas para ler planilha e localizar o index de um dado.

    Parâmetros:
    - df (DataFrame)
    - coluna_nome (str): Nome da coluna onde irá ser procurado o dado.
    - localizar (str): Dado que será localizado.
    - linha_cabecalho (int): Linha que contém o cabeçalho na aba (nome das colunas).
    
    Retorna:
    - linhas (list): Números das linhas onde o dado foi localizado. Podendo ser uma ou mais.

    Exceções:
    - "Dado não localizado."
    """

    # ~~ Localiza dado.
    linhas = df.index[df[coluna_nome] == str(localizar)].tolist()

    # ~~ Se não localizar dado, retorna erro.
    if not linhas:
        raise Exception("Dado não localizado.")
    
    # ~~ Itera linhas do dataframe para corresponder as linhas da planilha.
    linhas = [linha + 1 + linha_cabecalho for linha in linhas]

    # ~~ Retorna números das linhas.
    return linhas

# ================================================== #

# ~~ Faz leitura de aba da planilha e salva como DataFrame.
def pandas_criar_df(diretorio_planilha: str, aba: str, linha_cabecalho: int, colunas_nomes: list = None) -> pd.DataFrame:

    """
    Resumo:
    - Faz leitura de aba da planilha e salva como DataFrame.

    Parâmetros:
    - diretorio_planilha (str)
    - aba (str): Nome da aba para ser transformada em DataFrame.
    - linha_cabecalho (int): Linha que contém o cabeçalho na aba (nome das colunas).
    - colunas_nomes (list | opcional): Se passado lista com nomes de colunas específicas, cria DataFrame apenas delas.
    
    Retorna:
    - df (DataFrame)

    Exceções:
    - ===
    """

    # ~~ Lê planilha e cria DataFrame.
    df = pd.read_excel(io=diretorio_planilha, sheet_name=aba, dtype=str, skiprows=linha_cabecalho-1, usecols=colunas_nomes)

    # ~~ Retorna DataFrame.
    return df

# ================================================== #

# ~~ Cria instância do SAP.
def sap_instanciar() -> object:

    """
    Resumo:
    - Cria instancia do SAP acessando a SAPScriptingEngine.
    
    Parâmetros:
    - ===
    
    Retorna:
    - sap (object): Vínculo com janela do SAP.
    
    Exceções:
    - "Não foi encontrado tela SAP disponível para conexão."
    """

    # ~~ Tenta conexão.
    try:
        gui = win32com.client.GetObject("SAPGUI")
        app = gui.GetScriptingEngine
        con = app.Children(0)
        for id in range(0, 4):
            sap = con.Children(id)
            if sap.ActiveWindow.Text == "SAP Easy Access":
                return sap
            else:
                continue

        # ~~ Se não encontrar tela disponível.
        else:
            raise Exception("Não foi encontrado tela SAP disponível para conexão.")
    
    # ~~ Se não encontrar tela logada no SAP.
    except:
        raise Exception("Não foi encontrado tela SAP disponível para conexão.")

# ================================================== #

# ~~ Abrir transação.
def sap_abrir_transacao(sap: object, transacao: str) -> None:

    """
    Resumo:
    - Abre transação no SAP.
    
    Parâmetros:
    - sap (object)
    - transação (str)
    
    Retorna:
    - ===
    
    Exceções:
    - "Sem acesso à {transação}."
    """

    # ~~ Acessa transação.
    sap.findById("wnd[0]/tbar[0]/okcd").text = "/N" + transacao
    sap.findById("wnd[0]").sendVKey(0)
    status_bar = None
    status_bar = sap.findById("wnd[0]/sbar").text
    if "Sem autorização" in status_bar:
        raise Exception(f"Sem acesso à {transacao}.")

# ================================================== #

# ~~ Coleta CNPJ do cliente da transação XD03.
def sap_coletar_cnpj_xd03(sap: object, codigo_erp: str) -> str:

    """
    Resumo:
    - Coleta CNPJ do cliente da transação XD03 e retorna.
    
    Parâmetros:
    - sap (object)
    - codigo_erp (str)
    
    Retorna:
    - cnpj (str)
    
    Exceções:
    - "Sem acesso à {Transação}."
    """

    # ~~ Abre transação XD03.
    sap_abrir_transacao(sap=sap, transacao="XD03")

    # ~~ Preenche dados e acessa conta.
    sap.findById("wnd[1]/usr/ctxtRF02D-KUNNR").text = codigo_erp
    sap.findById("wnd[1]/usr/ctxtRF02D-BUKRS").text = ""
    sap.findById("wnd[1]/usr/ctxtRF02D-VKORG").text = ""
    sap.findById("wnd[1]/usr/ctxtRF02D-VTWEG").text = ""
    sap.findById("wnd[1]/usr/ctxtRF02D-SPART").text = ""
    sap.findById("wnd[1]").sendVKey(0)

    # ~~ Acessa "dados de controle".
    sap.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02").select()

    # ~~ Coleta CNPJ e retorna.
    cnpj = sap.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02/ssubSUBSC:SAPLATAB:0200/subAREA3:SAPMF02D:7122/txtKNA1-STCD1").text
    return cnpj

# ================================================== #

# ~~ Coleta código ERP do cliente no SAP.
def sap_coletar_codigo_erp_xd03(sap: object, cnpj: str) -> str:

    """
    Resumo:
    - Coleta o código ERP do cliente no SAP.
    
    Parâmetros:
    - sap (object)
    - cnpj (str)
    
    Retorna:
    - codigo_erp (str)
    
    Exceções:
    - "CNPJ: {cnpj} não possui código ERP.": Cliente não tem cadastro no SAP.
    """

    # ~~ Acessa XD03.
    sap_abrir_transacao(sap=sap, transacao="XD03")

    # ~~ Busca pelo CNPJ.
    sap.findById("wnd[1]").sendVKey(4)
    sap.findById("wnd[2]/usr/tabsG_SELONETABSTRIP/tabpTAB006").select()
    sap.findById("wnd[2]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[0,24]").text = cnpj
    sap.findById("wnd[2]/tbar[0]/btn[0]").press()
    msg_bar = sap.findById("wnd[0]/sbar").text
    if "Nenhum valor para esta seleção" in msg_bar:
        sap.findById("wnd[1]").close()
        sap.findById("wnd[1]").close()
        raise Exception(f"CNPJ: {cnpj} não possui código ERP.")
    sap.findById("wnd[2]").sendVKey(2)

    # ~~ Coleta código ERP.
    codigo_erp = sap.findById("wnd[1]/usr/ctxtRF02D-KUNNR").text

    # ~~ Fecha transação.
    sap.findById("wnd[1]").close()

    # ~~ Retorna código ERP.
    return codigo_erp

# ================================================== #

# ~~ Coleta dados financeiros do cliente.
def sap_coletar_dados_financeiros_cliente(sap: object, raiz_cnpj: str, printar_dados: str = False, log_path: str = None) -> dict:

    """
    Resumo:
    - Coleta dados financeiros do cliente: notas vencidas, valor em aberto, limite, vencimento e margem.
    
    Parâmetros:
    - sap (object)
    - raiz_cnpj (str)
    - log_path (str | opcional): Caso passado um diretório, transfere texto printado para um arquivo ".txt". O parâmetro "printar_dados" deve ser True. 
    - printar_dados (bool | Opcional):
        - False: Padrão.
        - True: Printa todos os dados coletados. 
    
    Retorna:
    - dados (dict):
        - ["nfs_vencidas"] (str) ou (str: "Sem vencidos.")
        - ["em_aberto"] (float) ou (str: "Sem valores em aberto.")
        - ["limite"] (float) ou (str: "Sem limite ativo.")
        - ["margem"] (float) ou (str: "Sem margem disponível.")
        - ["vencimento"] (datetime) ou (str: "Sem limite ativo.")
        - ["tabela_fbl5n"] (DataFrame) ou (str: "Sem tabela FBL5N.")
    
    Exceções:
    - "Sem acesso à {Transação}."
    """

    # ~~ Cria dicionário novo para armazenar dados.
    dados = {}

    # ~~ Acessa transação FD33..
    sap_abrir_transacao(sap=sap, transacao="FD33")
    
    # ~~ Abre tela para colocar raiz do CNPJ.
    sap.findById("wnd[0]").sendVKey(4)
    sap.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006").select()

    # ~~ Itera raiz mais "i" até encontrar conta do cliente.
    i = 1
    while True:
        sap.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[0,24]").text = ""
        sap.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[0,24]").text = f"{raiz_cnpj}000{i}*"
        sap.findById("wnd[1]/tbar[0]/btn[0]").press()
        msg_bar = sap.findById("wnd[0]/sbar").text
        if "Nenhum valor para esta seleção" in msg_bar:
            i += 1
        else:
            break
    
    # ~~ Após achar conta, preenche restante dos campos.
    sap.findById("wnd[1]").sendVKey(2)
    sap.findById("wnd[0]/usr/ctxtRF02L-KKBER").text = "1000"
    sap.findById("wnd[0]/usr/chkRF02L-D0210").selected = True
    sap.findById("wnd[0]").sendVKey(0)

    # ~~ Coleta dados.
    limite = sap.findById("wnd[0]/usr/txtKNKK-KLIMK").text
    limite = limite.replace(".", "").replace(",", ".")
    limite = float(limite)
    vencimento = sap.findById("wnd[0]/usr/ctxtKNKK-NXTRV").text
    if not vencimento == "":
        vencimento = datetime.strptime(vencimento, "%d.%m.%Y").date()
    else:
        limite = 0.0
        vencimento = "Sem limite ativo."

    # ~~ Acessa transação FBL5N.
    sap_abrir_transacao(sap=sap, transacao="FBL5N")

    # ~~ Preenche dados.
    sap.findById("wnd[0]/tbar[1]/btn[17]").press()
    sap.findById("wnd[1]/usr/txtENAME-LOW").text = "72776"
    sap.findById("wnd[1]/tbar[0]/btn[8]").press()
    sap.findById("wnd[0]").sendVKey(4)
    sap.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006").select()
    sap.findById("wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[0,24]").text = f"{raiz_cnpj}*"
    sap.findById("wnd[1]").sendVKey(0)

    # ~~ Coleta cada conta de acordo com a raiz do CNPJ.
    contas = []
    for linha in range(3, 50):
        try:
            conta = sap.findById(f"wnd[1]/usr/lbl[119,{linha}]").text
        except:
            continue
        if conta != "":
            contas.append(conta)
        else:
            break
    sap.findById("wnd[1]/tbar[0]/btn[0]").press()

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
            sap.findById("wnd[0]/usr/ctxtDD_KUNNR-LOW").text = conta
            sap.findById("wnd[0]/usr/ctxtDD_BUKRS-LOW").text = empresa
            sap.findById("wnd[0]/tbar[1]/btn[8]").press()
            msg_bar = sap.findById("wnd[0]/sbar").text
            
            # ~~ Valor padrão da forma de busca será "SCROLL".
            forma_busca = "SCROLL"

            # ~~ Se cliente tem partidas em aberto.
            if msg_bar not in ["Nenhuma partida selecionada (ver texto descritivo)", "Nenhuma conta preenche as condições de seleção"]:

                # ~~ Verificando se forma de busca será por scroll na barra ou não.
                for linha in range(10, 100):
                    try:
                        célula = sap.findById(f"wnd[0]/usr/lbl[0,{linha}]").text
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
                    sap.findById("wnd[0]/usr").verticalScrollbar.position = linha_scroll

                    # ~~ Cria dicionário para armazenar as partidas.
                    tabela_dicionário = {}

                    # ~~ Try para ao terminar lista de partidas, ele dará erro, e com o erro sai do loop de coleta de partidas.
                    try:

                        # ~~ Verifica se são partidas em aberto, caso não, sai do loop.
                        situação = sap.findById(f"wnd[0]/usr/lbl[6,{linha}]").IconName
                        if situação != "S_LEDR":
                            sap.findById("wnd[0]").sendVKey(3)
                            break

                        # ~~ Verifica se há data de vencimento prorrogada no campo atribuição.
                        data_vencimento = sap.findById(f"wnd[0]/usr/lbl[9,{linha}]").text
                        data_vencimento = utilitarios_extrair_data(data_vencimento)

                        # ~~ Tenta converter para objeto datetime. Em caso de sucesso, é porque é uma data de prorrogação. 
                        try:
                            datetime.strptime(data_vencimento, "%d/%m/%Y")
                        
                        # ~~ Em caso de falha na conversão, não é prorrogação, então é considerado a data de vencimento padrão.
                        except:
                            data_vencimento = sap.findById(f"wnd[0]/usr/lbl[28,{linha}]").text
                            data_vencimento = str(data_vencimento).replace(".", "/")
                        
                        # ~~ Após verificar se há prorrogação ou não, verifica se data de vencimento está dentro da margem de 2 dias.
                        resultado = utilitarios_verificar_vencimento_boleto(data_vencimento)
                        if resultado == "Vencido":
                            situação = "Vencido"
                        else:
                            situação = "No prazo"
                        
                        # ~~ Coleta nº da NF.
                        nf = sap.findById(f"wnd[0]/usr/lbl[45,{linha}]").text

                        # ~~ Coleta os campos atribuição e texto e verifica se estão dentre os que devem ser ignorados para atualizar a situação.
                        atribuição = sap.findById(f"wnd[0]/usr/lbl[9,{linha}]").text
                        texto = sap.findById(f"wnd[0]/usr/lbl[81,{linha}]").text
                        if any(texto_procurado in atribuição for texto_procurado in textos_ignorar) or any(texto_procurado in texto for texto_procurado in textos_ignorar):
                            situação = "Outros"

                        # ~~ Coleta valor e verifica se o mesmo é crédito. Se for, atualiza a situação.
                        valor = sap.findById(f"wnd[0]/usr/lbl[62,{linha}]").text
                        valor = valor.replace(" ", "")
                        if valor.endswith("-"):
                            valor = "-" + valor[:-1]
                            situação = "Crédito"

                        # ~~ Coleta forma e condição de pagamento.
                        frm_pag = sap.findById(f"wnd[0]/usr/lbl[39,{linha}]").text
                        cond_pag = sap.findById(f"wnd[0]/usr/lbl[132,{linha}]").text

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
                        sap.findById("wnd[0]").sendVKey(3)
                        break

    # ~~ Cria um data frame das partidas, utilizando pandas.
    if tabela:
        df = pd.DataFrame(tabela)

        # ~~ Remove espaços da coluna valor e converte para float.
        df["VALOR"] = df["VALOR"].str.replace(".", "").str.replace(",", ".")
        df["VALOR"] = df["VALOR"].astype(float)

        # ~~ Faz soma do total em aberto e adiciona no data frame.
        soma_total = df.loc[df["SITUAÇÃO"] != "Outros", "VALOR"].sum()
        em_aberto = float(soma_total)
        em_aberto_str = f"R$ {em_aberto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        df["VALOR"] = df["VALOR"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        nova_linha = pd.DataFrame({"CONTA": [""], "SITUAÇÃO": [""], "FRM_PAGAMENTO": [""], "CND_PAGAMENTO": [""], "VENCIMENTO": [""], "NF": ["TOTAL"], "VALOR": [em_aberto_str]})
        df = pd.concat([df, nova_linha])

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
        pd.set_option("display.max_rows", None)

        # ~~ Printa dados.
        utilitarios_printar_mensagem(mostrar_data_hora="Only", log_path=log_path)
        if isinstance(dados["tabela_fbl5n"], pd.DataFrame):
            utilitarios_printar_dataframe(df=dados["tabela_fbl5n"], log_path=log_path)
            utilitarios_printar_mensagem(char_type="=", char_qtd=50, log_path=log_path)
            utilitarios_printar_mensagem(mostrar_data_hora="Only", log_path=log_path)
        if "Sem limite ativo." in [dados["limite"], dados["vencimento"]]:
            utilitarios_printar_mensagem(mensagem="Sem limite ativo. Margem indisponível.", mostrar_data_hora="False", log_path=log_path)
        else:
            utilitarios_printar_mensagem(mensagem=f"Vencimento do limite: {datetime.strftime(dados["vencimento"], "%d/%m/%Y")}", mostrar_data_hora="False", log_path=log_path)
            utilitarios_printar_mensagem(mensagem=f"Limite: {f"R$ {dados["limite"]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}", mostrar_data_hora="False", log_path=log_path)
        if dados["em_aberto"] == "Sem valores em aberto.":
            utilitarios_printar_mensagem(mensagem="Sem valores em aberto.", mostrar_data_hora="False", log_path=log_path)
        else:
            utilitarios_printar_mensagem(mensagem=f"Valor total em aberto: {f"R$ {dados["em_aberto"]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}", mostrar_data_hora="False", log_path=log_path)
        if dados["margem"] != "Sem margem disponível.":
            utilitarios_printar_mensagem(mensagem=f"Margem: {f"R$ {dados["margem"]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}", mostrar_data_hora="False", log_path=log_path)
        if dados["nfs_vencidas"] == "Sem vencidos.":
            utilitarios_printar_mensagem(mensagem="Sem vencidos.", char_type="=", char_qtd=50, char_side="bot", mostrar_data_hora="False", log_path=log_path)
        else:
            utilitarios_printar_mensagem(mensagem=f"Notas vencidas: {dados["nfs_vencidas"]}", char_type="=", char_qtd=50, char_side="bot", mostrar_data_hora="False", log_path=log_path)

    # ~~ Retorna.
    return dados

# ================================================== #

# ~~ Volta à tela inicial do SAP.
def sap_tela_inicial(sap: object) -> None:

    """
    Resumo:
    - Volta à tela inicial do SAP.
    
    Parâmetros:
    - sap (object)
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Encerra instância SAP.
    while True:
        if sap.ActiveWindow.Text == "SAP Easy Access":
            break
        else:
            try:
                sap.findById("wnd[1]").close()
            except:
                sap.findById("wnd[0]").sendVKey(3)

# ================================================== #

# ~~ Cria instância do navegador utilizando o webdriver.
def navegador_instanciar() -> webdriver.Chrome:

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

    # ~~ Diretório do profile.
    diretorio_profile = os.path.dirname(os.path.abspath(__file__))
    diretorio_profile = os.path.join(diretorio_profile, "profile")

    # ~~ Definindo configurações.
    options = opt()
    options.add_argument(f"user-data-dir={diretorio_profile}")
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
def navegador_acessar_godeep(driver: webdriver.Chrome) -> None:

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
        if any(login_string in body for login_string in ["Because you're accessing sensitive info, you need to verify your password.", "Sign in", "Pick an account"]):
            utilitarios_printar_mensagem(mostrar_data_hora="Only")
            input("Necessário logar conta Microsoft. Aperte ENTER aqui depois para continuar.")
            utilitarios_printar_mensagem(char_type="=", char_qtd=50)
        if "Approve sign in request" in body:
            time.sleep(3)
            codigo = driver.find_element(By.ID, value="idRichContext_DisplaySign").text
            utilitarios_printar_mensagem(mostrar_data_hora="Only")
            input(f"Necessário authenticator Microsoft para continuar: {codigo}. Aperte ENTER aqui depois para continuar.")
            utilitarios_printar_mensagem(char_type="=", char_qtd=50)
    except:
        driver.get(f"https://www.revendedorpositivo.com.br/admin/index/")

# ================================================== #

# ~~ Verifica status de assinatura de cliente na GoDeep.
def navegador_coletar_status_assinatura_godeep(driver: webdriver.Chrome, cnpj: str) -> str:

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
def navegador_fechar(driver: webdriver.Chrome) -> None:

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

# ~~ Acessa pedido no site.
def pedido_acessar(driver: webdriver.Chrome, pedido: int) -> None:

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
def pedido_coletar_data(driver: webdriver.Chrome) -> datetime:

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
def pedido_coletar_condição_pagamento(driver: webdriver.Chrome) -> str:

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
def pedido_coletar_forma_pagamento(driver: webdriver.Chrome) -> str:

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
def pedido_coletar_cnpj(driver: webdriver.Chrome) -> str:

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
def pedido_coletar_valor(driver: webdriver.Chrome) -> float:

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
def pedido_coletar_status(driver: webdriver.Chrome) -> str:

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
def pedido_coletar_razão_social(driver: webdriver.Chrome) -> str:

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
def pedido_coletar_código_erp(driver: webdriver.Chrome) -> str:

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
def pedido_coletar_vendedor(driver: webdriver.Chrome) -> str:

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
def pedido_coletar_escritório(vendedor: str) -> int:

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
    df = pandas_criar_df(diretorio_planilha=os.path.dirname(os.path.abspath(__file__)) + r"\comercial.xlsx", aba="COMERCIAL", linha_cabecalho=1, colunas_nomes=["NOME", "ESCRITÓRIO"])

    # ~~ Localiza vendedor.
    linha = df.index[df["NOME"] == str(vendedor)].tolist()

    # ~~ Coleta escritório.
    escritorio = df.iloc[linha]["ESCRITÓRIO"].values
    escritorio = int(escritorio)

    # ~~ Retorna escritório.
    return escritorio

# ================================================== #

# ~~ Coleta dados do pedido no site.
def pedido_coletar_dados_completos(driver: webdriver.Chrome, pedido: int) -> dict:

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
    pedido_acessar(driver=driver, pedido=pedido)

    # ~~ Coleta dados do pedido.
    dados_pedido["pedido"] = pedido
    dados_pedido["data"] = pedido_coletar_data(driver=driver)
    dados_pedido["forma_pagamento"] = pedido_coletar_forma_pagamento(driver=driver)
    dados_pedido["condição_pagamento"] = pedido_coletar_condição_pagamento(driver=driver)
    dados_pedido["razão_social"] = pedido_coletar_razão_social(driver=driver)
    dados_pedido["cnpj"] = pedido_coletar_cnpj(driver=driver)
    try:
        dados_pedido["código_erp"] = pedido_coletar_código_erp(driver=driver)
    except:
        dados_pedido["código_erp"] = "-"
    dados_pedido["valor_pedido"] = pedido_coletar_valor(driver=driver)
    dados_pedido["status"] = pedido_coletar_status(driver=driver)
    dados_pedido["vendedor"] = pedido_coletar_vendedor(driver=driver)

    # ~~ Retorna dados.
    return dados_pedido

# ================================================== #

# ~~ Função de consulta de dados da Receita Federal.
def utilitarios_consultar_receita_federal(cnpj: str, printar_dados: bool = False, log_path: str = None) -> dict:

    """
    Resumo:
    - Consulta a API da Receita Federal e obtém dados de um CNPJ.

    Parâmetros:
    - cnpj (str)
    - log_path (str | opcional): Caso passado um diretório, transfere texto printado para um arquivo ".txt". O parâmetro "printar_dados" deve ser True. 
    - printar_dados (bool):
        - False: Padrão.
        - True: Printa todos os dados.

    Retorna:
    - resposta_json (dict):
        - ["cnpj"] (str)
        - ["razao_social"] (str)
        - ["nome_fantasia"] (str) ou (str: "-")
        - ["natureza_juridica"] (str)
        - ["situacao_cadastral"] (str)
        - ["logradouro"] (str)
        - ["numero"] (str)
        - ["complemento"] (str) ou (str: "-")
        - ["bairro"] (str)
        - ["cep"] (str)
        - ["cidade"] (str)
        - ["estado"] (str): Estado em sigla.
        - ["telefone"] (str)
        - ["email"] (str) ou (str: "-")
        - ["recebimento_comissao"] (str):
            - "OK"
            - "NÃO OK"
        - ["regime_tributario"] (str):
            - "SIMPLES"
            - "LUCRO PRESUMIDO"
            - "LUCRO REAL"
        - ["inscricoes_estaduais"] (list) ou (str: "ISENTO"): Lista contendo todas as inscrições. Cada item possui as chaves:
            - ["inscricao_estadual"] (str)
            - ["situacao"] (str)
        - ["inscricoes_suframa"] (list) ou (str: "ISENTO"): Lista contendo todas as inscrições. Cada item possui as chaves:
            - ["inscricao_suframa"] (str)
            - ["situacao"] (str)
        - ["cnae"] (list): Lista contendo todos os CNAE. Cada item possui as chaves:
            - ["cnae"] (str)
            - ["descricao"] (str)

    Exceções:
    - "Erro na resposta da requisição.": Erro no retorno da requisição à API.
    - "Erro ao fazer requisição.": Erro a fazer requisição à API.
    """

    # Suprime avisos de SSL.
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # ~~ Url da API e autorização.
    url = f"https://comercial.cnpj.ws/cnpj/{cnpj}"
    headers = {
        "x_api_token": os.getenv("API_KEY")
    }

    # ~~ Requisição.
    try:
        resposta = requests.get(url=url, headers=headers, verify=False)
    except Exception as erro:
        raise Exception(f"Erro ao fazer requisição: {erro}.")

    # ~~ Verifica resposta.
    if resposta.status_code == 200:

        # ~~ Converte para JSON.
        resposta_json = resposta.json()

        # ~~ Cria dicionário para armazenar dados.
        dados = {}

        # ~~ Coleta CNPJ.
        dados["cnpj"] = resposta_json["estabelecimento"]["cnpj"]

        # ~~ Coleta razão social.
        dados["razao_social"] = utilitarios_formatar_texto(resposta_json["razao_social"])

        # ~~ Coleta nome fantasia.
        dados["nome_fantasia"] = utilitarios_formatar_texto(resposta_json["estabelecimento"]["nome_fantasia"]) if resposta_json["estabelecimento"]["nome_fantasia"] else "-"

        # ~~ Coleta natureza jurídica.
        dados["natureza_juridica"] = utilitarios_formatar_texto(resposta_json["natureza_juridica"]["descricao"])
        dados["natureza_juridica_id"] = resposta_json["natureza_juridica"]["id"]

        # ~~ Situação cadastral.
        dados["situacao_cadastral"] = utilitarios_formatar_texto(resposta_json["estabelecimento"]["situacao_cadastral"])

        # ~~ Coleta rua.
        dados["logradouro"] = utilitarios_formatar_texto(resposta_json["estabelecimento"]["logradouro"])

        # ~~ Coleta número.
        dados["numero"] = resposta_json["estabelecimento"]["numero"]

        # ~~ Coleta complemento.
        dados["complemento"] = re.sub(r"\s+", " ", utilitarios_formatar_texto(resposta_json["estabelecimento"]["complemento"])) if resposta_json["estabelecimento"]["complemento"] else "-"

        # ~~ Coleta bairro.
        dados["bairro"] = utilitarios_formatar_texto(resposta_json["estabelecimento"]["bairro"])

        # ~~ Coleta CEP.
        dados["cep"] = f"{resposta_json["estabelecimento"]["cep"][:5]}-{resposta_json["estabelecimento"]["cep"][5:]}"

        # ~~ Coleta cidade.
        dados["cidade"] = utilitarios_formatar_texto(resposta_json["estabelecimento"]["cidade"]["nome"])

        # ~~ Coleta sigla do estado.
        dados["estado"] = utilitarios_formatar_texto(resposta_json["estabelecimento"]["estado"]["sigla"])

        # ~~ Coleta telefone.
        dados["telefone"] = f"{resposta_json["estabelecimento"]["ddd1"]}{resposta_json["estabelecimento"]["telefone1"]}"

        # ~~ Coleta e-mail.
        dados["email"] = utilitarios_formatar_texto(resposta_json["estabelecimento"]["email"]) if resposta_json["estabelecimento"]["email"] else "-"

        # ~~ Coleta inscrições estaduais.
        dados["inscricoes_estaduais"] = [
            {
                "inscricao_estadual": inscricao["inscricao_estadual"],
                "situacao": "HABILITADA" if inscricao["ativo"] else "NÃO HABILITADA"
            }
            for inscricao in resposta_json["estabelecimento"]["inscricoes_estaduais"]
        ] if resposta_json["estabelecimento"]["inscricoes_estaduais"] else "ISENTO"

        # ~~ Coleta inscrições suframa.
        dados["inscricoes_suframa"] = [
            {
                "inscricao_suframa": inscricao["inscricao_suframa"],
                "situacao": "HABILITADA" if inscricao["ativo"] else "NÃO HABILITADA"
            }
            for inscricao in resposta_json["estabelecimento"]["inscricoes_suframa"]
        ] if resposta_json["estabelecimento"]["inscricoes_suframa"] else "ISENTO"

        # ~~ Coleta regime.
        try:
            regime = resposta_json["simples"]["simples"]
        except:
            regime = "Não"
        if regime == "Sim":
            dados["regime_tributario"] = {"regime_tributario": "SIMPLES"}
        else:
            dados["regime_tributario"] = [
                {
                    "ano": regime["ano"],
                    "regime_tributario": regime["regime_tributario"]
                }
                for regime in resposta_json["estabelecimento"]["regimes_tributarios"]
            ]
            dados["regime_tributario"] = max(dados["regime_tributario"], key=lambda x: x["ano"])
        
        # ~~ CNAE.
        dados["cnae"] = [
            {
                "cnae": cnae["classe"],
                "descricao": cnae["descricao"]
            }
            for cnae in resposta_json["estabelecimento"]["atividades_secundarias"]
        ]

        # ~~ Recebimento comissão.
        cnae_comissao = ["45.12-9", "45.30-7", "45.42-1", "46.11-7", "46.12-5", "46.13-3", "46.14-1", "46.15-0", "46.16-8", "46.17-6", "46.18-4", "46.19-2", "66.19-3"]
        dados["recebimento_comissao"] = "NÃO OK"
        for cnae in dados["cnae"]:
            if cnae["cnae"] in cnae_comissao:
                dados["recebimento_comissao"] = "OK"

        # ~~ Printa dados.
        if printar_dados == True:

            # ~~ Data e hora.
            utilitarios_printar_mensagem(mostrar_data_hora="Only", log_path=log_path)

            # ~~ Dados básicos.
            utilitarios_printar_mensagem(mensagem=f"CNPJ: {dados["cnpj"]}", mostrar_data_hora="False", log_path=log_path)
            utilitarios_printar_mensagem(mensagem=f"Razão Social: {dados["razao_social"]}", mostrar_data_hora="False", log_path=log_path)
            utilitarios_printar_mensagem(mensagem=f"Nome Fantasia: {dados["nome_fantasia"]}", mostrar_data_hora="False", log_path=log_path)
            utilitarios_printar_mensagem(mensagem=f"Natureza Jurídica: {dados["natureza_juridica_id"]} | {dados["natureza_juridica"]}", mostrar_data_hora="False", log_path=log_path)
            utilitarios_printar_mensagem(mensagem=f"Situação Cadastral: {dados["situacao_cadastral"]}", mostrar_data_hora="False", log_path=log_path)
            utilitarios_printar_mensagem(mensagem=f"Endereço Completo: {dados["logradouro"]}, {dados["numero"]} | {dados["complemento"]} | {dados["bairro"]} | {dados["cep"]} | {dados["cidade"]} | {dados["estado"]}", mostrar_data_hora="False", log_path=log_path)
            utilitarios_printar_mensagem(mensagem=f"Telefone: {dados["telefone"]}", mostrar_data_hora="False", log_path=log_path)
            utilitarios_printar_mensagem(mensagem=f"E-mail: {dados["email"]}", mostrar_data_hora="False", log_path=log_path)
            utilitarios_printar_mensagem(mensagem=f"Regime Tributário: {dados["regime_tributario"]["regime_tributario"]}", mostrar_data_hora="False", log_path=log_path)
            utilitarios_printar_mensagem(mensagem=f"Recebimento Comissão: {dados["recebimento_comissao"]}", mostrar_data_hora="False", log_path=log_path)

            # ~~ Inscrições estaduais.
            utilitarios_printar_mensagem(mensagem="Inscrições Estaduais:", mostrar_data_hora="False", log_path=log_path)
            if dados["inscricoes_estaduais"] != "ISENTO":
                for inscricao in dados["inscricoes_estaduais"]:
                    utilitarios_printar_mensagem(mensagem=f"    {inscricao["inscricao_estadual"]} | {inscricao["situacao"]}", mostrar_data_hora="False", log_path=log_path)
            else:
                utilitarios_printar_mensagem(mensagem=f"    {dados["inscricoes_estaduais"]}", mostrar_data_hora="False", log_path=log_path)

            # ~~ Inscrições suframa.
            utilitarios_printar_mensagem(mensagem="Inscrições Suframa:", mostrar_data_hora="False", log_path=log_path)
            if dados["inscricoes_suframa"] != "ISENTO":
                for inscricao in dados["inscricoes_suframa"]:
                    utilitarios_printar_mensagem(f"    {inscricao["inscricao_suframa"]} | {inscricao["situacao"]}", mostrar_data_hora="False", log_path=log_path)
            else:
                utilitarios_printar_mensagem(mensagem=f"    {dados["inscricoes_suframa"]}", mostrar_data_hora="False", log_path=log_path)

            # ~~ CNAE.
            utilitarios_printar_mensagem(mensagem="CNAE:", mostrar_data_hora="False", log_path=log_path)
            for cnae in dados["cnae"]:
                utilitarios_printar_mensagem(f"    {cnae["cnae"]} | {cnae["descricao"]}", mostrar_data_hora="False", log_path=log_path)

            # ~~ Fim.
            utilitarios_printar_mensagem(char_type="=", char_qtd=50)

        # ~~ Retorna dados.
        return dados
    
    # ~~ Em caso de de erro na resposta.
    else:
        utilitarios_printar_mensagem(mensagem=f"Erro: {resposta.status_code}", char_type="=", char_qtd=50, char_side="bot")
        raise Exception(f"Erro na resposta da requisição: {resposta.status_code} - {resposta.text}.")

# ================================================== #

# ~~ Verifica se data de boleto está vencido.
def utilitarios_verificar_vencimento_boleto(data_boleto: str) -> str:

    """
    Resumo:
    - Verifica se data de vencimento da nota está vencida ou não.
    
    Parâmetros:
    - data (str): Data para verificar se está vencida.
    
    Retorna:
    - resultado (str): Pode ser as opções abaixo. 
        - "Vencido"
        - "Não vencido"
    
    Exceções:
    - ===
    """

    # ~~ Converte data do boleto passada como parâmetro de "str" para "datetime".
    data_boleto = datetime.strptime(data_boleto, "%d/%m/%Y").date()

    # ~~ Coleta data atual.
    data_atual = datetime.now().date()

    # ~~ Verifica se data do boleto é menor que data atual. Se for menor, é vencido. Se for maior, não é.
    if data_boleto < data_atual:

        # ~~ Incrementa 1 dia a mais na "data_boleto" até ele chegar na data atual, ignorando sábados e domingos, contando há quantos dias está vencido.
        dias_vencidos = 0
        data_boleto = data_boleto + timedelta(days=1)
        while data_boleto < data_atual:
            if data_boleto.weekday() < 5:
                dias_vencidos += 1
            data_boleto = data_boleto + timedelta(days=1)

        # ~~ Se os dias vencidos forem iguais ou maior a 2, então o boleto está vencido de fato. Caso não, não é considerado vencido.
        if dias_vencidos >= 2:
            return "Vencido"
        else:
            return "Não vencido"
        
    # ~~ Caso a data do boleto seja maior que a data atual, não é vencido.
    else:
        return "Não vencido"

# ================================================== #

# ~~ Função customizada para printar mensagens.
def utilitarios_printar_mensagem(mensagem: str = None, char_type: str = None, char_qtd: int = None, char_side: str = None, log_path: str = None, mostrar_data_hora: str = "True") -> None:

    """
    Resumo:
    - Printa mensagem ou caractere especial no terminal.
    
    Parâmetros:
    - mensagem (str | opcional): Texto que será printado no terminal.
    - char_type: (str | opcional): Tipo de caractere a ser printado.
    - char_qtd: (int | opcional): Quantidade do caractere.
    - char_side: (str | opcional): Lado que será printado, podendo ser as opções abaixo.
        - "top": Cima
        - "bot": Baixo
        - "both": Ambos
    - log_path (str | opcional): Caso passado um diretório, transfere texto printado para um arquivo ".txt". 
    - mostar_data_hora (str | opcional): 
        - "True" Padrão
        - "False": Para não mostrar data e hora.
        - "Only": Para printar somente a data.
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Coleta data e hora atual.
    data_hora_atual = datetime.now().replace(microsecond = 0)
    data_hora_atual = data_hora_atual.strftime("%d/%m/%Y_%H:%M")

    # ~~ Se for para direcionar output à um arquivo ".txt".
    if log_path:
        log = open(log_path, "a", encoding="utf-8")

    # ~~ Se for somente para printar a data:
    if mostrar_data_hora == "Only":
        print(f"<{data_hora_atual}>")
        if log_path:
            log.write(f"<{data_hora_atual}>" + "\n")
        return

    # ~~ Se tiver mensagem.
    if mensagem:

        # ~~ Se tiver mensagem e char_type, verifica o lado a ser printado.
        if char_type:
            if char_side == "top":
                print(char_type*char_qtd)
                if mostrar_data_hora == "True":
                    print(f"<{data_hora_atual}>")
                print(mensagem)
                if log_path:
                    log.write(char_type*char_qtd + "\n")
                    if mostrar_data_hora == "True":
                        log.write(f"<{data_hora_atual}>" + "\n")
                    log.write(f"<{mensagem}>" + "\n")
            if char_side == "bot":
                if mostrar_data_hora == "True":
                    print(f"<{data_hora_atual}>")
                print(mensagem)
                print(char_type*char_qtd)
                if log_path:
                    if mostrar_data_hora == "True":
                        log.write(f"<{data_hora_atual}>" + "\n")
                    log.write(mensagem + "\n")
                    log.write(char_type*char_qtd + "\n")
            if char_side == "both":
                print(char_type*char_qtd)
                if mostrar_data_hora == "True":
                    print(f"<{data_hora_atual}>")
                print(mensagem)
                print(char_type*char_qtd)
                if log_path:
                    log.write(char_type*char_qtd + "\n")
                    if mostrar_data_hora == "True":
                        log.write(f"<{data_hora_atual}>" + "\n")
                    log.write(mensagem + "\n")
                    log.write(char_type*char_qtd + "\n")

        # ~~ Se não tiver char_type, printa somente mensagem.
        else:
            if mostrar_data_hora == "True":
                print(f"<{data_hora_atual}>")
            print(mensagem)
            if log_path:
                if mostrar_data_hora == "True":
                    log.write(f"<{data_hora_atual}>" + "\n")
                log.write(mensagem + "\n")
    
    # ~~ Se não tiver mensagem, printa somente char_type.
    else:
        print(char_type*char_qtd)
        if log_path:
            log.write(char_type*char_qtd + "\n")

# ================================================== #

# ~~ Printar DataFrame.
def utilitarios_printar_dataframe(df: pd.DataFrame, log_path: str = None) -> None:

    """
    Resumo:
    - Printa DataFrame em formato de tabela.
    
    Parâmetros:
    - df (DataFrame): DataFrame do pandas.
    - log_path (str | opcional): Caso passado um diretório, transfere texto printado para um arquivo ".txt". 
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Instancia console do rich.
    console = Console()

    # ~~ Cria tabela.
    tabela = Table(show_header=True, header_style="bold blue")

    # ~~ Adiciona colunas.
    for coluna in df.columns:
        tabela.add_column(coluna)

    # ~~ Adiciona linhas.
    for _, linha in df.iterrows():
        tabela.add_row(*map(str, linha.values), end_section=True)

    # ~~ Printa tabela usando o console.
    console.print(tabela)

    # ~~ Se for para direcionar output à um arquivo ".txt".
    if log_path:

        # ~~ Usa tabulate, pois rich exporta tabela com ANSI e arquivo ".txt" não suporta.
        tabela_txt = tabulate(df, headers="keys", tablefmt="grid", showindex=False)

        # ~~ Escreve no arquivo.
        log = open(log_path, "a", encoding="utf-8")
        log.write(tabela_txt + "\n")

# ================================================== #

# ~~ Remove acentos e converte tudo para maiúsculas.
def utilitarios_formatar_texto(texto: str) -> str:

    """
    Resumo:
    - Remove acentos e converte tudo para maiúsculas.
    
    Parâmetros:
    - texto (str): Texto para formatar.
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Verifica se é str passada no parâmetro.
    if isinstance(texto, str):
        
        # ~~ Remove acentos.
        texto_formatado = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")

        # ~~ Converte para maiúsculas.
        texto_formatado = texto_formatado.upper()

        # ~~ Retorna texto formatado.
        return texto_formatado

    # ~~ Caso não seja str, retorna o mesmo valor.
    else:
        return texto

# ================================================== #

# ~~ Retorna as informações de data e mês atuais.
def utilitarios_coletar_data_atual() -> dict:

    """
    Resumo:
    - Retorna as informações de data, mês e ano atuais.
    
    Parâmetros:
    - ===
    
    Retorna:
    - data (dict): Dicionário contendo os dados abaixo.
        - ["dia_numero"] (str): O dia em seu formato numérico.
        - ["mes_numero"] (str): O mês em seu formato numérico.
        - ["ano"] (str): O ano em str.
        - ["hora"] (str): Hora no formato "%H-%M".
        - ["data_com_hora"] (str): Data e hora no formato "%d-%m-%Y_%H-%M".
        - ["dia_extenso"] (str): O dia em seu formato extenso.
        - ["mes_extenso"] (str): O mês em seu formato extenso.
    
    Exceções:
    - ===
    """

    # ~~ Define local para PT-BR no modelo UTF-8 para puxar acentuação e caracteres latinos.
    locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')

    # ~~ Cria dicionário.
    data = {}

    # ~~ Coleta dia, mês e ano.
    data["dia_numero"] = datetime.now().strftime("%d")
    data["mes_numero"] = datetime.now().strftime("%m")
    data["ano"] = datetime.now().strftime("%Y")
    data["hora"] = datetime.now().replace(microsecond=0).strftime("%H-%M")
    data["data_com_hora"] = datetime.now().replace(microsecond=0).strftime("%d-%m-%Y_%H-%M")

    # ~~ Converte para extenso.
    data["dia_extenso"] = datetime.now().strftime("%A").upper()
    data["mes_extenso"] = datetime.now().strftime("%B").upper()

    # ~~ Retorna dados.
    return data

# ================================================== #

# ~~ Retorna a matrícula do usuário.
def utilitarios_coletar_matricula() -> str:

    """
    Resumo:
    - Retorna a matrícula do usuário.
    
    Parâmetros:
    - ===
    
    Retorna:
    - matricula (str): Matrícula.
    
    Exceções:
    - ===
    """

    # ~~ Coleta matrícula.
    matrícula = os.getlogin()

    # ~~ Retorna.
    return matrícula

# ================================================== #

# ~~ Extrai data de string.
def utilitarios_extrair_data(string: str) -> str:

    """
    Resumo:
    - Extrai data de string.
    
    Parâmetros:
    - string (str): Texto para extrair a data.
    
    Retorna:
    - data (str): Data no formato string. Exemplo: "DD/MM/AA".
    
    Exceções:
    - ===
    """

    # ~~ Remove letras e caracteres especiais.
    nova_string = re.sub(r"\D", "", string)

    # ~~ Se quantidade de números for 6, converte ano para o formato "AAAA".
    if len(nova_string) == 6:
        dia, mes, ano = nova_string[:2], nova_string[2:4], nova_string[4:]
        ano = f"20{ano}"
        return f"{dia}/{mes}/{ano}"
    
    # ~~ Sendo 8 números.
    elif len(nova_string) == 8:
        return f"{nova_string[:2]}/{nova_string[2:4]}/{nova_string[4:]}"
    
    # ~~ Não sendo quantidade de números para formar data, retorna string passada no parâmetro.
    else:
        return string

# ================================================== #

# ~~ Obtém diretório do script que está sendo executado.
def utilitarios_obter_diretorio_atual() -> str:

    """
    Resumo:
    - Obtém diretório do script que está sendo executado.
    
    Parâmetros:
    - ===
    
    Retorna:
    - diretório (str): Diretório do script que está sendo executado.
    
    Exceções:
    - ===
    """

    # ~~ Retorna diretório.
    return os.path.dirname(os.path.abspath(sys.argv[0]))

# ================================================== #

# ~~ Consulta os dados financeiros do cliente.
def funcao_consultar_dados_financeiros() -> None:

    """
    Resumo:
    - Consulta os dados financeiros do cliente.
    
    Parâmetros:
    - ===
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Captura de erros.
    try:

        # ~~ Vincula SAP.
        sap = sap_instanciar()

        # ~~ Solicita input da raiz do CNPJ.
        utilitarios_printar_mensagem(mostrar_data_hora="Only")
        raiz_cnpj = input("Informe a raiz do CNPJ (somente números): ")
        utilitarios_printar_mensagem(char_type="=", char_qtd=50)

        # ~~ Faz coleta dos dados.
        utilitarios_printar_mensagem(mensagem=f"Coletando dados financeiros do cliente: {raiz_cnpj}.", char_type="=", char_qtd=50, char_side="bot")
        sap_coletar_dados_financeiros_cliente(sap=sap, raiz_cnpj=raiz_cnpj, printar_dados=True)

        # ~~ Encerra conexão.
        sap_tela_inicial(sap)

    # ~~ Caso seja capturado erro.
    except Exception as erro:
        utilitarios_printar_mensagem(mensagem=erro, char_type="=", char_qtd=50, char_side="bot")
        exit()

# ================================================== #

# ~~ Consulta CNPJ na Receita Federal.
def funcao_consultar_receita_federal() -> None:

    """
    Resumo:
    - Consulta CNPJ na Receita Federal.
    
    Parâmetros:
    - ===
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Solicita o input do CNPJ.
    utilitarios_printar_mensagem(mostrar_data_hora="Only")
    cnpj = input("Digite o CNPJ (somente números): ").strip()
    utilitarios_printar_mensagem(char_type="=", char_qtd=50)

    # ~~ Executa função.
    try:
        utilitarios_consultar_receita_federal(cnpj=cnpj, printar_dados=True)
    except Exception as erro:
        utilitarios_printar_mensagem(mensagem=erro, char_type="=", char_qtd=50, char_side="bot")

# ================================================== #

# ~~ Conferência assinaturas bases (Base Cadastros / Base Revendas).
def funcao_conferencia_assinaturas_bases() -> None:

    """
    Resumo:
    - Conferência assinaturas bases (Base Cadastros / Base Revendas).
    
    Parâmetros:
    - ===
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ While True para manter script ativo até ser selecionado uma opção válida.
    while True:

        # ~~ Input para decidir qual base atualizar. Armazena index escolhido.
        utilitarios_printar_mensagem(mostrar_data_hora="Only")
        index_planilha = int(input("1 - Base de Revendas\n2 - Base de Cadastros\n\nEscolha qual base atualizar: "))
        utilitarios_printar_mensagem(char_type="=", char_qtd=50)

        # ~~ Com base no index escolhido, armazena qual base será atualizada.
        if index_planilha == 1:
            diretorio_planilha = os.getenv("DIRETORIO_BASE_REVENDAS")
            abas = ["Consolidado", "Status Assinatura"]
            aba_leitura = "Consolidado"
            break
        elif index_planilha == 2:
            diretorio_planilha = os.getenv("DIRETORIO_BASE_CADASTROS")
            abas = ["BASE CADASTRO", "Status Assinatura"]
            aba_leitura = "BASE CADASTRO"
            break
        else:
            utilitarios_printar_mensagem(mensagem="Selecione dentre uma das opções listadas.", char_type="=", char_qtd=50, char_side="bot")

    # ~~ Instancia navegador e loga na GoDeep.
    driver = navegador_instanciar()
    navegador_acessar_godeep(driver)

    # ~~ Instancia planilha.
    planilha = excel_instanciar(diretorio_planilha, abas)

    # ~~ Faz leitura da aba planilha usando pandas para atualizar os status de forma otimizada.
    utilitarios_printar_mensagem(mensagem="Fazendo leitura da planilha. Aguarde...", char_type="-", char_qtd=3, char_side="bot")
    excel_salvar_planilha(planilha)
    if index_planilha == 1:
        df = pandas_criar_df(diretorio_planilha=diretorio_planilha, aba="Consolidado", linha_cabecalho=3, colunas_nomes=["CNPJ Cliente.1"])
    else:
        df = pandas_criar_df(diretorio_planilha=diretorio_planilha, aba="BASE CADASTRO", linha_cabecalho=1, colunas_nomes=["CNPJ"])
    utilitarios_printar_mensagem(mensagem="Concluído.", char_type="=", char_qtd=50, char_side="bot")

    # ~~ Loop para verificar linha a linha da aba "Status Assinatura".
    for linha_status_assinatura in range(2, 999999):

        # ~~ Coleta CNPJ.
        cnpj_status_assinatura = excel_coletar_dados(planilha=planilha, aba_nome="Status Assinatura", coluna_nome="CNPJ", linha=linha_status_assinatura, linha_cabecalho=1)

        # ~~ Se não encontra CNPJ, encerrou a lista.
        if cnpj_status_assinatura is None:
            break

        # ~~ Mensagem.
        utilitarios_printar_mensagem(mensagem=f"Verificando status de assinatura do CNPJ: {cnpj_status_assinatura}.", char_type="-", char_qtd=3, char_side="bot")

        # ~~ Função que coleta o status de assinatura.
        status = navegador_coletar_status_assinatura_godeep(driver=driver, cnpj=cnpj_status_assinatura)

        # ~~ Printa status.
        utilitarios_printar_mensagem(mensagem=f"Status: {status}.", char_type="=", char_qtd=50, char_side="bot", mostrar_data_hora="False")

        # ~~ Insere status na planilha, usando o data frame para localizar a linha correspondente.
        if index_planilha == 1:
            linhas_consolidado = pandas_localizar_index(df=df, coluna_nome="CNPJ Cliente.1", localizar=cnpj_status_assinatura, linha_cabecalho=3)
            for linha in linhas_consolidado:
                excel_inserir_dados(planilha=planilha, dado=status, aba_nome="Consolidado", coluna_nome="STATUS DOC", linha=linha, linha_cabecalho=3)
        else:
            linhas_base = pandas_localizar_index(df=df, coluna_nome="CNPJ", localizar=cnpj_status_assinatura, linha_cabecalho=1)
            for linha in linhas_base:
                excel_inserir_dados(planilha=planilha, dado=status, aba_nome="BASE CADASTRO", coluna_nome="STATUS", linha=linha, linha_cabecalho=1)

    # ~~ Após encerrar lista na aba "Status Assinatura", encerra driver e execução do código.
    utilitarios_printar_mensagem(mensagem="Lista finalizada. Encerrando execução...", char_type="=", char_qtd=50, char_side="bot")
    navegador_fechar(driver)

# ================================================== #

# ~~ Consulta status de assinatura.
def funcao_consultar_status_assinaturas() -> None:

    """
    Resumo:
    - Consulta status de assinatura.
    
    Parâmetros:
    - ===
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Input do CNPJ.
    utilitarios_printar_mensagem(mostrar_data_hora="Only")
    cnpj = input("Insira o CNPJ para consultar o status de assinatura (somente números): ")
    utilitarios_printar_mensagem(char_type="=", char_qtd=50)

    # ~~ Cria instância e acessa GoDeep.
    driver = navegador_instanciar()
    navegador_acessar_godeep(driver)

    # ~~ Mensagem.
    utilitarios_printar_mensagem(mensagem=f"Verificando status de assinatura do CNPJ: {cnpj}.", char_type="-", char_qtd=3, char_side="bot")

    # ~~ Coleta status.
    status = navegador_coletar_status_assinatura_godeep(driver, cnpj)

    # ~~ Printa status.
    utilitarios_printar_mensagem(mensagem=f"Status: {status}.", char_type="=", char_qtd=50, char_side="bot", mostrar_data_hora="False")

    # ~~ Fecha navegador.
    navegador_fechar(driver)

# ================================================== #

# ~~ Consulta limites e insere na carteira.
def funcao_consultar_limites_carteira() -> None:

    """
    Resumo:
    - Consulta limites e insere na carteira.
    
    Parâmetros:
    - ===
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Coleta data para encontrar a planilha da carteira mais atualizada.
    data = utilitarios_coletar_data_atual()
    matrícula = utilitarios_coletar_matricula()

    # ~~ Define caminho da Carteira mais atualizada.
    caminho_planilha = fr"C:\Users\{matrícula}\OneDrive - Positivo\Documentos - Carteira_Faturamento\Carteira_Status {data["mes_extenso"]} {data["dia_numero"]}{data["mes_numero"]}.xlsm"

    # ~~ Vincula planilha.
    abas = ["Carteira", "Consultar Limites"]
    planilha = excel_instanciar(caminho_planilha, abas)

    # ~~ Vincula SAP.
    try:
        sap = sap_instanciar()
    except Exception as erro:
        print(erro)
        exit()

    # ~~ Faz leitura da planilha.
    df = pandas_criar_df(diretorio_planilha=caminho_planilha, aba="Carteira", linha_cabecalho=16, colunas_nomes=["Código SAP"])

    # ~~ Loop para pegar cada código ERP na aba "Consultar Limites" e consultar.
    for linha in range(2, 999999):
        cliente_consultado = excel_coletar_dados(planilha=planilha, aba_nome="Consultar Limites", coluna_nome="Código SAP", linha=linha, linha_cabecalho=1)
        if cliente_consultado is None:
            sap_tela_inicial(sap)
            exit()
        cliente_consultado = int(cliente_consultado)
        cliente_consultado = str(cliente_consultado)
        utilitarios_printar_mensagem(mensagem=f"Analisando cliente: {cliente_consultado}.", char_type="=", char_qtd=50, char_side="bot")
        cnpj = sap_coletar_cnpj_xd03(sap=sap, codigo_erp=cliente_consultado)
        raiz_cnpj = cnpj[:8]
        retorno_análise = sap_coletar_dados_financeiros_cliente(sap=sap, raiz_cnpj=raiz_cnpj, printar_dados=True)
        linhas_carteira = pandas_localizar_index(df=df, coluna_nome="Código SAP", localizar=cliente_consultado, linha_cabecalho=16)
        for linha in linhas_carteira:
            excel_inserir_dados(planilha=planilha, dado=retorno_análise["limite"], aba_nome="Carteira", coluna_nome="Limite", linha=linha, linha_cabecalho=16)
            excel_inserir_dados(planilha=planilha, dado=retorno_análise["vencimento"], aba_nome="Carteira", coluna_nome="Vencimento Limite", linha=linha, linha_cabecalho=16)
            excel_inserir_dados(planilha=planilha, dado=retorno_análise["margem"], aba_nome="Carteira", coluna_nome="Margem", linha=linha, linha_cabecalho=16)
            excel_inserir_dados(planilha=planilha, dado=retorno_análise["nfs_vencidas"], aba_nome="Carteira", coluna_nome="Vencidos", linha=linha, linha_cabecalho=16)

# ================================================== #

# ~~ Escolher qual função do bolt irá utilizar.
def funcao_iniciar() -> None:

    """
    Resumo:
    - Escolher qual função do bolt irá utilizar.
    
    Parâmetros:
    - ===
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Início.
    utilitarios_printar_mensagem(char_type="=", char_qtd=50)
    utilitarios_printar_mensagem(mostrar_data_hora="Only")

    # ~~ Input.
    funcao = int(input(
        "1 - Conferência de assinaturas das bases (Base de Cadastros / Base de Revendas).\n" \
        "2 - Consultar status de assinatura na GoDeep.\n" \
        "3 - Consultar Receita Federal.\n" \
        "4 - Consultar dados financeiros.\n" \
        "5 - Consultar dados financeiro (Carteira).\n\n" \
        "Escolha qual executar (inserir número): "
        ))
    utilitarios_printar_mensagem(char_type="=", char_qtd=50)

    # ~~ Inicia função escolhida.
    while True:
        if funcao == 1:
            funcao_conferencia_assinaturas_bases()
            break
        elif funcao == 2:
            funcao_consultar_status_assinaturas()
            break
        elif funcao == 3:
            funcao_consultar_receita_federal()
            break
        elif funcao == 4:
            funcao_consultar_dados_financeiros()
            break
        elif funcao == 5:
            funcao_consultar_limites_carteira()
            break
        else:
            utilitarios_printar_mensagem(mostrar_data_hora="Only")
            funcao = int(input("Não encontrado na lista. Inserir número válido: "))
            utilitarios_printar_mensagem(char_type="=", char_qtd=50)

# ================================================== #