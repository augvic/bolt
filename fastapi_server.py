# ================================================== #

# ~~ Imports.
import asyncio
from fastapi import FastAPI
from scripts.instancias_primarias.navegador import Navegador
from scripts.auxiliar.utilitarios import Utilitarios
from scripts.auxiliar.database import Database
from app.models import *

# ================================================== #

# ~~ Classe FastApiServer.
class FastApiServer:

    """
    Resumo:
    - Controla rotas para manipulação do WebDriver.

    Atributos:
    - (navegador: Navegador): Instância do "Navegador".
    - (utilitarios: Utilitarios): Instância do "Utilitarios".
    - (database: Database): Instância do "Database".

    Métodos:
    - (iniciar): Cria atributos e instâncias.
    - (monitorar_navegador): Verifica se navegador é fechado e abre ele novamente.
    - (criar_app): Retorna instância do app FastAPI.
    """

    # ================================================== #

    # ~~ Cria instância do "Navegador".
    async def iniciar(self) -> None:

        """
        Resumo:
        - Cria atributos e instâncias.

        Atributos:
        - (navegador: Navegador): Instância do "Navegador".
        - (utilitarios: Utilitarios): Instância do "Utilitarios".
        - (database: Database): Instância do "Database".
        """

        # ~~ Cria instâncias.
        self.utilitarios = Utilitarios()
        self.navegador = Navegador(self.utilitarios)
        self.database = Database()

        # ~~ Acessa página principal.
        self.navegador.driver.get("http://127.0.0.1:8000")

        # ~~ Abre as abas que o usuário possui acesso.
        modulos_disponiveis = await self.database.modulos_disponiveis()
        for modulo in modulos_disponiveis:
            self.navegador.driver.execute_script(f"window.open('http://127.0.0.1:8000/{modulo}');")

        abas = self.navegador.driver.window_handles
        self.navegador.driver.switch_to.window(abas[0])

    # ================================================== #

    # ~~ Monitora se navegador foi fechado e abre novamente.
    async def monitorar_navegador(self) -> None:

        """
        Resumo:
        - Monitora se navegador foi fechado e abre novamente.
        """

        # ~~ Fica em loop.
        while True:
            try:
                _ = self.navegador.driver.title
            except:
                try:
                    self.navegador.driver.quit()
                except:
                    pass
                await self.iniciar()
            await asyncio.sleep(5)

    # ================================================== #

    # ~~ Criar app FastAPI.
    def criar_app(self) -> FastAPI:

        """
        Resumo:
        - Retorna app FastAPI.

        Retorna:
        - (app: FastAPI)
        """

        # ~~ Cria app.
        app = FastAPI()

        # ~~ Inicia FastAPI Server.
        @app.on_event("startup")
        async def startup():

            # ~~ Inicia.
            await fastapi_server.iniciar()

            # ~~ Monitora fechamento do navegador de forma assíncrona.
            await self.monitorar_navegador()

        # ~~ Retorna app.
        return app
    
    # ================================================== #

# ================================================== #

# ~~ Cria instância do FastApiServer.
fastapi_server = FastApiServer()

# ~~ Cria app.
app = fastapi_server.criar_app()

# ================================================== #