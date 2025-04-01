# ================================================== #

# ~~ Bibliotecas.
import pandas_tools
import excel
import pandas
import os
import requests
import urllib3
import unicodedata
import locale
import re
import sys
from datetime import datetime
from tabulate import tabulate
from dotenv import load_dotenv
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table

# ================================================== #

# ~~ Variáveis de ambiente.
load_dotenv()

# ================================================== #

# ~~ Função de consulta de dados da Receita Federal.
def consultar_receita_federal(cnpj: str, printar_dados: bool = False, log_path: str = None) -> dict:

    """
    Resumo:
    - Consulta a API da Receita Federal e obtém dados de um CNPJ.

    Parâmetros:
    - cnpj (str)
    - log_path (str | opcional): Caso passado um diretório, transfere texto printado para um arquivo ".txt". O parâmetro "printar_dados" deve ser True. 
    - printar_dados (bool):
        - False: Padrão.
        - True: Printa todos os dados.

    Retorna:
    - resposta_json (dict):
        - ["cnpj"] (str)
        - ["razao_social"] (str)
        - ["nome_fantasia"] (str) ou (str: "-")
        - ["natureza_juridica"] (str)
        - ["situacao_cadastral"] (str)
        - ["logradouro"] (str)
        - ["numero"] (str)
        - ["complemento"] (str) ou (str: "-")
        - ["bairro"] (str)
        - ["cep"] (str)
        - ["cidade"] (str)
        - ["estado"] (str): Estado em sigla.
        - ["telefone"] (str)
        - ["email"] (str) ou (str: "-")
        - ["recebimento_comissao"] (str):
            - "OK"
            - "NÃO OK"
        - ["regime_tributario"] (str):
            - "SIMPLES"
            - "LUCRO PRESUMIDO"
            - "LUCRO REAL"
        - ["inscricoes_estaduais"] (list) ou (str: "ISENTO"): Lista contendo todas as inscrições. Cada item possui as chaves:
            - ["inscricao_estadual"] (str)
            - ["situacao"] (str)
        - ["inscricoes_suframa"] (list) ou (str: "ISENTO"): Lista contendo todas as inscrições. Cada item possui as chaves:
            - ["inscricao_suframa"] (str)
            - ["situacao"] (str)
        - ["cnae"] (list): Lista contendo todos os CNAE. Cada item possui as chaves:
            - ["cnae"] (str)
            - ["descricao"] (str)

    Exceções:
    - "Erro na resposta da requisição.": Erro no retorno da requisição à API.
    - "Erro ao fazer requisição.": Erro a fazer requisição à API.
    """

    # Suprime avisos de SSL.
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # ~~ Url da API e autorização.
    url = f"https://comercial.cnpj.ws/cnpj/{cnpj}"
    headers = {
        "x_api_token": os.getenv("API_KEY")
    }

    # ~~ Requisição.
    try:
        resposta = requests.get(url=url, headers=headers, verify=False)
    except Exception as erro:
        raise Exception(f"Erro ao fazer requisição: {erro}.")

    # ~~ Verifica resposta.
    if resposta.status_code == 200:

        # ~~ Converte para JSON.
        resposta_json = resposta.json()

        # ~~ Cria dicionário para armazenar dados.
        dados = {}

        # ~~ Coleta CNPJ.
        dados["cnpj"] = resposta_json["estabelecimento"]["cnpj"]

        # ~~ Coleta razão social.
        dados["razao_social"] = formatar_texto(resposta_json["razao_social"])

        # ~~ Coleta nome fantasia.
        dados["nome_fantasia"] = formatar_texto(resposta_json["estabelecimento"]["nome_fantasia"]) if resposta_json["estabelecimento"]["nome_fantasia"] else "-"

        # ~~ Coleta natureza jurídica.
        dados["natureza_juridica"] = formatar_texto(resposta_json["natureza_juridica"]["descricao"])
        dados["natureza_juridica_id"] = resposta_json["natureza_juridica"]["id"]

        # ~~ Situação cadastral.
        dados["situacao_cadastral"] = formatar_texto(resposta_json["estabelecimento"]["situacao_cadastral"])

        # ~~ Coleta rua.
        dados["logradouro"] = formatar_texto(resposta_json["estabelecimento"]["logradouro"])

        # ~~ Coleta número.
        dados["numero"] = resposta_json["estabelecimento"]["numero"]

        # ~~ Coleta complemento.
        dados["complemento"] = re.sub(r"\s+", " ", formatar_texto(resposta_json["estabelecimento"]["complemento"])) if resposta_json["estabelecimento"]["complemento"] else "-"

        # ~~ Coleta bairro.
        dados["bairro"] = formatar_texto(resposta_json["estabelecimento"]["bairro"])

        # ~~ Coleta CEP.
        dados["cep"] = f"{resposta_json["estabelecimento"]["cep"][:5]}-{resposta_json["estabelecimento"]["cep"][5:]}"

        # ~~ Coleta cidade.
        dados["cidade"] = formatar_texto(resposta_json["estabelecimento"]["cidade"]["nome"])

        # ~~ Coleta sigla do estado.
        dados["estado"] = formatar_texto(resposta_json["estabelecimento"]["estado"]["sigla"])

        # ~~ Coleta telefone.
        dados["telefone"] = f"{resposta_json["estabelecimento"]["ddd1"]}{resposta_json["estabelecimento"]["telefone1"]}"

        # ~~ Coleta e-mail.
        dados["email"] = formatar_texto(resposta_json["estabelecimento"]["email"]) if resposta_json["estabelecimento"]["email"] else "-"

        # ~~ Coleta inscrições estaduais.
        dados["inscricoes_estaduais"] = [
            {
                "inscricao_estadual": inscricao["inscricao_estadual"],
                "situacao": "HABILITADA" if inscricao["ativo"] else "NÃO HABILITADA"
            }
            for inscricao in resposta_json["estabelecimento"]["inscricoes_estaduais"]
        ] if resposta_json["estabelecimento"]["inscricoes_estaduais"] else "ISENTO"

        # ~~ Coleta inscrições suframa.
        dados["inscricoes_suframa"] = [
            {
                "inscricao_suframa": inscricao["inscricao_suframa"],
                "situacao": "HABILITADA" if inscricao["ativo"] else "NÃO HABILITADA"
            }
            for inscricao in resposta_json["estabelecimento"]["inscricoes_suframa"]
        ] if resposta_json["estabelecimento"]["inscricoes_suframa"] else "ISENTO"

        # ~~ Coleta regime.
        try:
            regime = resposta_json["simples"]["simples"]
        except:
            regime = "Não"
        if regime == "Sim":
            dados["regime_tributario"] = {"regime_tributario": "SIMPLES", "ano": "-"}
        else:
            dados["regime_tributario"] = [
                {
                    "ano": regime["ano"],
                    "regime_tributario": regime["regime_tributario"]
                }
                for regime in resposta_json["estabelecimento"]["regimes_tributarios"]
            ]
            if dados["regime_tributario"]:
                dados["regime_tributario"] = max(dados["regime_tributario"], key=lambda x: x["ano"])
            else:
                dados["regime_tributario"] = {"regime_tributario": "LUCRO", "ano": "-"}
        
        # ~~ CNAE.
        dados["cnae"] = [
            {
                "cnae": cnae["classe"],
                "descricao": cnae["descricao"]
            }
            for cnae in resposta_json["estabelecimento"]["atividades_secundarias"]
        ]

        # ~~ Recebimento comissão.
        cnae_comissao = ["45.12-9", "45.30-7", "45.42-1", "46.11-7", "46.12-5", "46.13-3", "46.14-1", "46.15-0", "46.16-8", "46.17-6", "46.18-4", "46.19-2", "66.19-3"]
        dados["recebimento_comissao"] = "NÃO OK"
        for cnae in dados["cnae"]:
            if cnae["cnae"] in cnae_comissao:
                dados["recebimento_comissao"] = "OK"

        # ~~ Printa dados.
        if printar_dados == True:

            # ~~ Data e hora.
            printar_mensagem(mostrar_data_hora="Only", log_path=log_path)

            # ~~ Dados básicos.
            printar_mensagem(mensagem=f"CNPJ: {dados["cnpj"]}", mostrar_data_hora="False", log_path=log_path)
            printar_mensagem(mensagem=f"Razão Social: {dados["razao_social"]}", mostrar_data_hora="False", log_path=log_path)
            printar_mensagem(mensagem=f"Nome Fantasia: {dados["nome_fantasia"]}", mostrar_data_hora="False", log_path=log_path)
            printar_mensagem(mensagem=f"Natureza Jurídica: {dados["natureza_juridica_id"]} | {dados["natureza_juridica"]}", mostrar_data_hora="False", log_path=log_path)
            printar_mensagem(mensagem=f"Situação Cadastral: {dados["situacao_cadastral"]}", mostrar_data_hora="False", log_path=log_path)
            printar_mensagem(mensagem=f"Endereço Completo: {dados["logradouro"]}, {dados["numero"]} | {dados["complemento"]} | {dados["bairro"]} | {dados["cep"]} | {dados["cidade"]} | {dados["estado"]}", mostrar_data_hora="False", log_path=log_path)
            printar_mensagem(mensagem=f"Telefone: {dados["telefone"]}", mostrar_data_hora="False", log_path=log_path)
            printar_mensagem(mensagem=f"E-mail: {dados["email"]}", mostrar_data_hora="False", log_path=log_path)
            printar_mensagem(mensagem=f"Regime Tributário: {dados["regime_tributario"]["regime_tributario"]}", mostrar_data_hora="False", log_path=log_path)
            printar_mensagem(mensagem=f"Recebimento Comissão: {dados["recebimento_comissao"]}", mostrar_data_hora="False", log_path=log_path)

            # ~~ Inscrições estaduais.
            printar_mensagem(mensagem="Inscrições Estaduais:", mostrar_data_hora="False", log_path=log_path)
            if dados["inscricoes_estaduais"] != "ISENTO":
                for inscricao in dados["inscricoes_estaduais"]:
                    printar_mensagem(mensagem=f"    {inscricao["inscricao_estadual"]} | {inscricao["situacao"]}", mostrar_data_hora="False", log_path=log_path)
            else:
                printar_mensagem(mensagem=f"    {dados["inscricoes_estaduais"]}", mostrar_data_hora="False", log_path=log_path)

            # ~~ Inscrições suframa.
            printar_mensagem(mensagem="Inscrições Suframa:", mostrar_data_hora="False", log_path=log_path)
            if dados["inscricoes_suframa"] != "ISENTO":
                for inscricao in dados["inscricoes_suframa"]:
                    printar_mensagem(f"    {inscricao["inscricao_suframa"]} | {inscricao["situacao"]}", mostrar_data_hora="False", log_path=log_path)
            else:
                printar_mensagem(mensagem=f"    {dados["inscricoes_suframa"]}", mostrar_data_hora="False", log_path=log_path)

            # ~~ CNAE.
            printar_mensagem(mensagem="CNAE:", mostrar_data_hora="False", log_path=log_path)
            for cnae in dados["cnae"]:
                printar_mensagem(f"    {cnae["cnae"]} | {cnae["descricao"]}", mostrar_data_hora="False", log_path=log_path)

            # ~~ Fim.
            printar_mensagem(char_type="=", char_qtd=50)

        # ~~ Retorna dados.
        return dados
    
    # ~~ Em caso de de erro na resposta.
    else:
        printar_mensagem(mensagem=f"Erro: {resposta.status_code}", char_type="=", char_qtd=50, char_side="bot")
        raise Exception(f"Erro na resposta da requisição: {resposta.status_code} - {resposta.text}.")

