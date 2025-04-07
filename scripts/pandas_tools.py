# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Bibliotecas.
import pandas
from scripts.erros import *

# ================================================== #

# ~~ Classe PandasTools.
class PandasTools:

    """
    Resumo:
    - Classe com métodos auxiliares que utilizam pandas.

    Métodos:
    - (localizar_index): Lê planilha e localiza index de um dado.
    - (criar_df_planilha): Faz leitura de aba da planilha e salva como DataFrame.
    """

    # ================================================== #

    # ~~ Utiliza pandas para ler planilha e localizar o index de um dado.
    def localizar_index(df: pandas.DataFrame, coluna_nome: str, localizar: str, linha_cabecalho: int) -> list:

        """
        Resumo:
        - Utiliza pandas para ler planilha e localizar o index de um dado.

        Parâmetros:
        - (df: DataFrame)
        - (coluna_nome: str): Nome da coluna onde irá ser procurado o dado.
        - (localizar: str): Dado que será localizado.
        - (linha_cabecalho: int): Linha que contém o cabeçalho na aba (nome das colunas).
        
        Retorna:
        - (linhas: list): Números das linhas onde o dado foi localizado. Podendo ser uma ou mais.

        Exceções:
        - (PandasToolsDadoError): Quando dado não foi encontrado.
        """

        # ~~ Localiza dado.
        linhas = df.index[df[coluna_nome] == str(localizar)].tolist()

        # ~~ Se não localizar dado, retorna erro.
        if not linhas:
            raise PandasToolsDadoError()
        
        # ~~ Itera linhas do dataframe para corresponder as linhas da planilha.
        linhas = [linha + 1 + linha_cabecalho for linha in linhas]

        # ~~ Retorna números das linhas.
        return linhas

    # ================================================== #

    # ~~ Faz leitura de aba da planilha e salva como DataFrame.
    def criar_df_planilha(diretorio_planilha: str, aba: str, linha_cabecalho: int, colunas_nomes: list = None) -> pandas.DataFrame:

        """
        Resumo:
        - Faz leitura de aba da planilha e salva como DataFrame.

        Parâmetros:
        - (diretorio_planilha: str)
        - (aba: str): Nome da aba para ser transformada em DataFrame.
        - (linha_cabecalho: int): Linha que contém o cabeçalho na aba (nome das colunas).
        - (colunas_nomes: list | opcional): Se passado lista com nomes de colunas específicas, cria DataFrame apenas delas.
        
        Retorna:
        - (df: DataFrame)

        Exceções:
        - (PandasToolsPlanilhaError): Quando diretório da planilha não foi encontrado.
        """

        # ~~ Lê planilha e cria DataFrame.
        try:
            df = pandas.read_excel(io=diretorio_planilha, sheet_name=aba, dtype=str, skiprows=linha_cabecalho-1, usecols=colunas_nomes)
        except:
            raise PandasToolsPlanilhaError()

        # ~~ Retorna DataFrame.
        return df

    # ================================================== #

# ================================================== #