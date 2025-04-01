# ================================================== #

# ~~ Imports.
from fastapi import FastAPI
from . import utilitarios
import time
import threading

# ================================================== #

# ~~ Criando server e instância do webdriver.
app = FastAPI()
driver = utilitarios.navegador_instanciar()
driver.get("http://127.0.0.1:8000")

# ================================================== #

# ~~ Detecta se a janela foi fechada e abre novamente.
def monitorar_webdriver():
    global driver
    while True:
        try:
            driver.title
        except:
            driver.quit()
            driver = utilitarios.navegador_instanciar()
            driver.get("http://127.0.0.1:8000")
        time.sleep(5)

# ================================================== #

# ~~ Fica monitorando fechamento da janela do webdriver, usando threading.
threading.Thread(target=monitorar_webdriver, daemon=True).start()

# ================================================== #