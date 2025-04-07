# ================================================== #

# ~~ Imports.
import subprocess
import os

# ================================================== #

# ~~ Classe Main.
class Main:

    """
    Resumo:
    - Inicializa processo principal com seus dois subprocessos: "Django Server" e "FastAPI Server".

    Métodos:
    - (iniciar_django): Inicializa o Django Server.
    - (iniciar_fastapi): Inicializa o FastAPI Server.
    - (iniciar): Inicia subprocessos.
    """

    # ================================================== #

    # ~~ Processo do server Django.
    def iniciar_django(self) -> subprocess.Popen:

        """
        Resumo:
        - Inicializa o Django Server.
        """

        # ~~ Retorna com subprocesso.
        return subprocess.Popen(["python", "django_server.py", "runserver"])

    # ================================================== #

    # ~~ Processo do server FastAPI.
    def iniciar_fastapi(self) -> subprocess.Popen:

        """
        Resumo:
        - Inicializa o FastAPI Server.
        """ 

        # ~~ Retorna com subprocesso.
        return subprocess.Popen(["python", "-m", "uvicorn", "fastapi_server:app", "--host", "127.0.0.1", "--port", "5001"])

    # ================================================== #

    # ~~ Iniciar.
    def iniciar(self) -> None:

        """
        Resumo:
        - Executa os métodos, iniciando projeto.
        """

        # ~~ Muda título da aba do terminal.
        os.system("title bolt")

        # ~~ Init.
        processo_django = self.iniciar_django()
        processo_webdriver = self.iniciar_fastapi()

        # ~~ Wait.
        processo_django.wait()
        processo_webdriver.wait()

    # ================================================== #

# ================================================== #

# ~~ Inicializa ambos os servers.
if __name__ == "__main__":

    # ~~ Cria instância do Main.
    main = Main()
    main.iniciar()

# ================================================== #