# ================================================== #

# ~~ Imports.
from django.contrib import admin
from .models import *

# ================================================== #

# ~~ Filtros da tabela DatabaseAuthAdmin.
class ModulesAuthAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("usuario", "modulo")

    # ~~ Filtros laterais.
    list_filter = ("usuario", "modulo")

# ================================================== #

# ~~ Filtros da tabela DatabaseAuthAdmin.
class ComercialAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("nome", "escritorio")

    # ~~ Filtros laterais.
    list_filter = (["escritorio"])

# ================================================== #

# ~~ Filtros da tabela PedidoDados.
class PedidoDadosAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = (["pedido", "status", "forma_pagamento", "vendedor", "escritorio", "revenda", "cliente", "cnpj_cpf", "codigo_erp", "valor_total", "centros", "ordem"])

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

# ~~ Filtros da tabela PedidoItens.
class PedidoItensAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = (["pedido", "centro", "sku", "valor"])

    # ~~ Campo de busca.
    search_fields = (["pedido"])

    # ~~ Filtros laterais.
    list_filter = (["pedido", "centro", "sku"])

# ================================================== #

# ~~ Filtros da tabela DadosFinaceirosClientesAdmin.
class DadosFinaceirosClientesAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("raiz_cnpj", "vencimento_limite", "valor_limite", "valor_em_aberto", "margem")

    # ~~ Campo de busca.
    search_fields = (["raiz_cnpj"])

# ================================================== #

# ~~ Filtros da tabela PedidosPendentes.
class PedidosPendentesAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("pedido", "valor", "raiz_cnpj")

    # ~~ Campo de busca.
    search_fields = ("raiz_cnpj", "pedido")

    # ~~ Filtros laterais.
    list_filter = (["raiz_cnpj"])

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminDocumento(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminOrganizacao(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminCanal(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminEscritorio(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminEquipe(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminFormaPagamento(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminCondicaoPagamento(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminIncoterm(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminMotivo(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminExpedicao(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminTabela(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminCentro(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminDeposito(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao")

# ================================================== #

# ~~ Filtros das tabelas de tipos.
class TiposAdminGarantia(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("chave", "descricao", "valor")

    # ~~ Campo de busca.
    search_fields = ("chave", "descricao", "valor")

# ================================================== #

# ~~ Filtros das tabelas de documento de vendas.
class DocsVendaAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("id", "tipo_doc", "organizacao", "canal", "escritorio", "equipe", "pedido_nome", "emissor", "recebedor", "forma_pagamento", "condicao_pagamento", "incoterm", "motivo", "expedicao", "dados_adicionais", "tabela")

    # ~~ Campo de busca.
    search_fields = ("id", "pedido_nome")

    # ~~ Filtros laterais.
    list_filter = ("pedido_nome", "tipo_doc", "organizacao", "canal", "escritorio", "emissor", "recebedor", "forma_pagamento", "condicao_pagamento")

# ================================================== #

# ~~ Filtros das tabelas de itens dos documentos de vendas.
class DocsVendaItensAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("id_referencia", "sku", "quantidade", "valor_unitario", "centro", "deposito", "over", "garantia", "tipo")

    # ~~ Campo de busca.
    search_fields = ("id_referencia", "sku")

    # ~~ Filtros laterais.
    list_filter = ("sku", "centro", "deposito", "garantia", "tipo")

# ================================================== #

# ~~ Filtros das tabelas de parceiros dos documentos de vendas.
class DocsVendaParceirosAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("id_referencia", "chave", "codigo")

    # ~~ Campo de busca.
    search_fields = ("id_referencia", "chave", "codigo")

    # ~~ Filtros laterais.
    list_filter = ("chave", "codigo")

# ================================================== #

# ~~ Filtros das tabelas de comissionados dos documentos de vendas.
class DocsVendaComissionadosAdmin(admin.ModelAdmin):

    # ~~ Colunas que irão aparecer no admin.
    list_display = ("id_referencia", "chave", "codigo", "porcentagem")

    # ~~ Campo de busca.
    search_fields = ("id_referencia", "chave", "codigo")

    # ~~ Filtros laterais.
    list_filter = ("chave", "codigo")

# ================================================== #

# ~~ Descrição que consta no admin.
admin.site.index_title = "Banco de dados:"

# ================================================== #

# ~~ Tabelas para aparecer no admin.
admin.site.register(ModulesAuth, ModulesAuthAdmin)
admin.site.register(Comercial, ComercialAdmin)
admin.site.register(PedidoDados, PedidoDadosAdmin)
admin.site.register(PedidoRemessas, PedidoRemessasAdmin)
admin.site.register(PedidoDts, PedidoDtsAdmin)
admin.site.register(PedidoNfs, PedidoNfsAdmin)
admin.site.register(PedidoLogs, PedidoLogsAdmin)
admin.site.register(PedidoItens, PedidoItensAdmin)
admin.site.register(DadosFinaceirosClientes, DadosFinaceirosClientesAdmin)
admin.site.register(PedidosPendentes, PedidosPendentesAdmin)
admin.site.register(TiposDocumento, TiposAdminDocumento)
admin.site.register(TiposOrganizacao, TiposAdminOrganizacao)
admin.site.register(TiposCanal, TiposAdminCanal)
admin.site.register(TiposEscritorio, TiposAdminEscritorio)
admin.site.register(TiposEquipe, TiposAdminEquipe)
admin.site.register(TiposFormaPagamento, TiposAdminFormaPagamento)
admin.site.register(TiposCondicaoPagamento, TiposAdminCondicaoPagamento)
admin.site.register(TiposIncoterm, TiposAdminIncoterm)
admin.site.register(TiposMotivo, TiposAdminMotivo)
admin.site.register(TiposExpedicao, TiposAdminExpedicao)
admin.site.register(TiposTabela, TiposAdminTabela)
admin.site.register(TiposCentro, TiposAdminCentro)
admin.site.register(TiposDeposito, TiposAdminDeposito)
admin.site.register(TiposGarantia, TiposAdminGarantia)
admin.site.register(DocsVenda, DocsVendaAdmin)
admin.site.register(DocsVendaItens, DocsVendaItensAdmin)
admin.site.register(DocsVendaParceiros, DocsVendaParceirosAdmin)
admin.site.register(DocsVendaComissionados, DocsVendaComissionadosAdmin)

# ================================================== #