# ================================================== #

# ~~ Coleta os diretórios definidos.
def diretorios(diretorio: str) -> str:

    """
    Resumo:
    - Retorna diretorio do arquivo escolhido.
    
    Parâmetros:
    - diretorio (str):
        - "carteira"
        - "base_revendas"
        - "base_cadastros"
    
    Retorna:
    - diretorio_escolhido (str)
    
    Exceções:
    - ===
    """

    # ~~ Carteira.
    if diretorio == "carteira":
        data = coletar_data_atual()
        matrícula = coletar_matricula()
        diretorio_escolhido = fr"C:\Users\{matrícula}\OneDrive - Positivo\Documentos - Carteira_Faturamento\Carteira_Status {data["mes_extenso"]} {data["dia_numero"]}{data["mes_numero"]}.xlsm"

    # ~~ Base Revendas.
    if diretorio == "base_revendas":
        diretorio_escolhido = r"N:\NNPI\NN\Projeto Vendas 1 a 1\Cadastros Clientes\Base Consolidada de REVENDAS.xlsx"

    # ~~ Base Cadastros.
    if diretorio == "base_cadastros":
        diretorio_escolhido = r"N:\NNPI\NN\Projeto Vendas 1 a 1\Cadastros Clientes\Base de Novos Cadastros.xlsx"

    # ~~ Retorna.
    return diretorio_escolhido

