# ================================================== #

# ~~ Imports.
import os
import sys

# ================================================== #

# ~~ Classe DjangoServer.
class DjangoServer:

    """
    Resumo:
    - Controla comandos do server Django.

    Métodos:
    - (main): Executa comandos do Django. Argumentos devem ser passados via terminal ao executar script.
    """

    # ================================================== #

    # ~~ Main.
    def main(self):
        
        """
        Resumo:
        - Executa comandos do Django. Argumentos devem ser passados via terminal ao executar script.
        """

        # ~~ Manage.
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        execute_from_command_line(sys.argv)

    # ================================================== #

# ================================================== #

# ~~ Cria instância do DjangoServer.
django_server = DjangoServer()

# ~~ Inicia o main.
django_server.main()

# ================================================== #