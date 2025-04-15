# ================================================== #

# ~~ Imports.
from django.contrib import admin
from django.urls import path
from app.views import *

# ================================================== #

# ~~ Views.
financeiro = Financeiro()
inicio = Inicio()
doc_vendas = DocVendas()

# ================================================== #

# ~~ Rotas.
urlpatterns = [

    # ~~ Django Admin.
    path('admin/', admin.site.urls),

    # ~~ Início.
    path('', inicio.main, name="inicio"),

    # ~~ Financeiro.
    path('financeiro/', financeiro.main, name='financeiro'),

    # ~~ Doc. Vendas.
    path('doc-vendas/', doc_vendas.main, name='doc_vendas'),
]

# ================================================== #
