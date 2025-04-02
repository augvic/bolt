# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Imports.
import  time
import threading
from fastapi import FastAPI
from scripts import navegador

# ================================================== #

# ~~ Criando server e instância do webdriver.
app = FastAPI()
driver = navegador.instanciar()
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
            driver = navegador.instanciar()
            driver.get("http://127.0.0.1:8000")
        time.sleep(5)

# ================================================== #

# ~~ Fica monitorando fechamento da janela do webdriver, usando threading.
threading.Thread(target=monitorar_webdriver, daemon=True).start()

# ================================================== #