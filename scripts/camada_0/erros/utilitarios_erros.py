# ================================================== #

# ~~ Classe base para erros relacionados ao "Utilitarios".
class UtilitariosError(Exception):

    """Classe base para erros relacionados ao "Utilitarios"."""

    # ~~ Pass.
    pass

# ================================================== #

# ~~ Classe de erro quando há erro ao fazer requisição à API.
class UtilitariosFazerRequisicaoError(UtilitariosError):

    """Subclasse para erros relacionados ao "Utilitarios"."""

    # ~~ Erro.
    def __init__(self, erro):

        """Quando há erro ao fazer requisição à API."""

        # ~~ Erro.
        super().__init__(f"Erro ao fazer requisição: {erro}.")

# ================================================== #

# ~~ Classe de erro quando há erro no retorno da requisição à API.
class UtilitariosRetornoRequisicaoError(UtilitariosError):

    """Subclasse para erros relacionados ao "Utilitarios"."""

    # ~~ Erro.
    def __init__(self, resposta):

        """Quando há erro no retorno da requisição à API."""

        # ~~ Erro.
        super().__init__(f"Erro na resposta da requisição: {resposta.status_code} - {resposta.text}.")

# ================================================== #