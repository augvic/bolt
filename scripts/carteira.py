# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Imports.
from scripts.utilitarios import Utilitarios
from scripts.excel import Excel

# ================================================== #

# ~~ Classe Carteira.
class Carteira:

    """
    Resumo:
    - Gerencia funções relacionadas à carteira.

    Atributos:
    - (carteira: Excel): Instância da classe "Excel" referenciando à carteira.
    - (utilitarios: Utilitarios): Instância da classe "Utilitarios" com funções auxiliares.

    Métodos:
    - (__init__): Cria atributos "carteira" e "utilitarios".
    - (importar_dados_financeiros_carteira): Importa dados financeiros na carteira.
    """

    # ================================================== #

    # ~~ Init.
    def __init__(self, utilitarios: Utilitarios, carteira: Excel):

        """
        Resumo:
        - Cria referência à planilha carteira e cria atributos "carteira" e "utilitarios".

        Parâmetros:
        - (utilitarios: Utilitarios): Instância da classe "Utilitarios".
        - (carteira: Excel): Instância da classe Excel.
        """

        # ~~ Utilitarios.
        self.utilitarios = utilitarios

        # ~~ Cria referência à carteira.
        self.carteira = carteira

    # ================================================== #

    # ~~ Importa dados financeiros na carteira.
    def importar_dados_financeiros_carteira(self, cliente: str, dados: dict) -> None:

        """
        Resumo:
        - Importa dados financeiros na carteira.
        
        Parâmetros:
        - (cliente: str): Código ERP.
        - (dados: dict): Dicionário contendo os dados financeiros.
        """

        # ~~ Salva planilha.
        self.carteira.salvar()

        # ~~ Coleta todas as linhas que o cliente está.
        linhas_carteira = self.carteira.localizar_index(aba="Carteira", coluna_nome="Código SAP", localizar=cliente, linha_cabecalho=16)

        # ~~ Para cada linha, importa os dados.
        for linha in linhas_carteira:
            self.carteira.inserir_dado(aba="Carteira", dado=dados["limite"], aba_nome="Carteira", coluna_nome="Limite", linha=linha, linha_cabecalho=16)
            self.carteira.inserir_dado(aba="Carteira", dado=dados["vencimento"], aba_nome="Carteira", coluna_nome="Vencimento Limite", linha=linha, linha_cabecalho=16)
            self.carteira.inserir_dado(aba="Carteira", dado=dados["margem"], aba_nome="Carteira", coluna_nome="Margem", linha=linha, linha_cabecalho=16)
            self.carteira.inserir_dado(aba="Carteira", dado=dados["nfs_vencidas"], aba_nome="Carteira", coluna_nome="Vencidos", linha=linha, linha_cabecalho=16)

    # ================================================== #