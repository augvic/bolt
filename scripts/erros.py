# ================================================== #

# ~~ Classe base para erros relacionados ao "BasesHandler".
class BasesHandlerError(Exception):

    """Classe base para erros relacionados ao "BasesHandler"."""

    # ~~ Pass.
    pass

# ================================================== #

# ~~ Classe de erro quando não há instância do navegador armazenada.
class BasesHandlerNavegadorError(BasesHandlerError):

    """Subclasse para erros relacionados ao "BasesHandler"."""

    # ~~ Erro.
    def __init__(self, *args):

        """Quando não há navegador armazenado."""

        # ~~ Erro.
        super().__init__("Não há navegador armazenado.")

# ================================================== #

# ~~ Classe base de erros relacionados ao Excel.
class ExcelError(Exception):
    
    """Classe base para erros do Excel."""

    # ~~ Pass.
    pass

# ================================================== #

# ~~ Classe de erro para arquivo não encontrado.
class ArquivoNaoEncontradoError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, caminho):

        """Quando arquivo do Excel não for encontrado."""

        # ~~ Raise.
        super().__init__(f"Arquivo Excel não encontrado no caminho: '{caminho}'.")

# ================================================== #

# ~~ Classe de erro para aba não encontrada.
class AbaNaoEncontradaError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, aba, planilha):

        """Quando uma aba especificada não existe na planilha."""

        # ~~ Raise.
        super().__init__(f"Aba '{aba}' não existe na planilha '{planilha}'")

# ================================================== #

# ~~ Classe de erro para coluna não encontrada.
class ColunaNaoEncontradaError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, coluna, aba):

        """Quando uma coluna especificada não existe na aba."""

        # ~~ Raise.
        super().__init__(f"Coluna '{coluna}' não existe na aba '{aba}'")

# ================================================== #

# ~~ Classe de erro ao salvar planilha.
class SalvarPlanilhaError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, planilha):

        """Quando não é possível salvar planilha."""

        # ~~ Raise.
        super().__init__(f"Não foi possível salvar a planilha {planilha}")

# ================================================== #

# ~~ Classe de erro quando não há planilha referenciada.
class PlanilhaReferenciadaError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, *args):

        """Quando não há planilha referenciada."""

        # ~~ Raise.
        super().__init__(f"Sem planilha referenciada.")

# ================================================== #

# ~~ Classe base de erros relacionados ao Navegador.
class NavegadorError(Exception):

    """Classe base para erros do Navegador."""

    # ~~ Pass.
    pass

# ================================================== #

# ~~ Classe de erro para objeto não instanciado.
class NavegadorInstanciaError(NavegadorError):

    """Subclasse de erros do Navegador."""

    # ~~ Erro.
    def __init__(self, *args):

        """Quando objeto não foi instanciado."""

        # ~~ Raise.
        super().__init__("Navegador não instanciado.")

# ================================================== #

# ~~ Classe base para erros relacionados ao PandasTools.
class PandasToolsError(Exception):

    """Clase base para erros do PandasTools."""

    # ~~ Pass.
    pass

# ================================================== #

# ~~ Classe para erro de planilha não encontrada.
class PandasToolsPlanilhaError(PandasToolsError):

    """Subclasse para erros do PandasTools."""

    # ~~ Erro.
    def __init__(self, *args):

        """Quando diretório da planilha não foi encontrado."""

        # ~~ Raise.
        super().__init__("Planilha não encontrada.")

# ================================================== #

# ~~ Classe para erro de dado não encontrado.
class PandasToolsDadoError(PandasToolsError):

    """Subclasse para erros do PandasTools."""

    # ~~ Erro.
    def __init__(self, *args):

        """Quando dado não foi encontrado."""

        # ~~ Raise.
        super().__init__("Dado não encontrado.")

# ================================================== #

# ~~ Classe base para erros relacionados ao "Pedido".
class PedidoError(Exception):

    """Classe base para erros relacionados ao "Pedido"."""

    # ~~ Pass.
    pass

# ================================================== #

# ~~ Classe de erro quando não há instância do navegador armazenada.
class PedidoNavegadorError(PedidoError):

    """Subclasse para erros relacionados ao "Pedido"."""

    # ~~ Erro.
    def __init__(self, *args):

        """Quando não há navegador armazenado."""

        # ~~ Erro.
        super().__init__("Não há navegador armazenado.")

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

# ~~ Classe de erro quando não há vínculo com SAP criado.
class SapVinculoError(SapError):

    """Subclasse para erros relacionados ao "Sap"."""

    # ~~ Erro.
    def __init__(self, *args):

        """Quando não há vínculo com SAP criado."""

        # ~~ Erro.
        super().__init__("Não há vínculo com SAP criado.")

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