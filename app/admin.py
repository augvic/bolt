# ================================================== #

# ~~ Imports.
from django.contrib import admin
from .models import *

# ================================================== #

# ~~ Filtros da tabela DatabaseAuthAdmin.
class ComercialAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("nome", "escritorio")

    # ~~ Filtros laterais.
    list_filter = (["escritorio"])

# ================================================== #

# ~~ Filtros da tabela DatabaseAuthAdmin.
class DatabaseAuthAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("usuario", "tabela")

    # ~~ Filtros laterais.
    list_filter = ("usuario", "tabela")

# ================================================== #

# ~~ Filtros da tabela PedidoDados.
class PedidoDadosAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = (["pedido"])

    # ~~ Filtros laterais.
    list_filter = ("status", "forma_pagamento", "condicao_pagamento", "vendedor", "escritorio")

    # ~~ Campo de busca.
    search_fields = (["pedido"])

# ================================================== #

# ~~ Filtros da tabela PedidoRemessas.
class PedidoRemessasAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("pedido", "remessa")

    # ~~ Campo de busca.
    search_fields = (["pedido"])

# ================================================== #

# ~~ Filtros da tabela PedidoDts.
class PedidoDtsAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("pedido", "dt")

    # ~~ Campo de busca.
    search_fields = (["pedido"])

# ================================================== #

# ~~ Filtros da tabela PedidoNfs.
class PedidoNfsAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("pedido", "nf", "situacao", "data_emissao")

    # ~~ Filtros laterais.
    list_filter = (["situacao"])

    # ~~ Campo de busca.
    search_fields = ("pedido", "nf")

# ================================================== #

# ~~ Filtros da tabela PedidoNfs.
class PedidoLogsAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = (["pedido"])

    # ~~ Campo de busca.
    search_fields = (["pedido"])

# ================================================== #

# ~~ Tabelas para aparecer no admin.
admin.site.register(Comercial)
admin.site.register(DatabaseAuth, DatabaseAuthAdmin)
admin.site.register(PedidoDados, PedidoDadosAdmin)
admin.site.register(PedidoRemessas, PedidoRemessasAdmin)
admin.site.register(PedidoDts, PedidoDtsAdmin)
admin.site.register(PedidoNfs, PedidoNfsAdmin)
admin.site.register(PedidoLogs, PedidoLogsAdmin)

# ================================================== #
