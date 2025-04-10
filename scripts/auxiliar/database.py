# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# ================================================== #

# ~~ Inicia setup Django.
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

# ================================================== #

# ~~ Imports.
import getpass
from app.models import *
from asgiref.sync import sync_to_async

# ================================================== #

# ~~ Classe Database.
class Database:

    """
    Resumo:
    - Classe que controla interações com o database.
    """

    # ================================================== #

    # ~~ Coleta os acessos à modulos disponíveis por usuário.
    async def modulos_disponiveis(self) -> list:

        """
        Resumo:
        - Retorna os acessos de módulos que o usuário tem disponivel.

        Retorna:
        - (modulos_disponiveis: list)
        """

        # ~~ Abre as abas que o usuário possui acesso.
        matricula = getpass.getuser()
        modulos_disponiveis = await sync_to_async(
            lambda: list(ModulesAuth.objects.filter(usuario=matricula).values_list("modulo", flat=True))
        )()

        # ~~ Retorna.
        return modulos_disponiveis
    
    # ================================================== #

# ================================================== #