# ================================================== #

# ~~ Adiciona raiz ao path.
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ================================================== #

# ~~ Inicia setup Django.
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

# ================================================== #

# ~~ Bibliotecas.
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
from datetime import datetime
from rich.console import Console
from rich.table import Table
from scripts.erros import *
from django.db import connection

# ================================================== #

# ~~ Variáveis de ambiente.
load_dotenv()

# ================================================== #

# ~~ Classes utilitários.
class Utilitarios:

    """
    Resumo:
    - Controla funções utilitarias.

    Métodos:
    - (drop_table): Função para excluir tabelas do sqlite3.
    - (consultar_receita_federal): Consulta a API da Receita Federal e obtém dados de um CNPJ.
    - (diretorios): Retorna diretorio do arquivo escolhido.
    - (printar_mensagem): Printa mensagem ou caractere especial no terminal.
    - (printar_dataframe): Printa DataFrame em formato de tabela.
    - (formatar_texto): Remove acentos e converte tudo para maiúsculas.
    - (coletar_data_atual): Retorna as informações de data, mês e ano atuais.
    - (coletar_matricula): Retorna a matrícula do usuário.
    - (extrair_data_da_string): Extrai data de string.
    - (obter_diretorio_atual): Obtém diretório do script que está sendo executado.

    Exceções:
    - (UtilitariosError): Classe base.
    - (UtilitariosFazerRequisicaoError): Quando há erro ao fazer requisição à API.
    - (UtilitariosRetornoRequisicaoError): Quando há erro no retorno da requisição à API.
    """

    # ================================================== #

    # ~~ Função para excluir tabelas do sqlite3.
    def drop_table(table_name: str):

        """
        Resumo:
        - Função para excluir tabelas do sqlite3.

        Parâmetros:
        - (table_name: str): Nome da tabela.
        """

        # ~~ Exclui tabela.
        with connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Tabela {table_name} removida.")

    # ================================================== #

    # ~~ Função de consulta de dados da Receita Federal.
    def consultar_receita_federal(self, cnpj: str, printar_dados: bool = False, log_path: str = None) -> dict:

        """
        Resumo:
        - Consulta a API da Receita Federal e obtém dados de um CNPJ.

        Parâmetros:
        - (cnpj: str)
        - (log_path: str): Caso passado um diretório, transfere texto printado para um arquivo ".txt". O parâmetro "printar_dados" deve ser True.
        - (printar_dados):
            - (False: bool): Padrão.
            - OU (True: bool): Printa todos os dados.

        Retorna:
        - (resposta_json: dict):
            - (cnpj: str)
            - (razao_social: str)
            - (nome_fantasia):
                - (nome_fantasia: str)
                - OU ("-": str)
            - (natureza_juridica: str)
            - (situacao_cadastral: str)
            - (logradouro: str)
            - (numero: str)
            - (complemento):
                - (complemento: str)
                - OU ("-": str)
            - (bairro: str)
            - (cep: str)
            - (cidade: str)
            - (estado: str): Estado em sigla.
            - (telefone: str)
            - (email):
                - (email: str)
                - OU ("-": str)
            - (recebimento_comissao):
                - ("OK": str)
                - OU ("NÃO OK": str)
            - (regime_tributario):
                - ("SIMPLES": str)
                - OU ("LUCRO PRESUMIDO": str)
                - OU ("LUCRO REAL": str)
            - (inscricoes_estaduais: list):
                - (dict):
                    - (inscricao_estadual: str)
                    - (situacao: str)
                - OU ("ISENTO": str)
            - (inscricoes_suframa: list):
                - (dict):
                    - (inscricao_suframa: str)
                    - (situacao: str)
                - OU ("ISENTO": str)
            - (cnae: list):
                - (dict):
                    - (cnae: str)
                    - (descricao: str)

        Exceções:
        - (UtilitariosFazerRequisicaoError): Quando há erro ao fazer requisição à API.
        - (UtilitariosRetornoRequisicaoError): Quando há erro no retorno da requisição à API.
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
            raise UtilitariosFazerRequisicaoError(erro)

        # ~~ Verifica resposta.
        if resposta.status_code == 200:

            # ~~ Converte para JSON.
            resposta_json = resposta.json()

            # ~~ Cria dicionário para armazenar dados.
            dados = {}

            # ~~ Coleta CNPJ.
            dados["cnpj"] = resposta_json["estabelecimento"]["cnpj"]

            # ~~ Coleta razão social.
            dados["razao_social"] = self.formatar_texto(resposta_json["razao_social"])

            # ~~ Coleta nome fantasia.
            dados["nome_fantasia"] = self.formatar_texto(resposta_json["estabelecimento"]["nome_fantasia"]) if resposta_json["estabelecimento"]["nome_fantasia"] else "-"

            # ~~ Coleta natureza jurídica.
            dados["natureza_juridica"] = self.formatar_texto(resposta_json["natureza_juridica"]["descricao"])
            dados["natureza_juridica_id"] = resposta_json["natureza_juridica"]["id"]

            # ~~ Situação cadastral.
            dados["situacao_cadastral"] = self.formatar_texto(resposta_json["estabelecimento"]["situacao_cadastral"])

            # ~~ Coleta rua.
            dados["logradouro"] = self.formatar_texto(resposta_json["estabelecimento"]["logradouro"])

            # ~~ Coleta número.
            dados["numero"] = resposta_json["estabelecimento"]["numero"]

            # ~~ Coleta complemento.
            dados["complemento"] = re.sub(r"\s+", " ", self.formatar_texto(resposta_json["estabelecimento"]["complemento"])) if resposta_json["estabelecimento"]["complemento"] else "-"

            # ~~ Coleta bairro.
            dados["bairro"] = self.formatar_texto(resposta_json["estabelecimento"]["bairro"])

            # ~~ Coleta CEP.
            dados["cep"] = f"{resposta_json["estabelecimento"]["cep"][:5]}-{resposta_json["estabelecimento"]["cep"][5:]}"

            # ~~ Coleta cidade.
            dados["cidade"] = self.formatar_texto(resposta_json["estabelecimento"]["cidade"]["nome"])

            # ~~ Coleta sigla do estado.
            dados["estado"] = self.formatar_texto(resposta_json["estabelecimento"]["estado"]["sigla"])

            # ~~ Coleta telefone.
            dados["telefone"] = f"{resposta_json["estabelecimento"]["ddd1"]}{resposta_json["estabelecimento"]["telefone1"]}"

            # ~~ Coleta e-mail.
            dados["email"] = self.formatar_texto(resposta_json["estabelecimento"]["email"]) if resposta_json["estabelecimento"]["email"] else "-"

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
                self.printar_mensagem(mostrar_data_hora="Only", log_path=log_path)

                # ~~ Dados básicos.
                self.printar_mensagem(mensagem=f"CNPJ: {dados["cnpj"]}", mostrar_data_hora="False", log_path=log_path)
                self.printar_mensagem(mensagem=f"Razão Social: {dados["razao_social"]}", mostrar_data_hora="False", log_path=log_path)
                self.printar_mensagem(mensagem=f"Nome Fantasia: {dados["nome_fantasia"]}", mostrar_data_hora="False", log_path=log_path)
                self.printar_mensagem(mensagem=f"Natureza Jurídica: {dados["natureza_juridica_id"]} | {dados["natureza_juridica"]}", mostrar_data_hora="False", log_path=log_path)
                self.printar_mensagem(mensagem=f"Situação Cadastral: {dados["situacao_cadastral"]}", mostrar_data_hora="False", log_path=log_path)
                self.printar_mensagem(mensagem=f"Endereço Completo: {dados["logradouro"]}, {dados["numero"]} | {dados["complemento"]} | {dados["bairro"]} | {dados["cep"]} | {dados["cidade"]} | {dados["estado"]}", mostrar_data_hora="False", log_path=log_path)
                self.printar_mensagem(mensagem=f"Telefone: {dados["telefone"]}", mostrar_data_hora="False", log_path=log_path)
                self.printar_mensagem(mensagem=f"E-mail: {dados["email"]}", mostrar_data_hora="False", log_path=log_path)
                self.printar_mensagem(mensagem=f"Regime Tributário: {dados["regime_tributario"]["regime_tributario"]}", mostrar_data_hora="False", log_path=log_path)
                self.printar_mensagem(mensagem=f"Recebimento Comissão: {dados["recebimento_comissao"]}", mostrar_data_hora="False", log_path=log_path)

                # ~~ Inscrições estaduais.
                self.printar_mensagem(mensagem="Inscrições Estaduais:", mostrar_data_hora="False", log_path=log_path)
                if dados["inscricoes_estaduais"] != "ISENTO":
                    for inscricao in dados["inscricoes_estaduais"]:
                        self.printar_mensagem(mensagem=f"    {inscricao["inscricao_estadual"]} | {inscricao["situacao"]}", mostrar_data_hora="False", log_path=log_path)
                else:
                    self.printar_mensagem(mensagem=f"    {dados["inscricoes_estaduais"]}", mostrar_data_hora="False", log_path=log_path)

                # ~~ Inscrições suframa.
                self.printar_mensagem(mensagem="Inscrições Suframa:", mostrar_data_hora="False", log_path=log_path)
                if dados["inscricoes_suframa"] != "ISENTO":
                    for inscricao in dados["inscricoes_suframa"]:
                        self.printar_mensagem(f"    {inscricao["inscricao_suframa"]} | {inscricao["situacao"]}", mostrar_data_hora="False", log_path=log_path)
                else:
                    self.printar_mensagem(mensagem=f"    {dados["inscricoes_suframa"]}", mostrar_data_hora="False", log_path=log_path)

                # ~~ CNAE.
                self.printar_mensagem(mensagem="CNAE:", mostrar_data_hora="False", log_path=log_path)
                for cnae in dados["cnae"]:
                    self.printar_mensagem(f"    {cnae["cnae"]} | {cnae["descricao"]}", mostrar_data_hora="False", log_path=log_path)

                # ~~ Fim.
                self.printar_mensagem(char_type="=", char_qtd=50)

            # ~~ Retorna dados.
            return dados
        
        # ~~ Em caso de de erro na resposta.
        else:
            raise UtilitariosRetornoRequisicaoError(resposta)

    # ================================================== #

    # ~~ Coleta os diretórios definidos.
    def diretorios(self, diretorio: str) -> str:

        """
        Resumo:
        - Retorna diretorio do arquivo escolhido.
        
        Parâmetros:
        - (diretorio):
            - ("carteira": str)
            - OU ("base_revendas": str)
            - OU ("base_cadastros": str)
        
        Retorna:
        - (diretorio_escolhido: str)
        """

        # ~~ Carteira.
        if diretorio == "carteira":
            data = self.coletar_data_atual()
            matrícula = self.coletar_matricula()
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

    # ~~ Função customizada para printar mensagens.
    def printar_mensagem(self, mensagem: str = None, char_type: str = None, char_qtd: int = None, char_side: str = None, log_path: str = None, mostrar_data_hora: str = "True") -> None:

        """
        Resumo:
        - Printa mensagem ou caractere especial no terminal.
        
        Parâmetros:
        - (mensagem: str): Texto que será printado no terminal.
        - (char_type: str): Tipo de caractere a ser printado.
        - (char_qtd: int): Quantidade do caractere.
        - (char_side):
            - ("top": str): Printa caractere em cima.
            - OU ("bot": str): Printa caractere em baixo.
            - OU ("both": str): Printa caractere em ambos os lados.
        - (log_path: str): Caso passado um diretório, transfere texto printado para um arquivo ".txt".
        - (mostar_data_hora):
            - ("True": str) Padrão
            - OU ("False": str): Para não mostrar data e hora.
            - OU ("Only": str): Para printar somente a data.
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
    def printar_dataframe(self, df: pandas.DataFrame, log_path: str = None) -> None:

        """
        Resumo:
        - Printa DataFrame em formato de tabela.
        
        Parâmetros:
        - (df: DataFrame): DataFrame do pandas.
        - (log_path: str): Caso passado um diretório, transfere texto printado para um arquivo ".txt".
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
    def formatar_texto(self, texto: str) -> str:

        """
        Resumo:
        - Remove acentos e converte tudo para maiúsculas.
        
        Parâmetros:
        - (texto: str): Texto para formatar.
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
    def coletar_data_atual(self) -> dict:

        """
        Resumo:
        - Retorna as informações de data, mês e ano atuais.

        Retorna:
        - (data: dict):
            - (dia_numero: str): O dia em seu formato numérico.
            - (mes_numero: str): O mês em seu formato numérico.
            - (ano: str): O ano em str.
            - (hora: str): Hora no formato "%H-%M".
            - (data_com_hora: str): Data e hora no formato "%d-%m-%Y_%H-%M".
            - (dia_extenso: str): O dia em seu formato extenso.
            - (mes_extenso: str): O mês em seu formato extenso.
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
    def coletar_matricula(self) -> str:

        """
        Resumo:
        - Retorna a matrícula do usuário.

        Retorna:
        - (matricula: str): Matrícula.
        """

        # ~~ Coleta matrícula.
        matrícula = os.getlogin()

        # ~~ Retorna.
        return matrícula

    # ================================================== #

    # ~~ Extrai data de string.
    def extrair_data_da_string(self, string: str) -> str:

        """
        Resumo:
        - Extrai data de string.
        
        Parâmetros:
        - (string: str): Texto para extrair a data.
        
        Retorna:
        - (data: str): Data no formato string. Exemplo: "DD/MM/AA".
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
    def obter_diretorio_atual(self) -> str:

        """
        Resumo:
        - Obtém diretório do script que está sendo executado.
        
        Retorna:
        - (diretorio: str): Diretório do script que está sendo executado.
        """

        # ~~ Retorna diretório.
        return os.path.dirname(os.path.abspath(sys.argv[0]))

    # ================================================== #

# ================================================== #