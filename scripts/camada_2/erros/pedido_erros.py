# ================================================== #

# ~~ Classe base para erros relacionados ao "Pedido".
class PedidoError(Exception):

    """Classe base para erros relacionados ao "Pedido"."""

    # ~~ Pass.
    pass

# ================================================== #

# ~~ Classe de erro quando pedido não foi inserido no site ainda.
class PedidoNaoInseridoError(PedidoError):

    """Subclasse para erros relacionados ao "Pedido"."""

    # ~~ Erro.
    def __init__(self, pedido):

        """Quando pedido não foi inserido no site ainda."""

        # ~~ Erro.
        super().__init__(f"Pedido {pedido} não foi inserido no site ainda.")

# ================================================== #

# ~~ Classe de erro quando dados do pedido não foram coletados para analisar.
class PedidoDadosNaoColetadosError(PedidoError):

    """Subclasse para erros relacionados ao "Pedido"."""

    # ~~ Erro.
    def __init__(self, *args):

        """Quando dados do pedido não foram coletados para analisar."""

        # ~~ Erro.
        super().__init__("Não há dados coletados para analisar.")

# ================================================== #