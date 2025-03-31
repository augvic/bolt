# ================================================== #

# ~~ Imports.
from django.contrib import admin
from django.urls import path
import app.views

# ================================================== #

# ~~ Rotas.
urlpatterns = [

    # ~~ Django Admin.
    path('admin/', admin.site.urls),

    # ~~ Início.
    path('', app.views.inicio, name="inicio"),

    # ~~ Database.
    path('database/', app.views.database, name="database"),
    path('database/comercial/', app.views.database_comercial, name="database_comercial"),
    path('database/comercial/inserir/', app.views.database_comercial_inserir, name="database_comercial_inserir"),
    path('database/comercial/delete/<int:assistente_id>/', app.views.database_comercial_delete, name="database_comercial_delete"),
    path('database/comercial/edit/<int:assistente_id>/', app.views.database_comercial_edit, name="database_comercial_edit"),

    # ~~ Financeiro.
    path('financeiro/', app.views.financeiro, name='financeiro'),
]

# ================================================== #