# ================================================== #

# ~~ Verifica se data de boleto está vencido.
def verificar_vencimento_boleto(data_boleto: str) -> str:

    """
    Resumo:
    - Verifica se data de vencimento da nota está vencida ou não.
    
    Parâmetros:
    - data (str): Data para verificar se está vencida.
    
    Retorna:
    - resultado (str): Pode ser as opções abaixo. 
        - "Vencido"
        - "Não vencido"
    
    Exceções:
    - ===
    """

    # ~~ Converte data do boleto passada como parâmetro de "str" para "datetime".
    data_boleto = datetime.strptime(data_boleto, "%d/%m/%Y").date()

    # ~~ Coleta data atual.
    data_atual = datetime.now().date()

    # ~~ Verifica se data do boleto é menor que data atual. Se for menor, é vencido. Se for maior, não é.
    if data_boleto < data_atual:

        # ~~ Incrementa 1 dia a mais na "data_boleto" até ele chegar na data atual, ignorando sábados e domingos, contando há quantos dias está vencido.
        dias_vencidos = 0
        data_boleto = data_boleto + timedelta(days=1)
        while data_boleto < data_atual:
            if data_boleto.weekday() < 5:
                dias_vencidos += 1
            data_boleto = data_boleto + timedelta(days=1)

        # ~~ Se os dias vencidos forem iguais ou maior a 2, então o boleto está vencido de fato. Caso não, não é considerado vencido.
        if dias_vencidos >= 2:
            return "Vencido"
        else:
            return "Não vencido"
        
    # ~~ Caso a data do boleto seja maior que a data atual, não é vencido.
    else:
        return "Não vencido"

