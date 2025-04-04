# ================================================== #

# ~~ Imports.
import subprocess
import os

# ================================================== #

# ~~ Processo do server Django.
def iniciar_django() -> subprocess.Popen:
    return subprocess.Popen(["python", "django_server.py", "runserver"])

# ~~ Processo do server FastAPI.
def iniciar_fastapi() -> subprocess.Popen:
    return subprocess.Popen(["python", "-m", "uvicorn", "fastapi_server:app", "--host", "127.0.0.1", "--port", "5001"])

# ~~ Muda título da aba do terminal.
os.system("title bolt")

# ================================================== #

# ~~ Inicializa ambos os servers.
if __name__ == "__main__":

    # ~~ Init.
    processo_django = iniciar_django()
    processo_webdriver = iniciar_fastapi()

    # ~~ Wait.
    processo_django.wait()
    processo_webdriver.wait()

# ================================================== #