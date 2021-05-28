import requests
import urllib 
from bs4 import BeautifulSoup
import os, time, sys, json

numeral = 0

paridade = '' 
padrao = '' 
percent = '' 
WIN = '' 
G1 = '' 
G2 = '' 
HIT = '' 
win = ''  
g1 = '' 
g2 = '' 
hit = '' 
atu = ''

def disponiveis(M,G):

    if G == 0:
        gale = 'porcentagemWinDePrimeira'
        url = f'https://ocatalogador.com/api/{gale}/{M}'
    elif G == 1:
        gale = 'porcentagemGale1'
        url = f'https://ocatalogador.com/api/{gale}/{M}'
    elif G == 2:
        gale = 'porcentagemGale2'
        url = f'https://ocatalogador.com/api/{gale}/{M}'

    

    class_list = set()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    todos = json.loads(page.content)
    DISPO = todos['pares']
    return DISPO

def catalogar(M,G,ERROS,catalogo):
    global numeral
    global paridade 
    global padrao
    global percent
    global WIN 
    global G1
    global G2 
    global HIT 
    global win 
    global g1
    global g2
    global hit
    global atu
    #print(numeral)
    if catalogo == 0:
        if G == 0:
            gales = 'porcentagemWinDePrimeira'
            url = f'https://ocatalogador.com/api/{gales}/{M}'
        elif G == 1:
            gales = 'porcentagemGale1'
            url = f'https://ocatalogador.com/api/{gales}/{M}'
        elif G == 2:
            gales = 'porcentagemGale2'
            url = f'https://ocatalogador.com/api/{gales}/{M}'
    elif catalogo == 1:
        gales = 'porcentagemWinDePrimeira'
        url = f'https://ocatalogador.com/api/{gales}/{M}'
    elif catalogo == 2:
        gales = 'porcentagemGale1'
        url = f'https://ocatalogador.com/api/{gales}/{M}'
    elif catalogo == 3:
        gales = 'porcentagemGale2'
        url = f'https://ocatalogador.com/api/{gales}/{M}'


    

    class_list = set()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    todos = json.loads(page.content)
    
    par01 = todos['Todos'][numeral]
    atu = todos['ultimaAtualizacao']
    percent = par01[0]
    #par = par01[1]
    #padrao = par01[2]
    per = par01[3]
    taxa = str(per[1])
    DISPO = todos['pares']
        
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
    letrasP = per[0]
    lista_letras = []
    


    #letras = velas[1] + ' ' + velas[2] + ' ' + velas[3]
    #print(cores)
    #verd = int(cores.count('verde'))
    #verme = int(cores.count('vermelha'))
    

    for i in letrasP:
        lista_letras.append(i)
    doji = int(lista_letras.count('D'))
    fixa = int(lista_letras.count('W'))
    G01 = int(lista_letras.count('G1'))
    G02 = int(lista_letras.count('G2'))
    HITI = int(lista_letras.count('H'))

    if G == 0:
        T = doji + HITI + G01 + G02
    elif G == 1:
        T = doji + HITI + G02
    elif G == 2:
        T = doji + HITI


    #print(f'DOJI = {doji}\nFIXA = {fixa}\nG1 = {G01}\nG2 = {G02}\nHIT = {HITI}')
    total = doji+fixa+G01+G02+HITI
    totalDoji = int(round(doji/total*100, 0))
    totalFixa = int(round(fixa/total*100, 0))
    totalG1 = int(round(G01/total*100, 0))
    totalG2 = int(round(G02/total*100, 0))
    totalHit = int(round(HITI/total*100, 0))

        
    print(f'{paridade} / {padrao} = {T} Derrotas')
    if T > int(ERROS) and numeral <= 23:
        #print(f'BUSCANDO MELHOR OPÇÃO DE ENTRADA')
        numeral += 1
        catalogar(M,G,ERROS,catalogo)
    #print(url)
    os.system('cls' if os.name == 'nt' else 'clear')
    if numeral > 23:
        return '', '', '', '', '', '', '', '', '', '', '', ''
    else:
        return paridade, padrao, percent, WIN, G1, G2, HIT, win, g1, g2, hit, atu
    
            
        
        #return paridade, padrao, percent, WIN, G1, G2, HIT, win, g1, g2, hit, atu, 'ok'
    #catalogar(M,G,ERROS)
     

        #os.system('cls' if os.name == 'nt' else 'clear')
    #print(f'numero: {numeral} {paridade}')
        #Melhor = paridade, padrao, percent, WIN, G1, G2, HIT, win, g1, g2, hit
        #print(Melhor)
        #print(url)
        

def verificacao():
    ver = 1
    bot = 'mobtraderbot'
    data = {'desenvolvedor': f'{bot}','acao': 'verificar'}
    url = "http://mobtrader.mypressonline.com/bot/jogadores.php"    
    resp = requests.post(url, data)
    retorno = resp.text
    lista = resp.text.split(',')
    lista2 = []
    for i in lista:
        lista2.append(i)
    versao = lista2[1]
    link = lista2[4]
    msg = lista2[5]

    if ver < int(versao):
        print(f'{msg}\n{link}')
#os.system('cls' if os.name == 'nt' else 'clear')
#print(catalogar('M1',0,0))



