# ================================================== #

# ~~ Import.
from django.db import connection
import os
import sys
import django

# ================================================== #

# ~~ Sobe o diretório para raiz.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ~~ Define os settings do Django.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

# ~~ Inicia o setup do Django.
django.setup()

# ================================================== #

# ~~ Função para excluir tabelas do sqlite3.
def drop_table(table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Tabela {table_name} removida.")

# ~~ Tabelas para excluir.
tabelas_a_excluir = [""]

# ~~ Deleta cada tabela.
for tabela in tabelas_a_excluir:
    drop_table(tabela)

# ================================================== #