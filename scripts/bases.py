# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Imports.
import time
from scripts.navegador import Navegador
from scripts.excel import Excel
from scripts.erros import *

# ================================================== #

# ~~ Classe BasesHandler.
class BasesHandler:

    """
    Resumo:
    - Gerencia funções relacionadas as bases (revendas e cadastros).

    Atributos:
    - (navegador: Navegador): Instância da classe "Navegador".
    - (base: Excel): Instância da classe "Excel".

    Métodos:
    - (__init__): Cria atributos.
    - (coletar_status_assinatura): Coleta status de assinatura de documento no site.
    """

    # ================================================== #

    # ~~ Armazena instância "Navegador".
    def __init__(self, navegador: Navegador, base: Excel) -> None:

        """
        Resumo:
        - Cria atributos.

        Parâmetros:
        - (navegador: Navegador): Instância da classe "Navegador".
        - (base: Excel): Instância da classe "Excel". Sendo a base de revendas ou de cadastros.

        Atributos:
        - (navegador: Navegador): Instância da classe "Navegador".
        - (base: Excel): Instância da classe "Excel".
        """

        # ~~ Armazena qual base será atualizada.
        if base.planilha["BOOK"].name == "Base Consolidada de REVENDAS.xlsx":
            self.aba_leitura = "Consolidado"
            self.linha_cabecalho = 3
            self.coluna = "CNPJ Cliente.1"
            self.coluna_importar = "STATUS DOC"
        else:
            self.aba_leitura = "BASE CADASTRO"
            self.linha_cabecalho = 1
            self.coluna = "CNPJ"
            self.coluna_importar = "STATUS"

        # ~~ Atributos.
        self.base = base
        self.navegador = navegador

    # ================================================== #

    # ~~ Coletar status de assinatura.
    def coletar_status_assinatura(self, cnpj: str) -> str:

        """
        Resumo:
        - Coleta status de assinatura.

        Parâmetros:
        - (cnpj: str)

        Retorna:
        - (status):
            - ("Sem Cadastro": str)
            - OU("Atualizar Cadastro": str)
            - OU("Cadastro Concluído": str)
            - OU("Assinatura Incompleta": str)
            - OU("Aguardando Assinatura": str)
        """

        # ~~ Valor padrão.
        status = ""

        # ~~ Acessa site e acessa aba da DocuSign. Se não encontrar cliente, é porque ele não possui cadastro.
        try:
            self.navegador.driver.get("https://www.revendedorpositivo.com.br/admin/clients")
            pesquisa = self.navegador.driver.find_element(self.navegador.by.ID, value="keyword")
            pesquisa.clear()
            pesquisa.send_keys(cnpj)
            pesquisa.send_keys(self.navegador.keys.ENTER)
            time.sleep(3)
            editar = self.navegador.driver.find_elements(self.navegador.by.XPATH, value="//table/tbody/tr")[1].find_elements(self.navegador.by.XPATH, value=".//td")[10].find_element(self.navegador.by.XPATH, value=".//a") 
            editar = editar.get_attribute("href")
            self.navegador.driver.get(str(editar)) 
            time.sleep(3)
            docu_sign = self.navegador.driver.find_element(self.navegador.by.XPATH, value="//section").find_elements(self.navegador.by.XPATH, value=".//ul/li")[14].find_element(self.navegador.by.XPATH, value=".//a").get_attribute("href")
            self.navegador.driver.get(str(docu_sign))
        except:
            status = "Sem Cadastro"
            return status

        # ~~ Se status não for "Sem Cadastro", procura status do documento.
        if status == "":
            docs = self.navegador.driver.find_elements(self.navegador.by.XPATH, value="//table[@class='table-bordered table-striped table-condensed cf']/tbody/tr")
            for doc in docs:
                sem_documento = doc.find_elements(self.navegador.by.XPATH, value=".//td")[0].text
                if sem_documento == "Não foram encontrados registros.":
                    status = "Atualizar Cadastro"
                    break
                status = doc.find_elements(self.navegador.by.XPATH, value=".//td")[1].text
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

    # ~~ Importa status de assinaturas nas bases (Base Cadastros / Base Revendas).
    def importar_status_assinatura_base(self, cnpj: str, status: str) -> None:

        """
        Resumo:
        - Importa status de assinaturas nas bases (Base Cadastros / Base Revendas).

        Parâmetros:
        - (cnpj: str)
        - (status: str)
        """

        # ~~ Salva planilha.
        self.base.salvar()

        # ~~ Insere status na planilha, usando o data frame para localizar a linha correspondente.
        linhas = self.base.localizar_index(aba=self.aba_leitura, coluna_nome=self.coluna, localizar=cnpj, linha_cabecalho=self.linha_cabecalho)
        for linha in linhas:
            self.base.inserir_dado(dado=status, aba_nome=self.aba_leitura, coluna_nome=self.coluna_importar, linha=linha, linha_cabecalho=self.linha_cabecalho)

    # ================================================== #

# ================================================== #