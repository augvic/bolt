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
from scripts.controladores.pedido import Pedido

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
    def remover_pedido_pendente(numero_pedido: str, adicionar_ao_em_aberto: bool) -> dict:

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
    def importar_pedido_database(self, pedido: Pedido) -> None:

        """
        Resumo:
        - Importa dados coletados do pedido no database.

        Parâmetros:
        - (pedido: Pedido)
        """

        # ~~ Verifica se pedido já existe.
        pedido = PedidoDados.objects.filter(pedido=self.pedido).first()
        if pedido:
            pedido.status = self.status
            pedido.pedido = self.pedido
            pedido.data = self.data
            pedido.forma_pagamento = self.forma_pagamento
            pedido.condicao_pagamento = self.condicao_pagamento
            pedido.vendedor = self.vendedor
            pedido.escritorio = self.escritorio
            pedido.revenda = self.revenda
            pedido.cliente = self.cliente
            pedido.cnpj_cpf = self.cnpj_cpf
            pedido.codigo_erp = self.codigo_erp
            pedido.comissao_over = self.over
            pedido.porcentagem_z6 = self.porcentagem_comissao
            pedido.valor_total = self.valor_pedido
            pedido.observacao = self.observacao
            pedido.centros = self.centros
            pedido.ordem = self.ordem
            pedido.save()
        else:
            pedido_novo = PedidoDados(
                status=self.status,
                pedido=self.pedido,
                data=self.data,
                forma_pagamento=self.forma_pagamento,
                condicao_pagamento=self.condicao_pagamento,
                vendedor=self.vendedor,
                escritorio=self.escritorio,
                revenda=self.revenda,
                cliente=self.cliente,
                cnpj_cpf=self.cnpj_cpf,
                codigo_erp=self.codigo_erp,
                comissao_over=self.over,
                porcentagem_z6=self.porcentagem_comissao,
                valor_total=self.valor_pedido,
                observacao=self.observacao,
                centros=self.centros,
                ordem=self.ordem
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
        pedido_liberado = PedidosPendentes.objects.filter(pedido=self.pedido).first()
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

# ================================================== #