# ================================================== #

# ~~ Função customizada para printar mensagens.
def printar_mensagem(mensagem: str = None, char_type: str = None, char_qtd: int = None, char_side: str = None, log_path: str = None, mostrar_data_hora: str = "True") -> None:

    """
    Resumo:
    - Printa mensagem ou caractere especial no terminal.
    
    Parâmetros:
    - mensagem (str | opcional): Texto que será printado no terminal.
    - char_type: (str | opcional): Tipo de caractere a ser printado.
    - char_qtd: (int | opcional): Quantidade do caractere.
    - char_side: (str | opcional): Lado que será printado, podendo ser as opções abaixo.
        - "top": Cima
        - "bot": Baixo
        - "both": Ambos
    - log_path (str | opcional): Caso passado um diretório, transfere texto printado para um arquivo ".txt". 
    - mostar_data_hora (str | opcional): 
        - "True" Padrão
        - "False": Para não mostrar data e hora.
        - "Only": Para printar somente a data.
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Coleta data e hora atual.
    data_hora_atual = datetime.now().replace(microsecond = 0)
    data_hora_atual = data_hora_atual.strftime("%d/%m/%Y_%H:%M")

    # ~~ Se for para direcionar output à um arquivo ".txt".
    if log_path:
        log = open(log_path, "a", encoding="utf-8")

    # ~~ Se for somente para printar a data:
    if mostrar_data_hora == "Only":
        print(f"<{data_hora_atual}>")
        if log_path:
            log.write(f"<{data_hora_atual}>" + "\n")
        return

    # ~~ Se tiver mensagem.
    if mensagem:

        # ~~ Se tiver mensagem e char_type, verifica o lado a ser printado.
        if char_type:
            if char_side == "top":
                print(char_type*char_qtd)
                if mostrar_data_hora == "True":
                    print(f"<{data_hora_atual}>")
                print(mensagem)
                if log_path:
                    log.write(char_type*char_qtd + "\n")
                    if mostrar_data_hora == "True":
                        log.write(f"<{data_hora_atual}>" + "\n")
                    log.write(f"<{mensagem}>" + "\n")
            if char_side == "bot":
                if mostrar_data_hora == "True":
                    print(f"<{data_hora_atual}>")
                print(mensagem)
                print(char_type*char_qtd)
                if log_path:
                    if mostrar_data_hora == "True":
                        log.write(f"<{data_hora_atual}>" + "\n")
                    log.write(mensagem + "\n")
                    log.write(char_type*char_qtd + "\n")
            if char_side == "both":
                print(char_type*char_qtd)
                if mostrar_data_hora == "True":
                    print(f"<{data_hora_atual}>")
                print(mensagem)
                print(char_type*char_qtd)
                if log_path:
                    log.write(char_type*char_qtd + "\n")
                    if mostrar_data_hora == "True":
                        log.write(f"<{data_hora_atual}>" + "\n")
                    log.write(mensagem + "\n")
                    log.write(char_type*char_qtd + "\n")

        # ~~ Se não tiver char_type, printa somente mensagem.
        else:
            if mostrar_data_hora == "True":
                print(f"<{data_hora_atual}>")
            print(mensagem)
            if log_path:
                if mostrar_data_hora == "True":
                    log.write(f"<{data_hora_atual}>" + "\n")
                log.write(mensagem + "\n")
    
    # ~~ Se não tiver mensagem, printa somente char_type.
    else:
        print(char_type*char_qtd)
        if log_path:
            log.write(char_type*char_qtd + "\n")

# ================================================== #

# ~~ Printar DataFrame.
def printar_dataframe(df: pandas.DataFrame, log_path: str = None) -> None:

    """
    Resumo:
    - Printa DataFrame em formato de tabela.
    
    Parâmetros:
    - df (DataFrame): DataFrame do pandas.
    - log_path (str | opcional): Caso passado um diretório, transfere texto printado para um arquivo ".txt". 
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Instancia console do rich.
    console = Console()

    # ~~ Cria tabela.
    tabela = Table(show_header=True, header_style="bold blue")

    # ~~ Adiciona colunas.
    for coluna in df.columns:
        tabela.add_column(coluna)

    # ~~ Adiciona linhas.
    for _, linha in df.iterrows():
        tabela.add_row(*map(str, linha.values), end_section=True)

    # ~~ Printa tabela usando o console.
    console.print(tabela)

    # ~~ Se for para direcionar output à um arquivo ".txt".
    if log_path:

        # ~~ Usa tabulate, pois rich exporta tabela com ANSI e arquivo ".txt" não suporta.
        tabela_txt = tabulate(df, headers="keys", tablefmt="grid", showindex=False)

        # ~~ Escreve no arquivo.
        log = open(log_path, "a", encoding="utf-8")
        log.write(tabela_txt + "\n")

