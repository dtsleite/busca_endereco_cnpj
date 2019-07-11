# -*- coding: utf-8 -*-
'''
    Author: Douglas T. S. Leite
    @date: 2019-07-05
    Python version: 2.7
    
    Script responsável por buscar CNPJs na planilha lista_cnpj.xlsx extraída da tabela cliente e retornar seus respectivos
    endereços.
    
    Formato de retorno: O arquivo de retorno para exemplo se encontra na pasta de mesmo nível nomeado como:
    exemplo_retorno.json
    
    O endpoint utilizado disponibiliza apenas 3 endereços a cada minuto.


	Dependencias:
	- pandas
	- requests
	- xlrd
	- openpyxl
'''
import pandas as pd
import requests
import json
import time
import csv

df = pd.read_excel('lista_cnpj.xlsx', dtype=str)
colunas =  ['cnpj', 'logradouro', 'numero', 'municipio', 'bairro', 'uf', 'cep', 'req_status']
lst_enderecos = []
df = df['cnpj'].apply(lambda x: '{0:0>11}'.format(x))

def busca_endereco(d):
    for item in d.items():
        print(item)
        resultado = requests.get("https://www.receitaws.com.br/v1/cnpj/" + str(item[1]))
        data_endereco = json.loads(resultado.content)
        lst_enderecos.append([item[1],data_endereco['logradouro'],data_endereco['numero'],data_endereco['municipio'],data_endereco['bairro'],data_endereco['uf'], data_endereco['cep'].replace('.', '').replace('-',''), resultado])
        print(resultado)
    df1 = pd.DataFrame(lst_enderecos, columns=colunas)
    df1.to_excel("./output.xlsx")

colunas =  ['cnpj', 'logradouro', 'numero', 'municipio', 'bairro', 'uf', 'cep', 'req_status']
df1 = pd.DataFrame(lst_enderecos, columns=colunas)
df1.to_excel("./output.xlsx")

while(len(df) > 0):
    df_up = df.iloc[:3]
    df = df. iloc[3:,]
    busca_endereco(df_up)
    time.sleep(60)
    