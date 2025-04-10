# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# ================================================== #

# ~~ Imports.
import time
from selenium import webdriver
from scripts.instancias.erros.navegador_erros import *
from scripts.auxiliar.utilitarios import Utilitarios
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# ================================================== #

# ~~ Classe Navegador.
class Navegador:

    """
    Resumo:
    - Classe que manipula navegador.

    Atributos:
    - (driver: Chrome): Instância do WebDriver.
    - (by: By): Localizador de elementos do WebDriver.
    - (keys: Keys): Input de teclas do WebDriver.
    - (utilitarios: Utilitarios): Funções auxiliares.

    Métodos:
    - (__init__): Cria atributos, instanciando WebDriver.
    - (acessar_godeep): Acessa site GoDeep e loga nele.
    """

    # ================================================== #

    # ~~ Cria instância WebDriver.
    def __init__(self, utilitarios: Utilitarios) -> None:

        """
        Resumo:
        - Cria instância WebDriver e define atributos.

        Parâmetros:
        - (utilitarios: Utilitarios): Instância da classe "Utilitarios".

        Atributos:
        - (driver: Chrome): Instância do WebDriver.
        - (by: By): Localizador de elementos do WebDriver.
        - (keys: Keys): Input de teclas do WebDriver.
        - (utilitarios: Utilitarios): Funções auxiliares.
        """

        # ~~ Configurações.
        options = Options()
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

        # ~~ Atributos.
        self.driver = driver
        self.by = By()
        self.keys = Keys()
        self.utilitarios = utilitarios

    # ================================================== #

    # ~~ Acessa e loga na GoDeep.
    def acessar_godeep(self) -> None:

        """
        Resumo:
        - Acessa e loga na GoDeep.
        """

        # ~~ Acessando GoDeep e fazendo login.
        self.driver.get(f"https://www.revendedorpositivo.com.br/admin/")
        microsoft_login_botao = None
        try:
            microsoft_login_botao = self.driver.find_element(By.ID, value="login-ms-azure-ad")
            microsoft_login_botao.click()
            time.sleep(5)
            body = self.driver.find_element(By.TAG_NAME, value="body").text
            if any(login_string in body for login_string in ["Because you're accessing sensitive info, you need to verify your password.", "Sign in", "Pick an account", "Entrar"]):
                self.utilitarios.printar_mensagem(mostrar_data_hora="Only")
                input("Necessário logar conta Microsoft. Aperte ENTER aqui depois para continuar.")
                self.utilitarios.printar_mensagem(char_type="=", char_qtd=50)
            if "Approve sign in request" in body:
                time.sleep(3)
                codigo = self.driver.find_element(By.ID, value="idRichContext_DisplaySign").text
                self.utilitarios.printar_mensagem(mostrar_data_hora="Only")
                input(f"Necessário authenticator Microsoft para continuar: {codigo}. Aperte ENTER aqui depois para continuar.")
                self.utilitarios.printar_mensagem(char_type="=", char_qtd=50)
        except:
            self.driver.get(f"https://www.revendedorpositivo.com.br/admin/index/")

    # ================================================== #

# ================================================== #