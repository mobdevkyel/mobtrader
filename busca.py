import requests
import urllib 
from bs4 import BeautifulSoup
import os, time, sys, json
import pandas as pd


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

def catalogar(M,G,catalogo):
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

    #raspagem = pd.DataFrame([[par01[1],],[22,'F',58, 1.70]], index=range(0,2), columns=['MOEDA', 'PADRAO', 'PORCENTAGEM', 'WIN', 'G1', 'G2', 'HIT', 'QTDWIN', 'QTDG1', 'QTDG2', 'QTDHIT', 'HORA'])
    ParMoeda0 = pd.Series([todos['Todos'][0][1],todos['Todos'][1][1], todos['Todos'][2][1], todos['Todos'][3][1], todos['Todos'][4][1], todos['Todos'][5][1], todos['Todos'][6][1], todos['Todos'][7][1], todos['Todos'][8][1], todos['Todos'][9][1], todos['Todos'][10][1], todos['Todos'][11][1], todos['Todos'][12][1], todos['Todos'][13][1], todos['Todos'][14][1], todos['Todos'][15][1], todos['Todos'][16][1], todos['Todos'][17][1], todos['Todos'][18][1], todos['Todos'][19][1], todos['Todos'][20][1]], index=range(0,21))
    PadraoMoeda0 = pd.Series([todos['Todos'][0][2],todos['Todos'][1][2], todos['Todos'][2][2], todos['Todos'][3][2], todos['Todos'][4][2], todos['Todos'][5][2], todos['Todos'][6][2], todos['Todos'][7][2], todos['Todos'][8][2], todos['Todos'][9][2], todos['Todos'][10][2], todos['Todos'][11][2], todos['Todos'][12][2], todos['Todos'][13][2], todos['Todos'][14][2], todos['Todos'][15][2], todos['Todos'][16][2], todos['Todos'][17][2], todos['Todos'][18][2], todos['Todos'][19][2], todos['Todos'][20][2]], index=range(0,21))
    PorcentagemMoeda0 = pd.Series([todos['Todos'][0][0],todos['Todos'][1][0], todos['Todos'][2][0], todos['Todos'][3][0], todos['Todos'][4][0], todos['Todos'][5][0], todos['Todos'][6][0], todos['Todos'][7][0], todos['Todos'][8][0], todos['Todos'][9][0], todos['Todos'][10][0], todos['Todos'][11][0], todos['Todos'][12][0], todos['Todos'][13][0], todos['Todos'][14][0], todos['Todos'][15][0], todos['Todos'][16][0], todos['Todos'][17][0], todos['Todos'][18][0], todos['Todos'][19][0], todos['Todos'][20][0]], index=range(0,21))
    WinMoeda0 = pd.Series([todos['Todos'][0][3][7],todos['Todos'][1][3][7], todos['Todos'][2][3][7], todos['Todos'][3][3][7], todos['Todos'][4][3][7], todos['Todos'][5][3][7], todos['Todos'][6][3][7], todos['Todos'][7][3][7], todos['Todos'][8][3][7], todos['Todos'][9][3][7], todos['Todos'][10][3][7], todos['Todos'][11][3][7], todos['Todos'][12][3][7], todos['Todos'][13][3][7], todos['Todos'][14][3][7], todos['Todos'][15][3][7], todos['Todos'][16][3][7], todos['Todos'][17][3][7], todos['Todos'][18][3][7], todos['Todos'][19][3][7], todos['Todos'][20][3][7]], index=range(0,21))
    G1Moeda0 = pd.Series([todos['Todos'][0][3][9],todos['Todos'][1][3][9], todos['Todos'][2][3][9], todos['Todos'][3][3][9], todos['Todos'][4][3][9], todos['Todos'][5][3][9], todos['Todos'][6][3][9], todos['Todos'][7][3][9], todos['Todos'][8][3][9], todos['Todos'][9][3][9], todos['Todos'][10][3][9], todos['Todos'][11][3][9], todos['Todos'][12][3][9], todos['Todos'][13][3][9], todos['Todos'][14][3][9], todos['Todos'][15][3][9], todos['Todos'][16][3][9], todos['Todos'][17][3][9], todos['Todos'][18][3][9], todos['Todos'][19][3][9], todos['Todos'][20][3][9]], index=range(0,21))
    G2Moeda0 = pd.Series([todos['Todos'][0][3][10],todos['Todos'][1][3][10], todos['Todos'][2][3][10], todos['Todos'][3][3][10], todos['Todos'][4][3][10], todos['Todos'][5][3][10], todos['Todos'][6][3][10], todos['Todos'][7][3][10], todos['Todos'][8][3][10], todos['Todos'][9][3][10], todos['Todos'][10][3][10], todos['Todos'][11][3][10], todos['Todos'][12][3][10], todos['Todos'][13][3][10], todos['Todos'][14][3][10], todos['Todos'][15][3][10], todos['Todos'][16][3][10], todos['Todos'][17][3][10], todos['Todos'][18][3][10], todos['Todos'][19][3][10], todos['Todos'][20][3][10]], index=range(0,21))
    HitMoeda0 = pd.Series([todos['Todos'][0][3][8],todos['Todos'][1][3][8], todos['Todos'][2][3][8], todos['Todos'][3][3][8], todos['Todos'][4][3][8], todos['Todos'][5][3][8], todos['Todos'][6][3][8], todos['Todos'][7][3][8], todos['Todos'][8][3][8], todos['Todos'][9][3][8], todos['Todos'][10][3][8], todos['Todos'][11][3][8], todos['Todos'][12][3][8], todos['Todos'][13][3][8], todos['Todos'][14][3][8], todos['Todos'][15][3][8], todos['Todos'][16][3][8], todos['Todos'][17][3][8], todos['Todos'][18][3][8], todos['Todos'][19][3][8], todos['Todos'][20][3][8]], index=range(0,21))
    

    Raspagem = pd.DataFrame(data=ParMoeda0, columns=['MOEDAS'])
    Raspagem.insert(1, 'PADRAO', PadraoMoeda0)
    Raspagem.insert(2, 'PORCENTAGEM', PorcentagemMoeda0)
    Raspagem.insert(3, 'WINS', WinMoeda0)
    Raspagem.insert(4, 'G1', G1Moeda0)
    Raspagem.insert(5, 'G2', G2Moeda0)
    Raspagem.insert(6, 'HIT', HitMoeda0)
    
    
    
    
    par01 = Raspagem.loc[numeral, 'MOEDAS']
    atu = todos['ultimaAtualizacao']
    percent = Raspagem.loc[numeral, 'PORCENTAGEM']
    #par = par01[1]
    #padrao = par01[2]
    #per = par01[3]
    #taxa = str(per[1])
    #DISPO = todos['pares']
        
    paridade = Raspagem.loc[numeral, 'MOEDAS']
    padrao = Raspagem.loc[numeral, 'PADRAO']
    porcentagem = Raspagem.loc[numeral, 'PORCENTAGEM']
    WIN = Raspagem.loc[numeral, 'WINS']
    G1 = Raspagem.loc[numeral, 'G1']
    G2 = Raspagem.loc[numeral, 'G2']
    HIT = Raspagem.loc[numeral, 'HIT']
    #win = per[2]
    #g1 = per[4]
    #g2 = per[5]
    #hit = per[3]
    #letrasP = per[0]
    #lista_letras = []
    


    #letras = velas[1] + ' ' + velas[2] + ' ' + velas[3]
    #print(cores)
    #verd = int(cores.count('verde'))
    #verme = int(cores.count('vermelha'))
    

    #for i in letrasP:
    #    lista_letras.append(i)
    #doji = int(lista_letras.count('D'))
    #fixa = int(lista_letras.count('W'))
    #G01 = int(lista_letras.count('G1'))
    #G02 = int(lista_letras.count('G2'))
    #HITI = int(lista_letras.count('H'))

    #if G == 0:
    #    T = doji + HITI + G01 + G02
    #elif G == 1:
    #    T = doji + HITI + G02
    #elif G == 2:
    #    T = doji + HITI


    #print(f'DOJI = {doji}\nFIXA = {fixa}\nG1 = {G01}\nG2 = {G02}\nHIT = {HITI}')
    #total = doji+fixa+G01+G02+HITI
    #totalDoji = int(round(doji/total*100, 0))
    #totalFixa = int(round(fixa/total*100, 0))
    #totalG1 = int(round(G01/total*100, 0))
    #totalG2 = int(round(G02/total*100, 0))
    #totalHit = int(round(HITI/total*100, 0))

    #print(Raspagem)
    if padrao == 'C3':
        numeral += 1
        catalogar(M,G,catalogo)
    else:
        #print(f'{paridade} / {padrao}')
        return paridade, padrao, porcentagem, WIN, G1, G2, HIT, atu
    '''
    #print(f'{paridade} / {padrao} = {T} Derrotas')
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
    '''   

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



