# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# ================================================== #

# ~~ Inicia setup Django.
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

# ================================================== #

# ~~ Imports.
import getpass
from app.models import *
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404

# ================================================== #

# ~~ Classe Database.
class Database:

    """
    Resumo:
    - Classe que controla interações com o database.
    """

    # ================================================== #

    # ~~ Coleta os acessos à modulos disponíveis por usuário.
    async def modulos_disponiveis(self) -> list:

        """
        Resumo:
        - Retorna os acessos de módulos que o usuário tem disponivel.

        Retorna:
        - (modulos_disponiveis: list)
        """

        # ~~ Abre as abas que o usuário possui acesso.
        matricula = getpass.getuser()
        modulos_disponiveis = await sync_to_async(
            lambda: list(ModulesAuth.objects.filter(usuario=matricula).values_list("modulo", flat=True))
        )()

        # ~~ Retorna.
        return modulos_disponiveis
    
    # ================================================== #

    # ~~ Remove do database o valor de pedido pendente.
    def remover_pedido_pendente(self, numero_pedido: str, adicionar_ao_em_aberto: bool) -> None:

        """
        Resumo:
        - Remove do database o valor de pedido pendente.
        
        Parâmetros:
        - (numero_pedido: str):
        - (adicionar_ao_em_aberto):
            - (False: bool): Apenas remove valor pendente.
            - (True: bool): Remove valor e soma ele com o que possui em aberto.
        """

        # ~~ Coleta pedido pendente.
        pedido = get_object_or_404(PedidosPendentes, pedido=numero_pedido)

        # ~~ Coleta cliente.
        cliente = get_object_or_404(DadosFinaceirosClientes, raiz_cnpj=pedido.raiz_cnpj)

        # ~~ Coleta valores.
        margem = float(cliente.margem)
        valor_pedido = float(pedido.valor)
        if cliente.valor_em_aberto != "Sem valores em aberto.":
            em_aberto = float(cliente.valor_em_aberto)
        else:
            em_aberto = 0

        # ~~ Se for para adicionar o valor ao "em aberto".
        if adicionar_ao_em_aberto == True:
            cliente.valor_em_aberto = em_aberto + valor_pedido
        else:
            cliente.margem = margem + valor_pedido
        cliente.save()

        # ~~ Deleta pedido.
        pedido.delete()

    # ================================================== #

    # ~~ Importa dados no database.
    def importar_pedido_database(self,
        pedido: str, status: str = None, data: str = None, forma_pagamento: str = None,
        condicao_pagamento: str = None, vendedor: str = None, escritorio: str = None,
        revenda: str = None, cliente: str = None, cnpj_cpf: str = None, codigo_erp: str = None,
        over: str = None, porcentagem_comissao: str = None, valor_total: str = None, observacao: str = None,
        centros: str = None, ordem: str = None
    ) -> None:

        """
        Resumo:
        - Importa dados coletados do pedido no database.

        Parâmetros:
        - (pedido: Pedido)
        """

        # ~~ Verifica se pedido já existe.
        pedido_object = PedidoDados.objects.filter(pedido=pedido).first()
        if pedido_object:
            if status:
                pedido_object.status = status
            if pedido:
                pedido_object.pedido = pedido
            if data:
                pedido_object.data = data
            if forma_pagamento:
                pedido_object.forma_pagamento = forma_pagamento
            if condicao_pagamento:
                pedido_object.condicao_pagamento = condicao_pagamento
            if vendedor:
                pedido_object.vendedor = vendedor
            if escritorio:
                pedido_object.escritorio = escritorio
            if revenda:
                pedido_object.revenda = revenda
            if cliente:
                pedido_object.cliente = cliente
            if cnpj_cpf:
                pedido_object.cnpj_cpf = cnpj_cpf
            if codigo_erp:
                pedido_object.codigo_erp = codigo_erp
            if over:
                pedido_object.over = over
            if porcentagem_comissao:
                pedido_object.porcentagem_comissao = porcentagem_comissao
            if valor_total:
                pedido_object.valor_total = valor_total
            if observacao:
                pedido_object.observacao = observacao
            if centros:
                pedido_object.centros = centros
            if ordem:
                pedido_object.ordem = ordem
            pedido_object.save()
        else:
            pedido_novo = PedidoDados(
                status=status,
                pedido=pedido,
                data=data,
                forma_pagamento=forma_pagamento,
                condicao_pagamento=condicao_pagamento,
                vendedor=vendedor,
                escritorio=escritorio,
                revenda=revenda,
                cliente=cliente,
                cnpj_cpf=cnpj_cpf,
                codigo_erp=codigo_erp,
                over=over,
                porcentagem_comissao=porcentagem_comissao,
                valor_total=valor_total,
                observacao=observacao,
                centros=centros,
                ordem=ordem
            )
            pedido_novo.save()

    # ================================================== #

    # ~~ Coleta pedidos pendentes de um cliente.
    def coletar_pedidos_pendentes(self, raiz_cnpj: str) -> None:

        """
        Resumo:
        - Coleta pedidos pendentes de um cliente.

        Parâmetros:
        - (raiz_cnpj: str)

        Retorna:
        - (valores_pedidos_pendentes: QueryList)
        """

        # ~~ Retorna pedidos.
        return PedidosPendentes.objects.filter(raiz_cnpj=raiz_cnpj).values_list("valor", flat=True)

    # ================================================== #

    # ~~ Importa dados financeiros de cliente.
    def importar_dados_financeiros_cliente(self, raiz_cnpj: str, vencimento: str = None, limite: str = None, em_aberto: str = None, margem: str = None, nfs_vencidas: str = None) -> None:

        """
        Resumo:
        - Importa dados financeiros de cliente. Pode ser importado dados individualmente.

        Parâmetros:
        - (raiz_cnpj: str)
        - (vencimento: str)
        - (limite: str)
        - (em_aberto: str)
        - (margem: str)
        - (nfs_vencidas: str)
        """

        # ~~ Se cliente já existe, apenas atualiza.
        cliente = DadosFinaceirosClientes.objects.filter(raiz_cnpj=raiz_cnpj).first()
        if cliente:
            if vencimento:
                cliente.vencimento_limite = vencimento
            if limite:
                cliente.valor_limite = limite
            if em_aberto:
                cliente.valor_em_aberto = em_aberto
            if margem:
                cliente.margem = margem
            if nfs_vencidas:
                cliente.nfs_vencidas = nfs_vencidas
            cliente.save()
        
        # ~~ Se não existe, cria novo registro.
        else:
            novo_cliente = DadosFinaceirosClientes(
                raiz_cnpj=raiz_cnpj,
                vencimento_limite=vencimento,
                valor_limite=limite,
                valor_em_aberto=em_aberto,
                margem=margem,
                nfs_vencidas=nfs_vencidas
            )
            novo_cliente.save()

    # ================================================== #

    # ~~ Importa pedido pendente.
    def importar_pedido_pendente(self, raiz_cnpj: str, pedido: str, valor_pedido: str) -> None:

        """
        Resumo:
        - Importa pedido pendente.

        Parâmetros:
        - (raiz_cnpj: str)
        - (pedido: str)
        - (valor_pedido: str)
        """

        # ~~ Importa somente se pedido não estiver no database.
        pedido_liberado = PedidosPendentes.objects.filter(pedido=pedido).first()
        if not pedido_liberado:
            valor_pendente_novo = PedidosPendentes(
                raiz_cnpj=raiz_cnpj,
                pedido=pedido,
                valor=valor_pedido
            )
            valor_pendente_novo.save()

    # ================================================== #

    # ~~ Coleta escritório.
    def coletar_escritorio(self, vendedor: str) -> None:

        """
        Resumo:
        - Coleta escritório.

        Parâmetros:
        - (vendedor: str)

        Retorna:
        - (escritorio: QueryList)
        """

        # ~~ Retorna escritório.
        return Comercial.objects.filter(nome=vendedor).values_list("escritorio", flat=True)

    # ================================================== #

    # ~~ Importa itens do pedido.
    def importar_itens_pedido(self, pedido: str, itens: list) -> None:

        """
        Resumo:
        - Importa itens do pedido.

        Parâmetros:
        - (pedido: str)
        - (itens: list)
        """

        # ~~ Importa somente se itens não estiverem no database.
        itens_database = PedidoItens.objects.filter(pedido=pedido).first()
        if not itens_database:
            for item in itens:
                item_novo = PedidoItens(
                    pedido=pedido,
                    centro=item["centro"],
                    sku=item["sku"],
                    valor=item["valor"]
                )
                item_novo.save()

# ================================================== #