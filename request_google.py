import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
Cidades = ['Campinas - SP']
listafinal = list()
distribuidor = dict()
Distribuidores = ['oficina']
count2=0
for Cidade in Cidades:
    count2+=1
    for TipoDistribuidor in Distribuidores:
        url = "https://www.google.com/maps/search/" + TipoDistribuidor + "+" + Cidade
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        lista = soup.find_all('script', nonce_="")
        listaenderecos = str(lista[7])
        separador = str(",[")
        listaendereco = listaenderecos.split(separador)
        count = 0
        referencias = "http://www.google.com/search?q"
        for l in listaendereco:
            if listaendereco[count].find(referencias) != -1:
                distribuidor['Pesquisa'] = listaendereco[count]
                endereco = urllib.parse.unquote_plus((listaendereco[count][listaendereco[count].find("d") + 1:])[
                                                     :(listaendereco[count][listaendereco[count].find("d") + 1:]).find(
                                                         "\\")])
                distribuidor['Endereco'] = endereco[endereco.find('-') + 2:]
                if len(distribuidor['Endereco'].split(",")) >= 3:
                    distribuidor['Cidade'] = Cidade
                    distribuidor['Tipo'] = TipoDistribuidor
                distribuidor['Nome'] = endereco[:endereco.find('-') - 1]
                if len((str(listaendereco[count + 3]).replace("\\", "")).split('"')) != 1:
                    distribuidor['Seguimento'] = (str(listaendereco[count + 3]).replace("\\", "")).split('"')[1]
                else:
                    distribuidor['Seguimento'] = "0"
                distribuidor['Telefone'] = (str(listaendereco[count - 2]).replace("\\", "")).split('"')[1]
                listafinal.append(distribuidor.copy())
            count += 1
        print(count2,Cidade,TipoDistribuidor)
dados = listafinal[:]
df = pd.DataFrame(dados)
df.to_csv("DIGITE AQUI NOME DO ARQUIVO PARA SALVAR.csv")
print(df)
