# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Imports.
import time
from scripts import utilitarios
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# ================================================== #

# ~~ Classe base de erros relacionados ao Navegador.
class NavegadorError(Exception):

    """Classe base para erros do Navegador."""

    # ~~ Pass.
    pass

# ================================================== #

# ~~ Classe de erro para objeto não instanciado.
class NavegadorInstanciaError(NavegadorError):

    """Subclasse de erros do Navegador."""

    # ~~ Erro.
    def __init__(self):

        """Quando objeto não foi instanciado."""

        # ~~ Raise.
        super().__init__("Navegador não instanciado.")

# ================================================== #

# ~~ Classe Navegador.
class Navegador:

    """
    Resumo:
    - Classe que manipula navegador.

    Atributos:
    - (driver: Chrome): Instância do navegador.
    - (by: By)
    - (keys: Keys)

    Métodos:
    - (instanciar_webdriver): Cria atributo "driver", instanciando navegador.
    - (acessar_godeep): Acessa site GoDeep e loga nele.
    """

    # ================================================== #

    # ~~ Atributos.
    driver = None
    by = By()
    keys = Keys()

    # ================================================== #

    # ~~ Cria instância WebDriver.
    def instanciar_webdriver(self) -> None:

        """
        Resumo:
        - Cria instância WebDriver.

        Atributos:
        - (driver: Chrome)
        """

        # ~~ Configurações.
        options = Options()
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("detach", True)

        # ~~ Criando instância.
        self.driver = webdriver.Chrome(options=options)
        abas_abertas = self.driver.window_handles
        if len(abas_abertas) > 1:
            self.driver.switch_to.window(abas_abertas[0])
            self.driver.close()
        try:
            self.driver.switch_to.window(abas_abertas[0])
        except:
            self.driver.switch_to.window(abas_abertas[1])

        # ~~ Acessa rota principal do server Django.
        self.driver.get("http://127.0.0.1:8000")

    # ================================================== #

    # ~~ Acessa e loga na GoDeep.
    def acessar_godeep(self) -> None:

        """
        Resumo:
        - Acessa e loga na GoDeep.

        Exceções:
        - (NavegadorInstanciaError): Quando objeto não foi instanciado.
        """

        # ~~ Verifica se navegador está instanciado.
        if self.driver == None:
            raise NavegadorInstanciaError()

        # ~~ Acessando GoDeep e fazendo login.
        self.driver.get(f"https://www.revendedorpositivo.com.br/admin/")
        microsoft_login_botao = None
        try:
            microsoft_login_botao = self.driver.find_element(By.ID, value="login-ms-azure-ad")
            microsoft_login_botao.click()
            time.sleep(5)
            body = self.driver.find_element(By.TAG_NAME, value="body").text
            if any(login_string in body for login_string in ["Because you're accessing sensitive info, you need to verify your password.", "Sign in", "Pick an account", "Entrar"]):
                utilitarios.printar_mensagem(mostrar_data_hora="Only")
                input("Necessário logar conta Microsoft. Aperte ENTER aqui depois para continuar.")
                utilitarios.printar_mensagem(char_type="=", char_qtd=50)
            if "Approve sign in request" in body:
                time.sleep(3)
                codigo = self.driver.find_element(By.ID, value="idRichContext_DisplaySign").text
                utilitarios.printar_mensagem(mostrar_data_hora="Only")
                input(f"Necessário authenticator Microsoft para continuar: {codigo}. Aperte ENTER aqui depois para continuar.")
                utilitarios.printar_mensagem(char_type="=", char_qtd=50)
        except:
            self.driver.get(f"https://www.revendedorpositivo.com.br/admin/index/")

    # ================================================== #

# ================================================== #