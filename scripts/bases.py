# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Imports.
import time
from scripts.navegador import Navegador

# ================================================== #

# ~~ Classe BasesHandler.
class BasesHandler:

    """
    Resumo:
    - Gerencia funções relacionadas as bases (revendas e cadastros).

    Atributos:
    - (navegador: Navegador): Instância da classe "Navegador".

    Métodos:
    - (armazenar_navegador): Cria atributo "navegador", armazenando instância da classe "Navegador".
    - (coletar_status_assinatura): Coleta status de assinatura de documento no site.
    """

    # ================================================== #

    # ~~ Atributos.
    navegador = None

    # ================================================== #

    # ~~ Armazena instância "Navegador".
    def armazenar_navegador(self, navegador: Navegador) -> None:

        """
        Resumo:
        - Armazena instância "Navegador".

        Atributos:
        - (navegador: Navegador)
        """

        # ~~ Faz composição.
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
        - (status: str):
            - Sem Cadastro
            - Atualizar Cadastro
            - Cadastro Concluído
            - Assinatura Incompleta
            - Aguardando Assinatura
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

# ================================================== #