# ================================================== #

# ~~ Remove acentos e converte tudo para maiúsculas.
def formatar_texto(texto: str) -> str:

    """
    Resumo:
    - Remove acentos e converte tudo para maiúsculas.
    
    Parâmetros:
    - texto (str): Texto para formatar.
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Verifica se é str passada no parâmetro.
    if isinstance(texto, str):
        
        # ~~ Remove acentos.
        texto_formatado = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")

        # ~~ Converte para maiúsculas.
        texto_formatado = texto_formatado.upper()

        # ~~ Retorna texto formatado.
        return texto_formatado

    # ~~ Caso não seja str, retorna o mesmo valor.
    else:
        return texto

# ================================================== #

# ~~ Retorna as informações de data e mês atuais.
def coletar_data_atual() -> dict:

    """
    Resumo:
    - Retorna as informações de data, mês e ano atuais.
    
    Parâmetros:
    - ===
    
    Retorna:
    - data (dict): Dicionário contendo os dados abaixo.
        - ["dia_numero"] (str): O dia em seu formato numérico.
        - ["mes_numero"] (str): O mês em seu formato numérico.
        - ["ano"] (str): O ano em str.
        - ["hora"] (str): Hora no formato "%H-%M".
        - ["data_com_hora"] (str): Data e hora no formato "%d-%m-%Y_%H-%M".
        - ["dia_extenso"] (str): O dia em seu formato extenso.
        - ["mes_extenso"] (str): O mês em seu formato extenso.
    
    Exceções:
    - ===
    """

    # ~~ Define local para PT-BR no modelo UTF-8 para puxar acentuação e caracteres latinos.
    locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')

    # ~~ Cria dicionário.
    data = {}

    # ~~ Coleta dia, mês e ano.
    data["dia_numero"] = datetime.now().strftime("%d")
    data["mes_numero"] = datetime.now().strftime("%m")
    data["ano"] = datetime.now().strftime("%Y")
    data["hora"] = datetime.now().replace(microsecond=0).strftime("%H-%M")
    data["data_com_hora"] = datetime.now().replace(microsecond=0).strftime("%d-%m-%Y_%H-%M")

    # ~~ Converte para extenso.
    data["dia_extenso"] = datetime.now().strftime("%A").upper()
    data["mes_extenso"] = datetime.now().strftime("%B").upper()

    # ~~ Retorna dados.
    return data

# ================================================== #

# ~~ Retorna a matrícula do usuário.
def coletar_matricula() -> str:

    """
    Resumo:
    - Retorna a matrícula do usuário.
    
    Parâmetros:
    - ===
    
    Retorna:
    - matricula (str): Matrícula.
    
    Exceções:
    - ===
    """

    # ~~ Coleta matrícula.
    matrícula = os.getlogin()

    # ~~ Retorna.
    return matrícula

# ================================================== #

# ~~ Extrai data de string.
def extrair_data_da_string(string: str) -> str:

    """
    Resumo:
    - Extrai data de string.
    
    Parâmetros:
    - string (str): Texto para extrair a data.
    
    Retorna:
    - data (str): Data no formato string. Exemplo: "DD/MM/AA".
    
    Exceções:
    - ===
    """

    # ~~ Remove letras e caracteres especiais.
    nova_string = re.sub(r"\D", "", string)

    # ~~ Se quantidade de números for 6, converte ano para o formato "AAAA".
    if len(nova_string) == 6:
        dia, mes, ano = nova_string[:2], nova_string[2:4], nova_string[4:]
        ano = f"20{ano}"
        return f"{dia}/{mes}/{ano}"
    
    # ~~ Sendo 8 números.
    elif len(nova_string) == 8:
        return f"{nova_string[:2]}/{nova_string[2:4]}/{nova_string[4:]}"
    
    # ~~ Não sendo quantidade de números para formar data, retorna string passada no parâmetro.
    else:
        return string

# ================================================== #

# ~~ Obtém diretório do script que está sendo executado.
def obter_diretorio_atual() -> str:

    """
    Resumo:
    - Obtém diretório do script que está sendo executado.
    
    Parâmetros:
    - ===
    
    Retorna:
    - diretório (str): Diretório do script que está sendo executado.
    
    Exceções:
    - ===
    """

    # ~~ Retorna diretório.
    return os.path.dirname(os.path.abspath(sys.argv[0]))

# ================================================== #

# ~~ Importa status de assinaturas nas bases (Base Cadastros / Base Revendas).
def importar_status_assinatura_bases(base: str, cnpj: str, status: str) -> None:

    """
    Resumo:
    - Importa status de assinaturas nas bases (Base Cadastros / Base Revendas).
    
    Parâmetros:
    - base (str):
        - "cadastros"
        - "revendas"
    - cnpj (str)
    - status (str)
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Com base no index escolhido, armazena qual base será atualizada.
    if base == "revendas":
        diretorio_planilha = diretorios("base_revendas")
        abas = ["Consolidado", "Status Assinatura"]
        aba_leitura = "Consolidado"
        linha_cabecalho = 3
        coluna = "CNPJ Cliente.1"
        coluna_importar = "STATUS DOC"
    else:
        diretorio_planilha = diretorios("base_cadastros")
        abas = ["BASE CADASTRO", "Status Assinatura"]
        aba_leitura = "BASE CADASTRO"
        linha_cabecalho = 1
        coluna = "CNPJ"
        coluna_importar = "STATUS"

    # ~~ Instancia planilha.
    planilha = excel.instanciar(diretorio_planilha, abas)

    # ~~ Faz leitura da aba planilha usando pandas para atualizar os status de forma otimizada.
    excel.salvar_planilha(planilha)
    df = pandas_tools.criar_df_planilha(diretorio_planilha=diretorio_planilha, aba=aba_leitura, linha_cabecalho=linha_cabecalho, colunas_nomes=[coluna])

    # ~~ Insere status na planilha, usando o data frame para localizar a linha correspondente.
    linhas = pandas_tools.localizar_index(df=df, coluna_nome=coluna, localizar=cnpj, linha_cabecalho=linha_cabecalho)
    for linha in linhas:
        excel.inserir_dados(planilha=planilha, dado=status, aba_nome=aba_leitura, coluna_nome=coluna_importar, linha=linha, linha_cabecalho=linha_cabecalho)

