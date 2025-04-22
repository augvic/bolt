# ================================================== #

# ~~ Imports.
from django.shortcuts import render, redirect
from app.models import *
from scripts.auxiliar.database import Database

# ================================================== #

# ~~ Cria instância do controlador do database
database = Database()

# ================================================== #

# ~~ Financeiro.
class Financeiro:

    """Financeiro view."""

    # ================================================== #

    # ~~ Main view.
    def main(self, request):

        # ~~ Retorna página.
        return render(request, "financeiro/financeiro.html")

    # ================================================== #

# ================================================== #

# ~~ Inicio.
class Inicio:

    """Inicio view."""

    # ================================================== #

    # ~~ Main view.
    def main(self, request):

        # ~~ Retorna página.
        return render(request, "inicio/inicio.html")
    
    # ================================================== #

# ================================================== #

# ~~ Doc. Vendas.
class DocVendas:

    """Doc. Vendas view."""

    # ================================================== #

    # ~~ Main view.
    def main(self, request):

        # ~~ Coleta os datalist para renderizar a página.
        tipo_docs = database.coletar_datalist("tipo_doc")
        organizacoes = database.coletar_datalist("organizacao")
        canais = database.coletar_datalist("canal")
        escritorios = database.coletar_datalist("escritorio")
        equipes = database.coletar_datalist("equipe")
        formas_pagamento = database.coletar_datalist("forma_pagamento")
        condicoes_pagamento = database.coletar_datalist("condicao_pagamento")
        incoterms = database.coletar_datalist("incoterms")
        motivos = database.coletar_datalist("motivo")
        tipos_expedicao = database.coletar_datalist("expedicao")
        tabelas_preco = database.coletar_datalist("tabela")
        centros = database.coletar_datalist("centro")
        depositos = database.coletar_datalist("deposito")

        # ~~ Monta contexto.
        contexto = {
            "tipo_docs": tipo_docs,
            "organizacoes": organizacoes,
            "canais": canais,
            "escritorios": escritorios,
            "equipes": equipes,
            "formas_pagamento": formas_pagamento,
            "condicoes_pagamento": condicoes_pagamento,
            "incoterms": incoterms,
            "motivos": motivos,
            "tipos_expedicao": tipos_expedicao,
            "tabelas_preco": tabelas_preco,
            "centros": centros,
            "depositos": depositos
        }

        # ~~ Renderiza página.
        return render(request, "doc_vendas/doc_vendas.html", contexto)

    # ================================================== #

    # ~~ Rota para adicionar dados na fila.
    def adicionar_na_fila(self, request):

        # ~~ Verifica se o método é POST.
        if request.method == "POST":

            # ~~ Coleta os dados da requisição POST.
            dados = request.POST

            # ~~ Monta lista com itens.
            itens = []
            for i in range(0, 20):
                sku = dados.get(f"sku_{i}")
                if not sku:
                    pass
                item = {
                    "sku": dados.get(f"sku_{i}"),
                    "quantidade": dados.get(f"quantidade_{i}"),
                    "valor": dados.get(f"valor_{i}"),
                    "centro": dados.get(f"centro_{i}"),
                    "deposito": dados.get(f"deposito_{i}"),
                    "over": dados.get(f"over_{i}"),
                    "garantia": dados.get(f"garantia_{i}"),
                    
                }

            dados_dict = {
                "tipo_doc": str(dados.get("documento")).strip(),
                "organizacao": str(dados.get("organizacao")).strip(),
                "canal": str(dados.get("canal")).strip(),
                "escritorio": str(dados.get("escritorio")).strip(),
                "equipe": str(dados.get("equipe")).strip(),
                "pedido_nome": str(dados.get("pedido")).strip(),
                "emissor": str(dados.get("emissor")).strip(),
                "recebor": str(dados.get("recebedor")).strip(),
                "forma_pagamento": str(dados.get("forma_pagamento")).strip(),
                "condicao_pagamento": str(dados.get("condicao_pagamento")).strip(),
                "incoterm": str(dados.get("incoterm")).strip(),
                "motivo": str(dados.get("motivo")).strip(),
                "expedicao": str(dados.get("expedicao")).strip(),
                "dados_adicionais": str(dados.get("dados_adicionais")).strip(),
                "tabela": str(dados.get("tabela_preco")).strip(),
                "itens": [
                    {
                        
                    }    
                ],
                "parceiros": {

                },
                "comissao": {

                }
            }

        # ~~ Se não for post, redireciona para main view.
        else:
            return redirect("doc_vendas_main")

    # ================================================== #

# ================================================== #