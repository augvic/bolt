# ================================================== #

# ~~ Classe base para erros relacionados ao "BasesHandler".
class BasesHandlerError(Exception):

    """Classe base para erros relacionados ao "BasesHandler"."""

    # ~~ Pass.
    pass

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

# ~~ Classe base de erros relacionados ao Navegador.
class NavegadorError(Exception):

    """Classe base para erros do Navegador."""

    # ~~ Pass.
    pass

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