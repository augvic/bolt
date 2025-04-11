# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# ================================================== #

# ~~ Bibliotecas.
import win32com.client
from scripts.instancias_primarias.erros.sap_erros import *

# ================================================== #

# ~~ Classe SAP.
class Sap:

    """
    Resumo:
    - Manipula o SAP.

    Atributos:
    - (session: object): Vínculo com tela SAP.

    Métodos:
    - (__init__): Cria atributo "session", fazendo referência ao SAP acessando a SAPScriptingEngine.
    - (abrir_transacao): Abre transação do SAP.
    - (coletar_cnpj_xd03): Coleta CNPJ do cliente da transação XD03 e retorna.
    - (coletar_codigo_erp_xd03): Coleta o código ERP do cliente no SAP.
    - (ir_tela_inicial): Volta à tela inicial do SAP.

    Exceções:
    - (SapError): Classe base.
    - (SapTelaError): Quando não há tela disponível para conexão.
    - (SapTransacaoError): Quando não há acesso à transação.
    """

    # ================================================== #

    # ~~ Cria instância do SAP.
    def __init__(self) -> None:

        """
        Resumo:
        - Cria referência ao SAP acessando a SAPScriptingEngine.
        
        Atributos:
        - (session: object): Vínculo com janela do SAP.
        
        Exceções:
        - (SapTelaError): Quando não há tela disponível para conexão.
        """

        # ~~ Tenta conexão.
        try:
            gui = win32com.client.GetObject("SAPGUI")
            app = gui.GetScriptingEngine
            con = app.Children(0)
            for id in range(0, 4):
                session = con.Children(id)
                if session.ActiveWindow.Text == "SAP Easy Access":
                    self.session = session
                    return
                else:
                    continue

            # ~~ Se não encontrar tela disponível.
            else:
                raise SapTelaError()
        
        # ~~ Se não encontrar tela logada no SAP.
        except:
            raise SapTelaError()

    # ================================================== #

    # ~~ Abrir transação.
    def abrir_transacao(self, transacao: str) -> None:

        """
        Resumo:
        - Abre transação no SAP.
        
        Parâmetros:
        - (transacao: str)
        
        Exceções:
        - (SapTransacaoError): Quando não há acesso à transação.
        """

        # ~~ Acessa transação.
        self.session.findById("wnd[0]/tbar[0]/okcd").text = "/N" + transacao
        self.session.findById("wnd[0]").sendVKey(0)
        status_bar = None
        status_bar = self.session.findById("wnd[0]/sbar").text
        if "Sem autorização" in status_bar:
            raise SapTransacaoError(transacao)

    # ================================================== #

    # ~~ Coleta CNPJ do cliente da transação XD03.
    def coletar_cnpj_xd03(self, codigo_erp: str, liberar_tela: bool = False) -> str:

        """
        Resumo:
        - Coleta CNPJ do cliente da transação XD03 e retorna.
        
        Parâmetros:
        - (codigo_erp: str)
        - (liberar_tela):
            - (False: bool): Padrão. 
            - (True: bool): Libera tela do SAP.
        
        Retorna:
        - (cnpj: str)
        
        Exceções:
        - (SapTransacaoError): Quando não há acesso à transação.
        """

        # ~~ Abre transação XD03.
        self.abrir_transacao("XD03")

        # ~~ Preenche dados e acessa conta.
        self.session.findById("wnd[1]/usr/ctxtRF02D-KUNNR").text = codigo_erp
        self.session.findById("wnd[1]/usr/ctxtRF02D-BUKRS").text = ""
        self.session.findById("wnd[1]/usr/ctxtRF02D-VKORG").text = ""
        self.session.findById("wnd[1]/usr/ctxtRF02D-VTWEG").text = ""
        self.session.findById("wnd[1]/usr/ctxtRF02D-SPART").text = ""
        self.session.findById("wnd[1]").sendVKey(0)

        # ~~ Acessa "dados de controle".
        self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02").select()

        # ~~ Coleta CNPJ.
        cnpj = self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02/ssubSUBSC:SAPLATAB:0200/subAREA3:SAPMF02D:7122/txtKNA1-STCD1").text

        # ~~ Liberar tela?
        if liberar_tela == True:
            self.ir_tela_inicial()

        # ~~ Retorna.
        return cnpj

    # ================================================== #

    # ~~ Coleta código ERP do cliente no SAP.
    def coletar_codigo_erp_xd03(self, cnpj: str, liberar_tela: bool = False) -> str:

        """
        Resumo:
        - Coleta o código ERP do cliente no SAP.
        
        Parâmetros:
        - (cnpj: str)
        - (liberar_tela):
            - (False: bool): Padrão. 
            - OU (True: bool): Libera tela do SAP.
        
        Retorna:
        - (codigo_erp):
            - (codigo_erp: str)
            - OU ("-": str)
        
        Exceções:
        - (SapTransacaoError): Quando não há acesso à transação.
        """

        # ~~ Acessa XD03.
        self.abrir_transacao("XD03")

        # ~~ Busca pelo CNPJ.
        self.session.findById("wnd[1]").sendVKey(4)
        self.session.findById("wnd[2]/usr/tabsG_SELONETABSTRIP/tabpTAB006").select()
        self.session.findById("wnd[2]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[0,24]").text = cnpj
        self.session.findById("wnd[2]/tbar[0]/btn[0]").press()
        msg_bar = self.session.findById("wnd[0]/sbar").text
        if "Nenhum valor para esta seleção" in msg_bar:
            self.session.findById("wnd[1]").close()
            return "-"
        self.session.findById("wnd[2]").sendVKey(2)

        # ~~ Coleta código ERP.
        codigo_erp = self.session.findById("wnd[1]/usr/ctxtRF02D-KUNNR").text

        # ~~ Fecha transação.
        self.session.findById("wnd[1]").close()

        # ~~ Liberar tela?
        if liberar_tela == True:
            self.ir_tela_inicial()

        # ~~ Retorna código ERP.
        return codigo_erp

    # ================================================== #

    # ~~ Volta à tela inicial do SAP.
    def ir_tela_inicial(self) -> None:

        """
        Resumo:
        - Volta à tela inicial do SAP.
        """

        # ~~ Encerra instância SAP.
        while True:
            if self.session.ActiveWindow.Text == "SAP Easy Access":
                break
            else:
                try:
                    self.session.findById("wnd[1]").close()
                except:
                    self.session.findById("wnd[0]").sendVKey(3)

    # ================================================== #

# ================================================== #