# ================================================== #

# ~~ Subindo para raiz do projeto.
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Define settings Django.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django
django.setup()

# ~~ Imports.
import scripts.pedido as pedido
import scripts.navegador as navegador

# ================================================== #

# ~~ Área de testes.
dados_pedido = {
    "cnpj": "32228232000198",
    "pedido": "13398",
    "valor_pedido": 2655.19
}
pedido.analise_crédito(dados_pedido, printar_dados=True)

# ================================================== #