# ================================================== #

# ~~ Importa dados financeiros na carteira.
def importar_dados_financeiros_carteira(cliente: str, dados: dict) -> None:

    """
    Resumo:
    - Importa dados financeiros na carteira.
    
    Parâmetros:
    - cliente (str): Código ERP.
    - dados (dict): Dicionário contendo os dados financeiros.
    
    Retorna:
    - ===
    
    Exceções:
    - ===
    """

    # ~~ Define caminho da Carteira mais atualizada.
    caminho_planilha = diretorios("carteira")

    # ~~ Vincula planilha.
    abas = ["Carteira", "Consultar Limites"]
    planilha = excel.instanciar(caminho_planilha, abas)

    # ~~ Faz leitura da planilha.
    excel.salvar_planilha(planilha)
    df = pandas_tools.criar_df_planilha(diretorio_planilha=caminho_planilha, aba="Carteira", linha_cabecalho=16, colunas_nomes=["Código SAP"])

    # ~~ Coleta todas as linhas que o cliente está.
    linhas_carteira = pandas_tools.localizar_index(df=df, coluna_nome="Código SAP", localizar=cliente, linha_cabecalho=16)

    # ~~ Para cada linha, importa os dados.
    for linha in linhas_carteira:
        excel.inserir_dados(planilha=planilha, dado=dados["limite"], aba_nome="Carteira", coluna_nome="Limite", linha=linha, linha_cabecalho=16)
        excel.inserir_dados(planilha=planilha, dado=dados["vencimento"], aba_nome="Carteira", coluna_nome="Vencimento Limite", linha=linha, linha_cabecalho=16)
        excel.inserir_dados(planilha=planilha, dado=dados["margem"], aba_nome="Carteira", coluna_nome="Margem", linha=linha, linha_cabecalho=16)
        excel.inserir_dados(planilha=planilha, dado=dados["nfs_vencidas"], aba_nome="Carteira", coluna_nome="Vencidos", linha=linha, linha_cabecalho=16)

# ================================================== #