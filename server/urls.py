# ================================================== #

# ~~ Imports.
from django.contrib import admin
from django.urls import path
from app.views import *

# ================================================== #

# ~~ Views.
database = Database()
financeiro = Financeiro()
inicio = Inicio()

# ================================================== #

# ~~ Rotas.
urlpatterns = [

    # ~~ Django Admin.
    path('admin/', admin.site.urls),

    # ~~ Início.
    path('', inicio.main, name="inicio"),

    # ~~ Database.
    path('database/', database.main, name="database"),
    path('database/comercial/', database.comercial, name="database_comercial"),
    path('database/comercial/inserir/', database.comercial_inserir, name="database_comercial_inserir"),
    path('database/comercial/delete/<int:assistente_id>/', database.comercial_delete, name="database_comercial_delete"),
    path('database/comercial/edit/<int:assistente_id>/', database.comercial_edit, name="database_comercial_edit"),

    # ~~ Financeiro.
    path('financeiro/', financeiro.main, name='financeiro'),
]

# ================================================== #
