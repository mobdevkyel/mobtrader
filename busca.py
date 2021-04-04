
import requests
from bs4 import BeautifulSoup
import json



def catalogar():
    
    
    url = 'https://catalogador.ml/api/porcentagemGale2/M1'

    class_list = set()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    todos = json.loads(page.content)

    par01 = todos['Todos'][0]
    atu = todos['ultimaAtualizacao']
    percent = par01[0]
    #par = par01[1]
    #padrao = par01[2]
    per = par01[3]
    taxa = str(per[1])
    
    
   
    
    paridade = par01[1]
    padrao = par01[2]
    porcentagem = taxa.replace("%", "")
    WIN = per[7]
    G1 = per[9]
    G2 = per[10]
    HIT = per[8]
    win = per[2]
    g1 = per[4]
    g2 = per[5]
    hit = per[3]

    Melhor = paridade, padrao, porcentagem, WIN, G1, G2, HIT, win, g1, g2, hit
    #print(Melhor)

    return paridade, padrao, porcentagem, WIN, G1, G2, HIT, win, g1, g2, hit, atu
#catalogar()
