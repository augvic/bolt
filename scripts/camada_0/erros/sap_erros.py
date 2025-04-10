# ================================================== #

# ~~ Classe base para erros relacionados ao "Sap".
class SapError(Exception):

    """Classe base para erros relacionados ao "Sap"."""

    # ~~ Pass.
    pass

# ================================================== #

# ~~ Classe de erro quando não há tela disponível para conexão.
class SapTelaError(SapError):

    """Subclasse para erros relacionados ao "Sap"."""

    # ~~ Erro.
    def __init__(self, *args):

        """Quando não há tela disponível para conexão."""

        # ~~ Erro.
        super().__init__("Não há tela disponível para conexão.")

# ================================================== #

# ~~ Classe de erro quando não há acesso à transação.
class SapTransacaoError(SapError):

    """Subclasse para erros relacionados ao "Sap"."""

    # ~~ Erro.
    def __init__(self, transacao):

        """Quando não há acesso à transação."""

        # ~~ Erro.
        super().__init__(f"Sem acesso à transação {transacao}")

# ================================================== #