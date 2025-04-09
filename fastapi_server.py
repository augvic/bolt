# ================================================== #

# ~~ Imports.
import threading
import time
from fastapi import FastAPI
from scripts.camada_1.navegador import Navegador
from scripts.camada_0.utilitarios import Utilitarios

# ================================================== #

# ~~ Classe FastApiServer.
class FastApiServer:

    """
    Resumo:
    - Controla rotas para manipulação do WebDriver.

    Atributos:
    - (navegador: Navegador): Instância do "Navegador".
    - (utilitarios: Utilitarios): Instância do "Utilitarios".

    Métodos:
    - (instanciar_navegador): Cria atributo "navegador".
    - (monitorar_navegador): Verifica se navegador é fechado e abre ele novamente.
    - (criar_app): Retorna instância do app FastAPI.
    """

    # ================================================== #

    # ~~ Cria instância do "Navegador".
    def instanciar_navegador(self) -> None:

        """
        Resumo:
        - Cria instância do "Navegador".

        Atributos:
        - (navegador: Navegador): Instância do "Navegador".
        - (utilitarios: Utilitarios): Instância do "Utilitarios".
        """

        # ~~ Cria instância.
        self.utilitarios = Utilitarios()
        self.navegador = Navegador(self.utilitarios)
        time.sleep(3)
        
    # ================================================== #

    # ~~ Monitora se navegador foi fechado e abre novamente.
    def monitorar_navegador(self) -> None:

        """
        Resumo:
        - Monitora se navegador foi fechado e abre novamente.
        """

        while True:
            try:
                self.navegador.driver.title
            except:
                self.navegador.driver.quit()
                self.navegador.instanciar_webdriver()
                self.navegador.driver.get("http://127.0.0.1:8000")
            time.sleep(5)

    # ================================================== #

    # ~~ Criar app FastAPI.
    def criar_app(self) -> FastAPI:

        """
        Resumo:
        - Retorna app FastAPI.

        Retorna:
        - (app: FastAPI)
        """

        # ~~ Retorna app.
        return FastAPI()
    
    # ================================================== #

# ================================================== #

# ~~ Cria instância do FastApiServer.
fastapi_server = FastApiServer()

# ~~ Inicia app.
app = fastapi_server.criar_app()

# ~~ Cria instância do navegador.
fastapi_server.instanciar_navegador()

# ~~ Aloca thread para monitorar fechamento do navegador.
threading.Thread(target=fastapi_server.monitorar_navegador, daemon=True).start()

# ================================================== #