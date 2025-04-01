# ================================================== #

# ~~ Subindo para raiz do projeto.
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Bibliotecas.
import xlwings as xw
import time

# ================================================== #

# ~~ Cria instancia do Excel utilizando o xlwings.
def instanciar(diretorio_planilha: str, abas: list) -> dict:

    """
    Resumo:
    - Cria instancia do Excel.

    Parâmetros:
    - diretorio_planilha (str)
    - abas (list): Lista contendo o nome de cada aba.
    
    Retorna:
    - planilha (dict):
        - ["BOOK"] (xw.Book): Chave vinculada diretamente à planilha.
        - [abas] (xw.sheets): Cada aba vinculada é uma chave.
    
    Exceções:
    - ===
    """

    # ~~ Dicionário para armazenar planilha e abas.
    planilha = {}

    # ~~ Armazena planilha.
    planilha["BOOK"] = xw.Book(diretorio_planilha)

    # ~~ Armazena abas.
    for aba in abas:
        planilha[aba] = planilha["BOOK"].sheets[aba]

    # ~~ Retorna planilha e abas.
    return planilha

# ================================================== #

# ~~ Insere dados na planilha.
def inserir_dados(planilha: xw.Book, dado: any, aba_nome: str, coluna_nome: str, linha: int, linha_cabecalho: int) -> None:

    """
    Resumo:
    - Insere dados na planilha.
    
    Parâmetros:
    - planilha (xw.Book)
    - dado (any): Dado que será inserido na célula.
    - aba_nome (str): Nome da aba que será incluído o dado.
    - coluna_nome (str): Nome da coluna que será incluído o dado.
    - linha (int): Número da linha que será incluído o dado.
    - linha_cabecalho (int): Número da linha que está o cabeçalho (nome das colunas).
    
    Retorna:
    - ===
    
    Exceções:
    - "Coluna '{coluna_nome} não encontrada na aba '{aba_nome}'." 
    """

    # ~~ Cria lista de colunas de A à Z e depois concatena com outra lista de AA à AZ.
    letras = [chr(65 + i) for i in range(26)] + [f"A{chr(65 + i)}" for i in range(26)]

    # ~~ Cria dicionário com a chave sendo a "coluna" e o valor sendo a "letra".
    colunas = {
        planilha[aba_nome].range(f"{letra}{linha_cabecalho}").value: letra for letra in letras
    }

    # ~~ Coleta indice da coluna passado como parâmetro.
    coluna_a_ser_usada = colunas.get(coluna_nome)
    if not coluna_a_ser_usada:
        raise Exception(f"Coluna '{coluna_nome} não encontrada na aba '{aba_nome}'.")

    # ~~ Insere dado.
    planilha[aba_nome].range(f"{coluna_a_ser_usada}{linha}").value = dado

# ================================================== #

# ~~ Coleta dados da planilha.
def coletar_dados(planilha: xw.Book, aba_nome: str, coluna_nome: str, linha: int, linha_cabecalho: int) -> any:

    """
    Resumo:
    - Coleta dados da planilha.
    
    Parâmetros:
    - planilha (xw.Book)
    - dado (any): Dado que será coletado da célula.
    - aba_nome (str): Nome da aba que será coletado o dado.
    - coluna_nome (str): Nome da coluna que será coletado o dado.
    - linha (int): Número da linha que será coletado o dado.
    - linha_cabecalho (int): Número da linha que está o cabeçalho (nome das colunas).
    
    Retorna:
    - dado (any): Pode ser str, int, float, datetime, etc.
    
    Exceções:
    - "Coluna '{coluna_nome} não encontrada na aba '{aba_nome}'."
    """

    # ~~ Cria lista de colunas de A à Z e depois concatena com outra lista de AA à AZ.
    letras = [chr(65 + i) for i in range(26)] + [f"A{chr(65 + i)}" for i in range(26)]

    # ~~ Cria dicionário com a chave sendo a "coluna" e o valor sendo a "letra".
    colunas = {
        planilha[aba_nome].range(f"{letra}{linha_cabecalho}").value: letra for letra in letras
    }

    # ~~ Coleta indice da coluna passado como parâmetro.
    coluna_a_ser_usada = colunas.get(coluna_nome)
    if not coluna_a_ser_usada:
        raise Exception(f"Coluna '{coluna_nome} não encontrada na aba '{aba_nome}'.")

    # ~~ Coleta dado.
    dado = planilha[aba_nome].range(f"{coluna_a_ser_usada}{linha}").value

    # ~~ Retorna dado.
    return dado

# ================================================== #

# ~~ Salva planilha.
def salvar_planilha(planilha: xw.Book) -> None:

    """
    Resumo:
    - Salva a planilha.
    
    Parâmetros:
    - planilha (xw.Book)
    
    Retorna:
    - ===
    
    Exceções:
    - "Erro ao salvar planilha."
    """

    # ~~ Tenta salvar até 10x.
    tentativa = 0
    while tentativa != 10:
        try:
            planilha["BOOK"].save()
            return
        except:
            tentativa += 1
            time.sleep(2)
    
    # ~~ Se chegou ao limite de tentativas, exibe erro.
    if tentativa == 10:
        raise Exception("Erro ao salvar planilha.")

# ================================================== #

# ~~ Coleta última linha preenchida na coluna.
def ultima_linha_preenchida(planilha: xw.Book, aba: str, coluna: str) -> int:

    """
    Resumo:
    - Retorna última linha preenchida na coluna.

    Parâmetros:
    - planilha (xw.Book)
    - aba (str)
    - coluna (str): "A", "B", "C", etc.
    
    Retorna:
    - ultima_linha (int)

    Exceções:
    - ===
    """

    # ~~ Coleta última linha.
    ultima_linha = planilha[aba].range(coluna + str("99999")).end("up").row

    # ~~ Retorna.
    return ultima_linha

# ================================================== #