# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# ================================================== #

# ~~ Imports.
from datetime import datetime
from dateutil.relativedelta import relativedelta
from scripts.instancias_primarias.sap import Sap
from scripts.instancias_secundarias.erros.doc_vendas_erros import *

# ================================================== #

# ~~ Classe que gerencia criação e edição de documentos de venda do SAP.
class DocVendas:

    # ================================================== #

    # ~~ Init.
    def __init__(self, sap: Sap):
        
        # ~~ Atributos.
        self.sap = sap

    # ================================================== #

    # ~~ Criar documento de venda.
    def criar_doc(self, dados: dict) -> str:

        """
        Resumo:
        - Cria documento de venda no SAP.

        Parâmetros:
        - (dados: dict)

        Retorna:
        - (documento: str)

        Exceções:
        - (DocVendasGarantiaError): Quando ao salvar o documento, retorna mensagem de "sem garantia".
        """

        # ~~ Abre transação.
        if dados["tipo_doc"] == "ZCOT":
            self.sap.abrir_transacao("VA21")
        else:
            self.sap.abrir_transacao("VA01")
        
        # ~~ Insere dados organizacionais.
        self.sap.session.findById("wnd[0]/usr/ctxtVBAK-AUART").text = dados["tipo_doc"]
        self.sap.session.findById("wnd[0]/usr/ctxtVBAK-VKORG").text = dados["organizacao"]
        self.sap.session.findById("wnd[0]/usr/ctxtVBAK-VTWEG").text = dados["canal"]
        self.sap.session.findById("wnd[0]/usr/ctxtVBAK-SPART").text = "00"
        self.sap.session.findById("wnd[0]/usr/ctxtVBAK-VKBUR").text = dados["escritorio"]
        self.sap.session.findById("wnd[0]/usr/ctxtVBAK-VKGRP").text = dados["equipe"]
        self.sap.session.findById("wnd[0]").sendVKey(0)

        # ~~ Preenche dados de venda.
        self.sap.session.findById(r"wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/txtVBKD-BSTKD").text = dados["pedido_nome"]
        self.sap.session.findById(r"wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/ctxtVBKD-BSTDK").text = datetime.now().strftime("%d.%m.%Y")
        self.sap.session.findById(r"wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUAGV-KUNNR").text = dados["emissor"]
        self.sap.session.findById(r"wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/subPART-SUB:SAPMV45A:4701/ctxtKUWEV-KUNNR").text = dados["recebedor"]
        try:
            data_validade = datetime.now() + relativedelta(months=1)
            data_validade = data_validade.strftime("%d.%m.%Y")
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/ssubHEADER_FRAME:SAPMV45A:4440/ctxtVBAK-BNDDT").text = data_validade
        except:
            pass
        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/ssubHEADER_FRAME:SAPMV45A:4440/ctxtVBKD-ZTERM").text = dados["condicao_pagamento"]
        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/ssubHEADER_FRAME:SAPMV45A:4440/ctxtVBKD-INCO1").text = dados["incoterm"]
        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/ssubHEADER_FRAME:SAPMV45A:4440/cmbVBAK-AUGRU").Key = dados["motivo"]
        self.sap.session.findById(r"wnd[0]").sendVKey(0)
        self.sap.session.findById(r"wnd[0]").sendVKey(0)
        self.sap.session.findById(r"wnd[0]").sendVKey(0)

        # ~~ Marca fornecimento completo.
        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4400/ssubHEADER_FRAME:SAPMV45A:4440/chkVBAK-AUTLF").Selected = True

        # ~~ Acessa síntese e insere itens.
        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02").select()
        i = 0
        for item in dados["itens"]:
            if item["tipo"] != "TCL/MOU":
                self.sap.session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtRV45A-MABNR[1,{i}]").text = item["sku"]
                self.sap.session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/txtRV45A-KWMENG[2,{i}]").text = item["quantidade"]
                self.sap.session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtVBAP-WERKS[13,{i}]").text = item["centro"]
                self.sap.session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtVBAP-LGORT[3,{i}]").text = item["deposito"]
                i += 1
        self.sap.session.findById(r"wnd[0]").sendVKey(0)
        
        # ~~ Lista técnica. Se pop up não aparecer, ignora.
        try:
            self.sap.session.findById(r"wnd[1]/usr/tblSAPMC29ACNTL/txtRC29K-STKTX[1,0]").setFocus()
            self.sap.session.findById(r"wnd[1]").sendVKey(2)
        except:
            pass

        # ~~ Acessa cabeçalho.
        self.sap.session.findById(r"wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/btnBT_HEAD").press()

        # ~~ Se tiver tabela, preenche.
        if dados["tabela"]:
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\01/ssubSUBSCREEN_BODY:SAPMV45A:4301/cmbVBKD-PLTYP").key = dados["tabela"]
            self.sap.session.findById(r"wnd[0]").sendVKey(0)
        
        # ~~ Expedição.
        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\02").select()
        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4302/ctxtVBKD-VSART").text = dados["expedicao"]
        self.sap.session.findById(r"wnd[0]").sendVKey(0)

        # ~~ Forma de pagamento.
        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\05").select()
        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\05/ssubSUBSCREEN_BODY:SAPMV45A:4311/ctxtVBKD-ZLSCH").text = dados["forma_pagamento"]
        self.sap.session.findById(r"wnd[0]").sendVKey(0)

        # ~~ Parceiros.
        for parceiro in dados["parceiros"]:
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08").select()
            for i in range(0, 20):
                key = self.sap.session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW/cmbGVS_TC_DATA-REC-PARVW[0,{i}]").key    
                if key == " ":
                    self.sap.session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW/cmbGVS_TC_DATA-REC-PARVW[0,{i}]").key = parceiro["chave"]
                    self.sap.session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\08/ssubSUBSCREEN_BODY:SAPMV45A:4352/subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW/ctxtGVS_TC_DATA-REC-PARTNER[1,{i}]").text = parceiro["codigo"]
                    break
            self.sap.session.findById(r"wnd[0]").sendVKey(0)
            self.sap.session.findById(r"wnd[0]").sendVKey(0)

        # ~~ Dados adicionais da NF, caso tenha.
        if dados["dados_adicionais"] != None:
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\09").select()
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\09/ssubSUBSCREEN_BODY:SAPMV45A:4152/subSUBSCREEN_TEXT:SAPLV70T:2100/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[1]/shell").setSelectionIndexes(0, 0)
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\09/ssubSUBSCREEN_BODY:SAPMV45A:4152/subSUBSCREEN_TEXT:SAPLV70T:2100/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[0]/shell").selectItem("9002", "Column1")
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\09/ssubSUBSCREEN_BODY:SAPMV45A:4152/subSUBSCREEN_TEXT:SAPLV70T:2100/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[0]/shell").ensureVisibleHorizontalItem("9002", "Column1")
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\09/ssubSUBSCREEN_BODY:SAPMV45A:4152/subSUBSCREEN_TEXT:SAPLV70T:2100/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[0]/shell").doubleClickItem("9002", "Column1")
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\09/ssubSUBSCREEN_BODY:SAPMV45A:4152/subSUBSCREEN_TEXT:SAPLV70T:2100/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[1]/shell").text = dados["dados_adicionais"]
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\09/ssubSUBSCREEN_BODY:SAPMV45A:4152/subSUBSCREEN_TEXT:SAPLV70T:2100/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[1]/shell").setSelectionIndexes(0, 0)
            self.sap.session.findById(r"wnd[0]").sendVKey(0)

        # ~~ Volta à síntese.
        self.sap.session.findById(r"wnd[0]/tbar[0]/btn[3]").press()

        # ~~ Insere valores e garantias para cada item.
        i = 0
        for item in dados["itens"]:

            # ~~ Acessa o item.
            self.sap.session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtRV45A-MABNR[1,{i}]").setFocus()
            self.sap.session.findById(r"wnd[0]").sendVKey(2)

            # ~~ Entra em dados adicionais B.
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15").select()

            # ~~ Coloca a garantia.
            if item["garantia"]:
                self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/ctxtVBAP-ZZCDGARANTIAEXT").text = item["garantia"]
                self.sap.session.findById(r"wnd[0]").sendVKey(0)
                self.sap.session.findById(r"wnd[0]").sendVKey(0)

            # ~~ Acessa as condições.
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06").select()

            # ~~ Atualiza em B.
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/subSUBSCREEN_PUSHBUTTONS:SAPLV69A:1000/btnBT_KONY").press()
            self.sap.session.findById(r"wnd[1]/usr/lbl[1,4]").setFocus()
            self.sap.session.findById(r"wnd[1]").sendVKey(2)

            # ~~ Se tiver over.
            if item["over"]:
                self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/txtKOMV-KBETR[3,11]").text = item["over"]
            
            # ~~ Loop para inserir valor.
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/txtKOMV-KBETR[3,2]").text = str(item["valor"]).replace(".", ",")
            self.sap.session.findById(r"wnd[0]").sendVKey(0)
            while True:

                # ~~ Pega os valores do SAP e soma.
                valor_liquido = float(str(self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/txtKOMP-NETWR").text).replace(".", "").replace(",", ".").strip())
                valor_imposto = float(str(self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/txtKOMP-MWSBP").text).replace(".", "").replace(",", ".").strip())
                soma_liquido_imposto = round((valor_liquido + valor_imposto) / item["quantidade"], 2)

                # ~~ Se valor estiver diferente do valor do item.
                if soma_liquido_imposto != item["valor"]:

                    # ~~ Calcula a diferença.
                    diferenca = round(soma_liquido_imposto - item["valor"], 2)

                    # ~~ Se a diferença estiver 15 centavos pra cima ou baixo, insere no ZD15.
                    if 0 < diferenca <= 0.15 or -0.15 < diferenca <= 0:
                        for linha in range(70, 90):
                            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN").verticalScrollbar.position = linha
                            zd15 = self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/ctxtKOMV-KSCHL[1,0]").text
                            if zd15 == "ZD15":
                                self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/txtKOMV-KBETR[3,0]").text = str(abs(diferenca)).replace(".", ",") if diferenca < 0 else str(-abs(diferenca)).replace(".", ",")
                                break

                    # ~~ Se não estiver, insere no campo de valor padrão.
                    else:
                        valor_no_campo = float(str(self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/txtKOMV-KBETR[3,2]").text).replace(".", "").replace(",", ".").strip())
                        novo_valor = round(valor_no_campo - diferenca, 2)
                        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\06/ssubSUBSCREEN_BODY:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/txtKOMV-KBETR[3,2]").text = str(novo_valor).replace(".", ",")
                    
                    # ~~ Confirma novo valor.
                    self.sap.session.findById(r"wnd[0]").sendVKey(0)
                
                # ~~ Quando valor estiver correto, sai do loop.
                else:
                    break

            # ~~ Volta à síntese.
            self.sap.session.findById(r"wnd[0]/tbar[0]/btn[3]").press()
            i += 1
        
        # ~~ Colocando comissão.
        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\02/ssubSUBSCREEN_BODY:SAPMV45A:4401/subSUBSCREEN_TC:SAPMV45A:4900/tblSAPMV45ATCTRL_U_ERF_AUFTRAG/ctxtRV45A-MABNR[1,0]").setFocus()
        self.sap.session.findById(r"wnd[0]").sendVKey(2)
        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15").select()
        i = 0
        for comissionado in dados["comissao"]:
            self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnPB_ADD").press()
            self.sap.session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/cmbTG_TABCOM-PARVW[0,{i}]").key = comissionado["chave"]
            self.sap.session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/ctxtTG_TABCOM-LIFNR[1,{i}]").text = comissionado["codigo"]
            self.sap.session.findById(rf"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/tblSAPMV45ATC_TABCOMISS/txtTG_TABCOM-KBETR[3,{i}]").text = comissionado["porcentagem"]
            i += 1
        self.sap.session.findById(r"wnd[0]").sendVKey(0)

        # ~~ Replica comissão.
        self.sap.session.findById(r"wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\15/ssubSUBSCREEN_BODY:SAPMV45A:4462/subKUNDEN-SUBSCREEN_8459:SAPMV45A:8459/btnBT_REPL_COMISS").press()
        self.sap.session.findById(r"wnd[1]/usr/btnBUTTON_1").press()
        self.sap.session.findById(r"wnd[1]/tbar[0]/btn[0]").press()

        # ~~ Salva documento.
        self.salvar_documento()

        # ~~ Coleta número do documento criado.
        if dados["tipo_doc"] == "ZCOT":
            self.sap.abrir_transacao("VA22")
        else:
            self.sap.abrir_transacao("VA02")
        documento = self.sap.session.findById(r"wnd[0]/usr/subSUBSCREEN_HEADER:SAPMV45A:4021/ctxtVBAK-VBELN").text

        # ~~ Retorna.
        return documento

    # ================================================== #

    # ~~ Salva documento.
    def salvar_documento(self) -> None:

        """
        Resumo:
        - Salva documento.

        Exceções:
        - (DocVendasGarantiaError): Quando ao salvar o documento, retorna mensagem de "sem garantia".
        """

        # ~~ Salvar.
        self.sap.session.findById("wnd[0]/tbar[0]/btn[11]").press()
        try:
            self.sap.session.findById("wnd[0]/tbar[1]/btn[18]").press()
        except:
            pass
        msg_bar = self.sap.session.findById("wnd[0]/sbar").text
        if "sem garantia" in msg_bar:
            raise DocVendasGarantiaError()
        elif "Não foi efetuada" in msg_bar:
            return
        elif "foi gravado" in msg_bar:
            return
        else:
            self.sap.session.findById("wnd[0]").sendVKey(0)
            try:
                self.sap.session.FindById("wnd[1]/usr/btnSPOP-VAROPTION1").press()
            except:
                pass
            return

    # ================================================== #

# ================================================== #

dados = {
    "tipo_doc": "ZCOT",
    "organizacao": "3100",
    "canal": "15",
    "escritorio": "1105",
    "equipe": "058",
    "pedido_nome": "TESTE SAMOC",
    "emissor": "1000784725",
    "recebedor": "1000784725",
    "condicao_pagamento": "Z134",
    "incoterm": "CIF",
    "motivo": "900",
    "itens": [
        {
            "sku": "1307015",
            "quantidade": "4",
            "centro": "3010",
            "deposito": "0175",
            "garantia": "",
            "over": "",
            "valor": "2815.00",
            "tipo": "PAI"
        },
        {
            "sku": "11117918",
            "quantidade": "4",
            "centro": "3010",
            "deposito": "0175",
            "garantia": "",
            "over": "",
            "valor": "42.00",
            "tipo": "TCL/MOU"
        },
        {
            "sku": "11086967",
            "quantidade": "4",
            "centro": "3010",
            "deposito": "0175",
            "garantia": "",
            "over": "",
            "valor": "21.00",
            "tipo": "TCL/MOU"
        },
        {
            "sku": "1702794",
            "quantidade": "1",
            "centro": "3010",
            "deposito": "0175",
            "garantia": "",
            "over": "",
            "valor": "3428.00",
            "tipo": "PAI"
        },
        {
            "sku": "1702837",
            "quantidade": "1",
            "centro": "3010",
            "deposito": "0175",
            "garantia": "",
            "over": "",
            "valor": "3428.00",
            "tipo": "PAI"
        }
    ],
    "tabela": "21",
    "expedicao": "01",
    "forma_pagamento": "V",
    "parceiros": [
        {
            "chave": "ZW",
            "codigo": "1001380210"
        }
    ],
    "dados_adicionais": "TESTE",
    "comissao": [
        {
            "chave": "Z2",
            "codigo": "2000006653",
            "porcentagem": "0,32"
        },
        {
            "chave": "Z5",
            "codigo": "2000005674",
            "porcentagem": "0,32"
        },
        {
            "chave": "Z7",
            "codigo": "COMPROV",
            "porcentagem": "0,30"
        }
    ]
}

sap = Sap()
doc_vendas = DocVendas(sap)
doc_vendas.criar_doc(dados)