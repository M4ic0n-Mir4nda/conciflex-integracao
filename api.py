import json
import requests
import os
from PyQt5.QtCore import QDateTime
from datetime import datetime, timedelta
from functions import conectar, verifyDecimalAndHexadecimal
from connDB import ConnectDB


def vendas(data, cnpj, page, lastPage, loja=1):
    try:
        print(data)
        conexaoODBC = conectar()
        conn = ConnectDB(conexaoODBC)
        conn.conecta()
        folderConc = 'conc'
        if os.path.exists(folderConc):
            pass
        else:
            os.mkdir(folderConc)
        folderVendas = 'conc/vendas'
        if os.path.exists(folderVendas):
            pass
        else:
            os.mkdir(folderVendas)
        foldeRetorno = f'conc/vendas/retorno'
        if os.path.exists(foldeRetorno):
            pass
        else:
            os.mkdir(foldeRetorno)
        folderData = f'conc/vendas/retorno/{data}'
        if os.path.exists(folderData):
            pass
        else:
            os.mkdir(folderData)
        token = "ae905ef0dda38d31af1243db6257dd54"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        numPage = page
        lastPage = lastPage
        url = f"https://login.conciflex.com.br/api/vendas?data_inicial={data}&data_final={data}&cnpj={cnpj}&page={numPage}"
        response = requests.get(url, headers=headers)
        jsonForDictionary = json.loads(response.text)
        if 'data' in response.text:
            if len(jsonForDictionary['data']) == 0:
                return False
            lastPage += jsonForDictionary['last_page']
            for i in range(1, lastPage):
                url = f"https://login.conciflex.com.br/api/vendas?data_inicial={data}&data_final={data}&cnpj={cnpj}&page={numPage}"
                response = requests.get(url, headers=headers)
                jsonForDictionary = json.loads(response.text)
                for datas in jsonForDictionary['data']:
                    idConciliador = datas['id_erp'].split("-") if datas['id_erp'] is not None else None
                    idErp = int(idConciliador[1]) if idConciliador is not None else 0
                    dataVenda = datas['data_venda'].replace("-", "")
                    valorVenda = float(datas['valor_bruto']) if datas['valor_bruto'] else 0
                    parcela = int(datas['parcela'])
                    nsu = datas['nsu']
                    autorizacao = verifyDecimalAndHexadecimal(str(datas['autorizacao']))
                    codigoAdquirente = int(datas['codigo_adquirente'])
                    codigoBandeira = int(datas['codigo_bandeira'])
                    codigoProduto = int(datas['codigo_produto'])
                    try:
                        codigoEstabelecimento = int(datas['estabelecimento'])
                    except ValueError:
                        codigoEstabelecimento = 0
                    codigoFormaPagamento = int(datas['codigo_forma_pagamento'])
                    produto = datas['produto']
                    dataPrevisao = datas['data_previsao'].replace("-", "")
                    valorReceber = float(datas['valor_liquido'])
                    try:
                        sql = f"""
                                REPLACE INTO cartoesconcvendas (
                                    iderp, data, valor, parcela, nsuorigem, nsuadministradora, autorizacao, codadquirente, codloja,
                                    codbandeira, codproduto, codmodalidade, produto, datarecebe, valorrecebe
                                )
                                VALUES (
                                    {idErp}, {dataVenda}, {valorVenda}, {parcela}, "", "{nsu}", "{autorizacao}", 
                                    {codigoAdquirente}, {codigoEstabelecimento}, {codigoBandeira}, 
                                    {codigoProduto}, {codigoFormaPagamento}, "{produto}", {dataPrevisao},
                                    {valorReceber}
                                )
                            """
                        conn.execute(sql)
                        conn.commit()
                    except Exception as e:
                        print(e)
                dataDictionary = jsonForDictionary['data']
                dictionaryForJson = json.dumps(dataDictionary, indent=2)
                with open(f"{folderData}/{f'pagina-{i}'}.json", 'w') as arquivo:
                    arquivo.write(dictionaryForJson)
                numPage += 1
            return True
    except requests.exceptions.RequestException as e:
        print(e)
        return "Erro na requisição GET:"


