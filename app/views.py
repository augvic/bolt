# ================================================== #

# ~~ Imports.
import getpass
from django.shortcuts import render, redirect, get_object_or_404
from app.models import *

# ================================================== #

# ~~ Financeiro.
class Financeiro:

    """Financeiro view."""

    # ================================================== #

    # ~~ Financeiro view.
    def main(self, request):

        # ~~ Retorna página.
        return render(request, "financeiro/financeiro.html")

    # ================================================== #

# ================================================== #

# ~~ Inicio.
class Inicio:

    """Inicio view."""

    # ================================================== #

    # ~~ Inicio view.
    def main(self, request):

        # ~~ Retorna página.
        return render(request, "inicio/inicio.html")
    
    # ================================================== #

# ================================================== #

# ~~ Doc. Vendas.
class DocVendas:

    """Doc. Vendas view."""

    # ================================================== #

    # ~~ View.
    def main(self, request):

        # ~~ Renderiza página.
        tipo_docs = None
        organizacoes = None
        canais = None
        escritorios = None
        equipes = None
        formas_pagamento = None
        condicoes_pagamento = None
        incoterms = None
        tabelas_preco = None
        return render(request, "doc_vendas/doc_vendas.html")

    # ================================================== #

# ================================================== #