# ================================================== #

# ~~ Subindo para raiz do projeto.
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Bibliotecas.
import pandas

# ================================================== #

# ~~ Utiliza pandas para ler planilha e localizar o index de um dado.
def localizar_index(df: pandas.DataFrame, coluna_nome: str, localizar: str, linha_cabecalho: int) -> list:

    """
    Resumo:
    - Utiliza pandas para ler planilha e localizar o index de um dado.

    Parâmetros:
    - df (DataFrame)
    - coluna_nome (str): Nome da coluna onde irá ser procurado o dado.
    - localizar (str): Dado que será localizado.
    - linha_cabecalho (int): Linha que contém o cabeçalho na aba (nome das colunas).
    
    Retorna:
    - linhas (list): Números das linhas onde o dado foi localizado. Podendo ser uma ou mais.

    Exceções:
    - "Dado não localizado."
    """

    # ~~ Localiza dado.
    linhas = df.index[df[coluna_nome] == str(localizar)].tolist()

    # ~~ Se não localizar dado, retorna erro.
    if not linhas:
        raise Exception("Dado não localizado.")
    
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
    - diretorio_planilha (str)
    - aba (str): Nome da aba para ser transformada em DataFrame.
    - linha_cabecalho (int): Linha que contém o cabeçalho na aba (nome das colunas).
    - colunas_nomes (list | opcional): Se passado lista com nomes de colunas específicas, cria DataFrame apenas delas.
    
    Retorna:
    - df (DataFrame)

    Exceções:
    - ===
    """

    # ~~ Lê planilha e cria DataFrame.
    df = pandas.read_excel(io=diretorio_planilha, sheet_name=aba, dtype=str, skiprows=linha_cabecalho-1, usecols=colunas_nomes)

    # ~~ Retorna DataFrame.
    return df

# ================================================== #