def pagamentos(data, cnpj, page, lastPage, loja=1):
    try:
        print(data)
        conexaoODBC = conectar()
        conn = ConnectDB(conexaoODBC)
        conn.conecta()
        folderConc = 'conc'
        if os.path.exists(folderConc):
            pass
        else:
            os.mkdir(folderConc)
        folderVendas = 'conc/pagamentos'
        if os.path.exists(folderVendas):
            pass
        else:
            os.mkdir(folderVendas)
        folderretorno = f'conc/pagamentos/retorno'
        if os.path.exists(folderretorno):
            pass
        else:
            os.mkdir(folderretorno)
        folderData = f'conc/pagamentos/retorno/{data}'
        if os.path.exists(folderData):
            pass
        else:
            os.mkdir(folderData)
        token = "ae905ef0dda38d31af1243db6257dd54"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        numPage = page
        lastPage = lastPage
        url = f"https://login.conciflex.com.br/api/pagamentos?data_inicial={data}&data_final={data}&cnpj={cnpj}&page={numPage}"
        response = requests.get(url, headers=headers)
        jsonForDictionary = json.loads(response.text)
        if 'data' in response.text:
            if len(jsonForDictionary['data']) == 0:
                return False
            lastPage += jsonForDictionary['last_page']
            for i in range(1, lastPage):
                url = f"https://login.conciflex.com.br/api/pagamentos?data_inicial={data}&data_final={data}&cnpj={cnpj}&page={numPage}"
                response = requests.get(url, headers=headers)
                jsonForDictionary = json.loads(response.text)
                for datas in jsonForDictionary['data']:
                    idConciliador = datas['id_venda_erp'].split("-") if datas['id_venda_erp'] is not None else None
                    idErp = int(idConciliador[1]) if idConciliador is not None else 0
                    tipoLancamento = datas['tipo_lancamento']
                    dataVenda = datas['data_venda'].replace("-", "")
                    valorBruto = float(datas['valor_bruto']) if datas['valor_bruto'] else 0
                    taxa = float(datas['taxa_percentual']) if datas['taxa_percentual'] else 0
                    valorTaxa = float(datas['valor_taxa']) if datas['valor_taxa'] else 0
                    nsu = datas['nsu'] if datas['nsu'] else ""
                    autorizacao = verifyDecimalAndHexadecimal(str(datas['autorizacao'])) if datas['autorizacao'] else ""
                    codigoAdquirente = int(datas['cod_adquirente'])
                    codigoBandeira = int(datas['cod_bandeira'])
                    codigoProduto = int(datas['cod_produto']) if datas['cod_produto'] else 0
                    codigoModalidade = int(datas['codigo_forma_pagamento'])
                    produto = datas['produto']
                    dataReceber = datas['data_pagamento'].replace("-", "")
                    valorReceber = float(datas['valor_liquido'])
                    codigoBanco = int(datas['cod_banco'])
                    banco = datas['banco']
                    agencia = int(datas['agencia'])
                    conta = int(datas['conta'])
                    statusConc = int(datas['cod_status_conciliacao'])
                    try:
                        sql = f"""
                                REPLACE INTO cartoesconcpag (
                                    iderp, tipolancamento, datavenda, valor, taxa, valortaxa, nsuorigem, nsuadministradora,
                                    autorizacao, codadquirente, codbandeira, codproduto, codmodalidade, produto,
                                    datarecebe, valorrecebe, codbanco, banco, agencia, conta, statusconc
                                )
                                VALUES (
                                    {idErp}, "{tipoLancamento}", {dataVenda}, {valorBruto}, {taxa}, {valorTaxa}, "", 
                                    "{nsu}", "{autorizacao}", {codigoAdquirente}, {codigoBandeira}, {codigoProduto},
                                    {codigoModalidade}, "{produto}", {dataReceber}, {valorReceber}, {codigoBanco},
                                    "{banco}", {agencia}, {conta}, {statusConc}
                                )
                            """
                        conn.execute(sql)
                        conn.commit()
                    except Exception as e:
                        print(e)
                dataDictionary = jsonForDictionary['data']
                dictionaryForJson = json.dumps(dataDictionary, indent=2)
                with open(f"{folderData}/{f'pagina-{i}'}.json", 'w') as arquivo:
                    arquivo.write(dictionaryForJson)
                numPage += 1
            return True
    except requests.exceptions.RequestException as e:
        print(e)
        return "Erro na requisição GET:"


class Api:
    def __init__(self):
        self.numPage = 1
        self.lastPage = 1
        self.token = "ae905ef0dda38d31af1243db6257dd54"

    def enviar_requisicao_post(self, lista):
        # URL da API para enviar as listas
        url = "https://login.conciflex.com.br/api/vendas_sistema"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            jsonT = json.dumps(lista)
            print(jsonT)
            response = requests.post(url, json=lista, headers=headers)
            if 'mensagem' in response.text:
                j = json.loads(response.text)
                return j
            else:
                return False

        except requests.exceptions.RequestException as e:
            print("Erro na requisição POST:", e)

    def getVendas(self, apartir, ate, loja, cnpj):
        try:
            data = datetime.strptime(str(apartir), '%d/%m/%Y').date()
            ate = datetime.strptime(str(ate), '%d/%m/%Y').date()
            while data <= ate:
                dia = data.day
                mes = data.month

                if mes in [4, 6, 9, 11] and dia <= 30:
                    vendas(data.strftime('%Y-%m-%d'), cnpj, self.numPage, self.lastPage)
                elif mes != 2 and dia <= 31:
                    vendas(data.strftime('%Y-%m-%d'), cnpj, self.numPage, self.lastPage)
                elif mes == 2 and dia <= 28:
                    vendas(data.strftime('%Y-%m-%d'), cnpj, self.numPage, self.lastPage)

                data += timedelta(days=1)
            self.numPage = 1
            self.lastPage = 1
            return True
        except Exception as e:
            print(e)
            return "Erro na requisição GET:"

    def getPagamentos(self, apartir, ate, loja, cnpj):
        try:
            data = datetime.strptime(str(apartir), '%d/%m/%Y').date()
            ate = datetime.strptime(str(ate), '%d/%m/%Y').date()
            while data <= ate:
                dia = data.day
                mes = data.month

                if mes in [4, 6, 9, 11] and dia <= 30:
                    pagamentos(data.strftime('%Y-%m-%d'), cnpj, self.numPage, self.lastPage)
                elif mes != 2 and dia <= 31:
                    pagamentos(data.strftime('%Y-%m-%d'), cnpj, self.numPage, self.lastPage)
                elif mes == 2 and dia <= 28:
                    pagamentos(data.strftime('%Y-%m-%d'), cnpj, self.numPage, self.lastPage)

                data += timedelta(days=1)
            self.numPage = 1
            self.lastPage = 1
            return True
        except requests.exceptions.RequestException as e:
            return "Erro na requisição GET:"


if __name__ == "__main__":
    api = Api()
    # api.getVendas("24/07/2023", "25/07/2023", "1", "12877125000183")
    api.getPagamentos("28/07/2023", "28/07/2023", "1", "12877125000183")
