# ================================================== #

# ~~ Importando models.
from django.db import models

# ================================================== #

# ~~ Modelo contendo os dados de cada assistente comercial.
class Comercial(models.Model):

    # ~~ Atributos.
    nome = models.CharField(max_length=200)
    escritorio = models.CharField(max_length=200)
    codigo_zage = models.CharField(max_length=200)
    codigo_assistente = models.CharField(max_length=200)
    codigo_fornecedor = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    superior = models.CharField(max_length=200)

    # ~~ Return no admin.
    def __str__(self):
        return self.nome

# ================================================== #

# ~~ Modelo contendo as permissões de acesso ao database de cada usuário.
class DatabaseAuth(models.Model):

    # ~~ Atributos.
    usuario = models.CharField(max_length=200)
    tabela = models.CharField(max_length=200)

    # ~~ Retorno no admin.
    def __str__(self):
        return self.usuario

# ================================================== #

# ~~ Modelo contendo os dados de pedidos.
class PedidoDados(models.Model):

    # ~~ Atributos.
    status = models.CharField(max_length=200)
    pedido = models.CharField(max_length=200)
    data = models.CharField(max_length=200)
    forma_pagamento = models.CharField(max_length=200)
    condicao_pagamento = models.CharField(max_length=200)
    vendedor = models.CharField(max_length=200)
    escritorio = models.CharField(max_length=200)
    revenda = models.CharField(max_length=200)
    cliente = models.CharField(max_length=200)
    cnpj_cpf = models.CharField(max_length=200)
    codigo_erp = models.CharField(max_length=200)
    comissao_over = models.CharField(max_length=200)
    porcentagem_z6 = models.CharField(max_length=200)
    valor_total = models.FloatField()
    observacao = models.CharField(max_length=200)
    centros = models.CharField(max_length=200)
    ordem = models.CharField(max_length=200)

    # ~~ Retorno no admin.
    def __str__(self):
        return self.pedido

# ================================================== #

# ~~ Modelo contendo as remessas de pedidos.
class PedidoRemessas(models.Model):

    # ~~ Atributos.
    pedido = models.CharField(max_length=200)
    remessa = models.CharField(max_length=200)

    # ~~ Retorno no admin.
    def __str__(self):
        return self.pedido

# ================================================== #

# ~~ Modelo contendo as dts de pedidos.
class PedidoDts(models.Model):

    # ~~ Atributos.
    pedido = models.CharField(max_length=200)
    dt = models.CharField(max_length=200)

    # ~~ Retorno no admin.
    def __str__(self):
        return self.pedido

# ================================================== #

# ~~ Modelo contendo as NFs de pedidos.
class PedidoNfs(models.Model):

    # ~~ Atributos.
    pedido = models.CharField(max_length=200)
    nf = models.CharField(max_length=200)
    situacao = models.CharField(max_length=200)
    data_emissao = models.CharField(max_length=200)

    # ~~ Retorno no admin.
    def __str__(self):
        return self.pedido

# ================================================== #

# ~~ Modelo contendo os logs do pedido.
class PedidoLogs(models.Model):

    # ~~ Atributos.
    pedido = models.CharField(max_length=200)
    log = models.CharField(max_length=200)
    data_hora = models.CharField(max_length=200)

    # ~~ Retorno no admin.
    def __str__(self):
        return self.pedido

# ================================================== #

# ~~ Modelo contendo os dados financeiros de clientes.
class DadosFinaceirosClientes(models.Model):

    # ~~ Atributos.
    raiz_cnpj = models.CharField(max_length=200, primary_key=True)
    vencimento_limite = models.DateField()
    valor_limite = models.CharField(max_length=200)
    valor_em_aberto = models.CharField(max_length=200)
    margem = models.CharField(max_length=200)
    nfs_vencidas = models.CharField(max_length=200)

    # ~~ Retorno no admin.
    def __str__(self):
        return self.raiz_cnpj

# ================================================== #

# ~~ Modelo contendo os pedidos e valores pendentes.
class PedidosPendentes(models.Model):

    # ~~ Atributos.
    raiz_cnpj = models.CharField(max_length=200)
    pedido = models.CharField(max_length=200)
    valor = models.CharField(max_length=200)

    # ~~ Retorno no admin.
    def __str__(self):
        return self.raiz_cnpj

# ================================================== #