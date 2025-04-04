# ================================================== #

# ~~ Imports.
import threading
import time
from fastapi import FastAPI
from scripts.navegador import Navegador

# ================================================== #

# ~~ Server.
app = FastAPI()

# ================================================== #

# ~~ Instância do navegador.
navegador = Navegador()
navegador.instanciar_webdriver()
time.sleep(3)
threading.Thread(target=navegador.monitorar_navegador, daemon=True).start()

# ================================================== #