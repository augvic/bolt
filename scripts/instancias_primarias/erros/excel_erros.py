# ================================================== #

# ~~ Classe base de erros relacionados ao Excel.
class ExcelError(Exception):
    
    """Classe base para erros do Excel."""

    # ~~ Pass.
    pass

# ================================================== #

# ~~ Classe de erro para arquivo não encontrado.
class ExcelArquivoNaoEncontradoError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, caminho):

        """Quando arquivo do Excel não for encontrado."""

        # ~~ Raise.
        super().__init__(f"Arquivo Excel não encontrado no caminho: '{caminho}'.")

# ================================================== #

# ~~ Classe de erro para aba não encontrada.
class ExcelAbaNaoEncontradaError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, aba, planilha):

        """Quando uma aba especificada não existe na planilha."""

        # ~~ Raise.
        super().__init__(f"Aba '{aba}' não existe na planilha '{planilha}'")

# ================================================== #

# ~~ Classe de erro para coluna não encontrada.
class ExcelColunaNaoEncontradaError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, coluna, aba):

        """Quando uma coluna especificada não existe na aba."""

        # ~~ Raise.
        super().__init__(f"Coluna '{coluna}' não existe na aba '{aba}'")

# ================================================== #

# ~~ Classe de erro ao salvar planilha.
class ExcelSalvarPlanilhaError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, planilha):

        """Quando não é possível salvar planilha."""

        # ~~ Raise.
        super().__init__(f"Não foi possível salvar a planilha {planilha}")

# ================================================== #

# ~~ Classe de erro quando dado para localizar não foi encontrado.
class ExcelLocalizarDadoError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, dado):

        """Quando dado para localizar não foi encontrado."""

        # ~~ Raise.
        super().__init__(f"Dado '{dado}' não foi localizado.")

# ================================================== #