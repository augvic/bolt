# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Imports.
import xlwings as xw
import time
import pandas
from scripts.erros import *

# ================================================== #

# ~~ Classe Excel.
class Excel:

    """
    Resumo:
    - Classe para manipulação de planilhas.

    Atributos:
    - (planilha: dict):
        - (BOOK: xw.Book): Chave referenciando diretamente à planilha.
        - (aba: xw.sheets): Cada aba é uma chave.

    Métodos:
    - (__init__): Cria atributo "planilha", fazendo referência à uma planilha Excel.
    - (inserir_dado): Insere dado em células da planilha.
    - (coletar_dado): Coleta dado de célula da planilha.
    - (salvar): Salva planilha.
    - (ultima_linha_preenchida): Retorna com o número da última linha preenchida na coluna específicada.
    - (localizar_index): Utiliza pandas para ler planilha e localizar o index de um dado.
    - (criar_df): Faz leitura de aba da planilha e salva como DataFrame.

    Exceções:
    - (ExcelError): Classe base.
    - (ExcelArquivoNaoEncontradoError): Quando arquivo do Excel não for encontrado.
    - (ExcelAbaNaoEncontradaError): Quando uma aba especificada não existe na planilha.
    - (ExcelColunaNaoEncontradaError): Quando uma coluna especificada não existe na aba.
    - (ExcelSalvarPlanilhaError): Quando não é possível salvar planilha.
    - (ExcelLocalizarDadoError): Quando dado para localizar não foi encontrado.
    """

    # ================================================== #

    # ~~ Cria referência à uma planilha do Excel.
    def __init__(self, diretorio_planilha: str, abas: list) -> None:

        """
        Resumo:
        - Cria referência à uma planilha do Excel.

        Parâmetros:
        - (diretorio_planilha: str): Caminho do arquivo Excel.
        - (abas: list): Lista com os nomes das abas que serão referenciadas.
        
        Atributos:
        - (planilha dict):
            - (BOOK: xw.Book): Chave referenciando diretamente à planilha.
            - (aba: xw.sheets): Cada aba é uma chave.

        Exceções:
        - (ExcelArquivoNaoEncontradoError): Quando arquivo do Excel não for encontrado.
        - (ExcelAbaNaoEncontradaError): Quando uma aba especificada não existe na planilha.
        """

        # ~~ Dicionário para armazenar planilha e abas.
        planilha = {}

        # ~~ Armazena planilha.
        try:
            planilha["BOOK"] = xw.Book(diretorio_planilha)
        except:
            raise ExcelArquivoNaoEncontradoError(diretorio_planilha)

        # ~~ Armazena abas.
        try:
            for aba in abas:
                planilha[aba] = planilha["BOOK"].sheets[aba]
        except:
            raise ExcelAbaNaoEncontradaError(aba, planilha["BOOK"].name)

        # ~~ Cria atributo com planilha e abas.
        self.planilha = planilha

    # ================================================== #

    # ~~ Insere dado em célula da planilha.
    def inserir_dado(self, aba_nome: str, linha_cabecalho: int, coluna_nome: str, linha: int, dado: any) -> None:

        """
        Resumo:
        - Insere dado em célula da planilha.
        
        Parâmetros:
        - (aba_nome: str): Nome da aba que será incluído o dado.
        - (linha_cabecalho: int): Número da linha que está o cabeçalho (nome das colunas).
        - (coluna_nome: str): Nome da coluna que será incluído o dado.
        - (linha: int): Número da linha que será incluído o dado.
        - (dado: any): Dado que será inserido na célula.
        
        Exceções:
        - (ExcelColunaNaoEncontradaError): Quando uma coluna especificada não existe na aba.
        """

        # ~~ Cria lista de colunas de A à Z e depois concatena com outra lista de AA à AZ.
        letras = [chr(65 + i) for i in range(26)] + [f"A{chr(65 + i)}" for i in range(26)]

        # ~~ Cria dicionário com a chave sendo a "coluna" e o valor sendo a "letra".
        colunas = {
            self.planilha[aba_nome].range(f"{letra}{linha_cabecalho}").value: letra for letra in letras
        }

        # ~~ Coleta indice da coluna passado como parâmetro.
        coluna_a_ser_usada = colunas.get(coluna_nome)
        if not coluna_a_ser_usada:
            raise ExcelColunaNaoEncontradaError(coluna_nome, aba_nome)

        # ~~ Insere dado.
        self.planilha[aba_nome].range(f"{coluna_a_ser_usada}{linha}").value = dado

    # ================================================== #

    # ~~ Coleta dado de célula da planilha.
    def coletar_dado(self, aba_nome: str, coluna_nome: str, linha_cabecalho: int, linha: int) -> any:

        """
        Resumo:
        - Coleta dado de célula da planilha.
        
        Parâmetros:
        - (aba_nome: str): Nome da aba que será coletado o dado.
        - (coluna_nome: str): Nome da coluna que será coletado o dado.
        - (linha_cabecalho: int): Número da linha que está o cabeçalho (nome das colunas).
        - (linha: int): Número da linha que será coletado o dado.
        
        Retorna:
        - (dado: any): Pode ser str, int, float, datetime, etc.

        Exceções:
        - (ExcelColunaNaoEncontradaError): Quando uma coluna especificada não existe na aba.
        """

        # ~~ Cria lista de colunas de A à Z e depois concatena com outra lista de AA à AZ.
        letras = [chr(65 + i) for i in range(26)] + [f"A{chr(65 + i)}" for i in range(26)]

        # ~~ Cria dicionário com a chave sendo a "coluna" e o valor sendo a "letra".
        colunas = {
            self.planilha[aba_nome].range(f"{letra}{linha_cabecalho}").value: letra for letra in letras
        }

        # ~~ Coleta indice da coluna passado como parâmetro.
        coluna_a_ser_usada = colunas.get(coluna_nome)
        if not coluna_a_ser_usada:
            raise ExcelColunaNaoEncontradaError(coluna_nome, aba_nome)

        # ~~ Coleta dado.
        dado = self.planilha[aba_nome].range(f"{coluna_a_ser_usada}{linha}").value

        # ~~ Retorna dado.
        return dado

    # ================================================== #

    # ~~ Salva planilha.
    def salvar(self) -> None:

        """
        Resumo:
        - Salva a planilha.

        Exceções:
        - (ExcelSalvarPlanilhaError): Quando não é possível salvar planilha.
        """

        # ~~ Tenta salvar até 10x.
        tentativa = 0
        while tentativa != 10:
            try:
                self.planilha["BOOK"].save()
                return
            except:
                tentativa += 1
                time.sleep(2)
        
        # ~~ Se chegou ao limite de tentativas, exibe erro.
        if tentativa == 10:
            raise ExcelSalvarPlanilhaError(self.planilha["BOOK"].name)

    # ================================================== #

    # ~~ Coleta última linha preenchida na coluna.
    def ultima_linha_preenchida(self, aba: str, coluna: str) -> int:

        """
        Resumo:
        - Retorna última linha preenchida na coluna.

        Parâmetros:
        - (aba: str): Nome da aba.
        - (coluna: str): "A", "B", "C", etc.

        Retorna:
        - (ultima_linha: int)

        Exceções:
        - (ExcelAbaNaoEncontradaError): Quando uma aba especificada não existe na planilha.
        - (ExcelColunaNaoEncontradaError): Quando uma coluna especificada não existe na aba.
        """

        # ~~ Coleta última linha.
        try:
            aba_object = self.planilha[aba]
        except:
            raise ExcelAbaNaoEncontradaError(aba, self.planilha["BOOK"].name)
        try:
            ultima_linha = aba_object.range(coluna + str("99999")).end("up").row
        except:
            raise ExcelColunaNaoEncontradaError(coluna, aba)

        # ~~ Retorna.
        return ultima_linha

    # ================================================== #

    # ~~ Utiliza pandas para ler planilha e localizar o index de um dado.
    def localizar_index(self, aba: str, coluna_nome: str, localizar: str, linha_cabecalho: int) -> list:

        """
        Resumo:
        - Utiliza pandas para ler planilha e localizar o index de um dado.

        Parâmetros:
        - (aba: str): Nome da aba.
        - (coluna_nome: str): Nome da coluna onde irá ser procurado o dado.
        - (localizar: str): Dado que será localizado.
        - (linha_cabecalho: int): Linha que contém o cabeçalho na aba (nome das colunas).
        
        Retorna:
        - (linhas: list): Números das linhas onde o dado foi localizado. Podendo ser uma ou mais.

        Exceções:
        - (ExcelLocalizarDadoError): Quando dado para localizar não foi encontrado.
        """

        # ~~ Cria df.
        df = self.criar_df(aba=aba, linha_cabecalho=linha_cabecalho)

        # ~~ Localiza dado.
        linhas = df.index[df[coluna_nome] == str(localizar)].tolist()

        # ~~ Se não localizar dado, retorna erro.
        if not linhas:
            raise ExcelLocalizarDadoError()
        
        # ~~ Itera linhas do dataframe para corresponder as linhas da planilha.
        linhas = [linha + 1 + linha_cabecalho for linha in linhas]

        # ~~ Retorna números das linhas.
        return linhas

    # ================================================== #

    # ~~ Faz leitura de aba da planilha e salva como DataFrame.
    def criar_df(self, aba: str, linha_cabecalho: int, colunas_nomes: list = None) -> pandas.DataFrame:

        """
        Resumo:
        - Faz leitura de aba da planilha e salva como DataFrame.

        Parâmetros:
        - (aba: str): Nome da aba para ser transformada em DataFrame.
        - (linha_cabecalho: int): Linha que contém o cabeçalho na aba (nome das colunas).
        - (colunas_nomes: list): Se passado lista com nomes de colunas específicas, cria DataFrame apenas delas.
        
        Retorna:
        - (df: DataFrame)
        """

        # ~~ Lê planilha e cria DataFrame.
        df = pandas.read_excel(io=self.planilha["BOOK"].fullname, sheet_name=aba, dtype=str, skiprows=linha_cabecalho-1, usecols=colunas_nomes)

        # ~~ Retorna DataFrame.
        return df

    # ================================================== #

# ================================================== #