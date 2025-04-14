# ================================================== #

# ~~ Classe base para erros relacionados ao "Pedido".
class DocVendasError(Exception):

    """Classe base para erros relacionados ao "DocVendas"."""

    # ~~ Pass.
    pass

# ================================================== #

# ~~ Classe de erro ao salvar o documento, retorna mensagem de "sem garantia".
class DocVendasGarantiaError(DocVendasError):

    """Subclasse para erros relacionados ao "Pedido"."""

    # ~~ Erro.
    def __init__(self, *args):

        """Quando ao salvar o documento, retorna mensagem de "sem garantia"."""

        # ~~ Erro.
        super().__init__("Erro ao salvar documento, está sem garantia.")

# ================================================== #