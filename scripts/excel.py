# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# ================================================== #

# ~~ Imports.
import xlwings as xw
import time

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

        """Erro para quando arquivo do Excel não for encontrado."""

        super().__init__(f"Arquivo Excel não encontrado no caminho: '{caminho}'.")

# ================================================== #

# ~~ Classe de erro para aba não encontrada.
class AbaNaoEncontradaError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, aba, planilha):

        """Erro para quando uma aba especificada não existe na planilha."""

        super().__init__(f"Aba '{aba}' não existe na planilha '{planilha}'")

# ================================================== #

# ~~ Classe de erro para coluna não encontrada.
class ColunaNaoEncontradaError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, coluna, aba):

        """Erro para quando uma coluna especificada não existe na aba."""

        super().__init__(f"Coluna '{coluna}' não existe na aba '{aba}'")

# ================================================== #

# ~~ Classe de erro ao salvar planilha.
class SalvarPlanilhaError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, planilha):

        """Erro quando não é possível salvar planilha."""

        super().__init__(f"Não foi possível salvar a planilha {planilha}")

# ================================================== #

# ~~ Classe de erro quando não há planilha referenciada.
class PlanilhaReferenciadaError(ExcelError):

    """Subclasse para erros do Excel."""

    # ~~ Erro.
    def __init__(self, planilha):

        """Erro para quando não há planilha referenciada."""

        super().__init__(f"Sem planilha referenciada.")

# ================================================== #

# ~~ Classe Excel.
class Excel:

    """
    Resumo:
    - Classe para manipulação de planilhas.

    Atributos:
    - (planilha: dict):
        - (BOOK: xw.Book): Chave referenciando diretamente à planilha.
        - ({aba}: xw.sheets): Cada aba passada como parâmetro é uma chave.

    Métodos:
    - (referenciar): Cria atributo "planilha", fazendo referência à uma planilha Excel.
    - (inserir_dado): Insere dado em células da planilha.
    - (coletar_dado): Coleta dado de célula da planilha.
    - (salvar): Salva planilha.
    - (ultima_linha_preenchida): Retorna com o número da última linha preenchida na coluna específicada.
    """

    # ================================================== #

    # ~~ Atributos.
    planilha = None

    # ================================================== #

    # ~~ Cria referência à uma planilha do Excel.
    def referenciar(self, diretorio_planilha: str, abas: list) -> None:

        """
        Resumo:
        - Cria referência à uma planilha do Excel.

        Parâmetros:
        - (diretorio_planilha: str): Caminho do arquivo Excel.
        - (abas: list): Lista com os nomes das abas que serão referenciadas.
        
        Atributos:
        - (planilha dict):
            - (BOOK: xw.Book): Chave referenciando diretamente à planilha.
            - ({aba}: xw.sheets): Cada aba passada como parâmetro é uma chave.
        
        Retorna:
        - ===

        Exceções:
        - (ArquivoNaoEncontradoError)
        - (AbaNaoEncontradaError)
        """

        # ~~ Dicionário para armazenar planilha e abas.
        planilha = {}

        # ~~ Armazena planilha.
        try:
            planilha["BOOK"] = xw.Book(diretorio_planilha)
        except:
            raise ArquivoNaoEncontradoError(diretorio_planilha)

        # ~~ Armazena abas.
        try:
            for aba in abas:
                planilha[aba] = planilha["BOOK"].sheets[aba]
        except:
            raise AbaNaoEncontradaError(aba, planilha["BOOK"].name)

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
        
        Atributos:
        - ===

        Retorna:
        - ===
        
        Exceções:
        - (ColunaNaoEncontradaError)
        - (PlanilhaReferenciadaError)
        """

        # ~~ Se não tiver planilha referenciada.
        if self.planilha == None:
            raise PlanilhaReferenciadaError()

        # ~~ Cria lista de colunas de A à Z e depois concatena com outra lista de AA à AZ.
        letras = [chr(65 + i) for i in range(26)] + [f"A{chr(65 + i)}" for i in range(26)]

        # ~~ Cria dicionário com a chave sendo a "coluna" e o valor sendo a "letra".
        colunas = {
            self.planilha[aba_nome].range(f"{letra}{linha_cabecalho}").value: letra for letra in letras
        }

        # ~~ Coleta indice da coluna passado como parâmetro.
        coluna_a_ser_usada = colunas.get(coluna_nome)
        if not coluna_a_ser_usada:
            raise ColunaNaoEncontradaError(coluna_nome, aba_nome)

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
        
        Atributos:
        - ===
        
        Retorna:
        - (dado: any): Pode ser str, int, float, datetime, etc.

        Exceções:
        - (ColunaNaoEncontradaError)
        - (PlanilhaReferenciadaError)
        """

        # ~~ Se não tiver planilha referenciada.
        if self.planilha == None:
            raise PlanilhaReferenciadaError()

        # ~~ Cria lista de colunas de A à Z e depois concatena com outra lista de AA à AZ.
        letras = [chr(65 + i) for i in range(26)] + [f"A{chr(65 + i)}" for i in range(26)]

        # ~~ Cria dicionário com a chave sendo a "coluna" e o valor sendo a "letra".
        colunas = {
            self.planilha[aba_nome].range(f"{letra}{linha_cabecalho}").value: letra for letra in letras
        }

        # ~~ Coleta indice da coluna passado como parâmetro.
        coluna_a_ser_usada = colunas.get(coluna_nome)
        if not coluna_a_ser_usada:
            raise ColunaNaoEncontradaError(coluna_nome, aba_nome)

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
        
        Parâmetros:
        - ===

        Atributos:
        - ===
        
        Retorna:
        - ===
        
        Exceções:
        - (SalvarPlanilhaError)
        - (PlanilhaReferenciadaError)
        """

        # ~~ Se não tiver planilha referenciada.
        if self.planilha == None:
            raise PlanilhaReferenciadaError()

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
            raise SalvarPlanilhaError(self.planilha["BOOK"].name)

    # ================================================== #

    # ~~ Coleta última linha preenchida na coluna.
    def ultima_linha_preenchida(self, aba: str, coluna: str) -> int:

        """
        Resumo:
        - Retorna última linha preenchida na coluna.

        Parâmetros:
        - (aba: str): Nome da aba.
        - (coluna: str): "A", "B", "C", etc.
        
        Atributos:
        - ===

        Retorna:
        - (ultima_linha: int)

        Exceções:
        - (AbaNaoEncontradaError)
        - (ColunaNaoEncontradaError)
        - (PlanilhaReferenciadaError)
        """

        # ~~ Se não tiver planilha referenciada.
        if self.planilha == None:
            raise PlanilhaReferenciadaError()

        # ~~ Coleta última linha.
        try:
            aba_object = self.planilha[aba]
        except:
            raise AbaNaoEncontradaError(aba, self.planilha["BOOK"].name)
        try:
            ultima_linha = aba_object.range(coluna + str("99999")).end("up").row
        except:
            raise ColunaNaoEncontradaError(coluna, aba)

        # ~~ Retorna.
        return ultima_linha

    # ================================================== #

# ================================================== #