import requests
from bs4 import BeautifulSoup
import os, time, sys



def Agora():
    url = 'https://www.protipster.pt/prognosticos/em-direto'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    Ag = soup.findAll('span', {"class" : "font-bold"})
    Pro = soup.findAll('p', {"class" : "cursor-pointer font-bold text-left text-black text-lg leading-8 m-0"})
    List_Agora = []
    List_Prod = []

    for B in Pro:
        dica = str(B).replace('<p class="cursor-pointer font-bold text-left text-black text-lg leading-8 m-0" data-toggle="tooltip" title="Detalhes da tip">','').replace('\n</p>','').replace('\n','').replace('  ','')
        List_Prod.append(dica)
        
    

    for A in Ag:
        times = str(A).replace('<span class="font-bold">','').replace('</span>','').replace('<span class="font-bold leading-none">','')
        List_Agora.append(times)

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'\n=============================\n  DICAS PARA JOGOS AO VIVO\n=============================\n{List_Agora[0]} VS {List_Agora[1]}\nDICA: {List_Prod[0]}\n-----------------------------\n{List_Agora[3]} VS {List_Agora[4]}\nDICA: {List_Prod[1]}\n-----------------------------\n')

def Especial():
    url = 'https://www.protipster.pt/prognosticos/aposta-dia-futebol'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    Ag = soup.findAll('span', {"class" : "font-bold"})
    Pro = soup.findAll('p', {"class" : "cursor-pointer font-bold text-left text-black text-lg leading-8 m-0"})
    List_Agora = []
    List_Prod = []
    

    for B in Pro:
        dica = str(B).replace('<p class="cursor-pointer font-bold text-left text-black text-lg leading-8 m-0" data-toggle="tooltip" title="Detalhes da tip">','').replace('\n</p>','').replace('\n','').replace('  ','')
        List_Prod.append(dica)
        
    

    for A in Ag:
        times = str(A).replace('<span class="font-bold">','').replace('</span>','').replace('<span class="font-bold leading-none">','')
        List_Agora.append(times)

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'\n===============================\n  DICAS PARA JOGO MAIS COMENTADO\n===============================\n{List_Agora[0]} VS {List_Agora[1]}\nDICA: {List_Prod[0]}\n')

def Proximo():
    url = 'https://afootballreport.com/pt/previsoes/cantos'

    class_list = set()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    List_Hora = []
    List_Casa = []
    List_Fora = []
    List_Tip = []
    List_Dica = []

    Times = soup.findAll('div', {"class" : "time"})
    Casas = soup.findAll('div', {"class" : "home-team"})
    Visitantes = soup.findAll('div', {"class" : "away-team"})
    Tip = soup.findAll('div', {"class" : "tips stats-tip"})
    Dica = soup.findAll('div', {"class" : "logic-tip"})


    for T in Times:
        Horarios = str(T).replace('<div class="time">','').replace('</div>','')
        List_Hora.append(Horarios)

    for C in Casas:
        Homes = str(C).replace('<div class="home-team">','').replace('</div>','')
        List_Casa.append(Homes)

    for V in Visitantes:
        away = str(V).replace('<div class="away-team">','').replace('</div>','')
        List_Fora.append(away)

    for TP in Tip:
        TIPS = str(TP).replace('<div class="tips stats-tip">','').replace('</div>','')
        List_Tip.append(TIPS)

    for D in Dica:
        DIC = str(D).replace('<div class="stats-tip-container logic-tip">','').replace('<div class="logic-tip">','').replace('</div>','').replace('\n','').replace('<div>','')
        List_Dica.append(DIC)



    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'\n=============================\n  DICAS PARA ESCANTEIOS\n=============================\n{List_Casa[0]} VS {List_Fora[0]}\nDICA: {List_Tip[0]} Escanteios\n-----------------------------\n{List_Casa[1]} VS {List_Fora[1]}\nDICA: {List_Tip[2]} Escanteios\n-----------------------------\n')

def Cartoes():
    url = 'https://afootballreport.com/pt/previsoes/cartoes'

    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    List_Hora = []
    List_Casa = []
    List_Fora = []
    List_Tip = []
    List_Dica = []

    Times = soup.findAll('div', {"class" : "time"})
    Casas = soup.findAll('div', {"class" : "home-team"})
    Visitantes = soup.findAll('div', {"class" : "away-team"})
    Tip = soup.findAll('div', {"class" : "tips stats-tip"})
    Dica = soup.findAll('div', {"class" : "logic-tip"})


    for T in Times:
        Horarios = str(T).replace('<div class="time">','').replace('</div>','')
        List_Hora.append(Horarios)

    for C in Casas:
        Homes = str(C).replace('<div class="home-team">','').replace('</div>','')
        List_Casa.append(Homes)

    for V in Visitantes:
        away = str(V).replace('<div class="away-team">','').replace('</div>','')
        List_Fora.append(away)

    for TP in Tip:
        TIPS = str(TP).replace('<div class="tips stats-tip">','').replace('</div>','')
        List_Tip.append(TIPS)

    for D in Dica:
        DIC = str(D).replace('<div class="stats-tip-container logic-tip">','').replace('<div class="logic-tip">','').replace('</div>','').replace('\n','').replace('<div>','')
        List_Dica.append(DIC)



    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'\n=============================\n  DUPLA PARA CARTOES\n=============================\n{List_Casa[0]} VS {List_Fora[0]}\nDICA: {List_Tip[0]} Cartões\n-----------------------------\n{List_Casa[2]} VS {List_Fora[2]}\nDICA: {List_Tip[2]} Cartões\n-----------------------------\n')

def Multipla(dia):
    if dia == 'Hoje':
        url = 'https://www.protipster.pt/prognosticos/melhores-jogos-apostar-hoje'
    elif dia == 'Amanhã':
        url = 'https://www.protipster.pt/prognosticos/melhores-jogos-apostar-amanha'
    elif dia == 'Handcap':
        url = 'https://www.protipster.pt/prognosticos/handicap-asiatico'
    elif dia == 'Cashout':
        url = 'https://www.protipster.pt/prognosticos/odds-a-descer'
    elif dia == 'Vencedores':
        url = 'https://www.protipster.pt/prognosticos/1x2'
    elif dia == 'Empates':
        url = 'https://www.protipster.pt/prognosticos/empates'   
    elif dia == 'Altas':
        url = 'https://www.protipster.pt/prognosticos/odds-altas'
    elif dia == 'Over1.5':
        url = 'https://www.protipster.pt/prognosticos/mais-1.5-golos' 
    elif dia == 'Over2.5':
        url = 'https://www.protipster.pt/prognosticos/mais-2.5-golos'
        
        
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    Ag = soup.findAll('span', {"class" : "details-pick__match-data__teams"})
    dc = soup.findAll('span', {"class" : "details-pick__match-data__outcome"})
    
    List_times = []
    List_dcs = []
    
    for B in Ag:
        t = str(B).replace('<span class="details-pick__match-data__teams">','').replace('\n</p>','').replace('</span>','').replace('<span>','').replace('\n','').replace('            ','').replace('        ','')
        List_times.append(t)

    for A in dc:
        D = str(A).replace('<span class="details-pick__match-data__teams">','').replace('<span class="details-pick__match-data__outcome">','').replace('</span>','')
        List_dcs.append(D)

    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'\n=============================\n  DICAS PARA MULTIPLAS {dia.upper()}\n=============================\n{List_times[0]}\nDica: {List_dcs[0]}\n--------------------\n{List_times[1]}\nDica: {List_dcs[1]}\n--------------------\n{List_times[2]}\nDica: {List_dcs[2]}\n--------------------\n{List_times[3]}\nDica: {List_dcs[3]}\n--------------------\n')

def selec():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('OLÁ, FUI CRIADO POR EZEQUIEL PARA PROCURAR BONS JOGOS\nQUE TIPO DE JOGOS ESTA QUERENDO?\n\n1 = AO VIVO\n2 = MAIS COMENTADO\n3 = ESCANTEIOS\n4 = CARTOES\n5 = MULTIPLAS\n')
    select = input('DIGITE UM NUMERO: ')

    if select == '1':
        print('Ok, procurando jogos...\n')
        Agora()
        print('\n1 = sair\n2 = Voltar')
        s = input('DIGITE UM NUMERO: ')
        if s == '1':
            sys.exit()
        else:
            selec()
    elif select == '2':
        print('Ok, procurando jogos...\n')
        Especial()
        print('\n1 = sair\n2 = Voltar')
        s = input('DIGITE UM NUMERO: ')
        if s == '1':
            sys.exit()
        else:
            selec()
    elif select == '3':
        print('Ok, procurando jogos...\n')
        Proximo()
        print('\n1 = sair\n2 = Voltar')
        s = input('DIGITE UM NUMERO: ')
        if s == '1':
            sys.exit()
        else:
            selec()
    elif select == '4':
        print('Ok, procurando jogos...\n')
        Cartoes()
        print('\n1 = sair\n2 = Voltar')
        s = input('DIGITE UM NUMERO: ')
        if s == '1':
            sys.exit()
        else:
            selec()
    elif select == '5':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('LEGAL, TENHOS VARIOS TIPOS DE MULTIPLAS, ESCOLHA:\n1 = PARA HOJE\n2 = PARA AMANHÃ\n3 = HANDCAP\n4 = CASHAUT\n5 = 1x2\n6 = EMPATES\n7 = ODDS ALTAS\n8 = OVER 1.5\n9 = OVER 2.5')
        m = input('DIGITE UM NUMERO: ')
        if m == '1':
            print('Ok, procurando jogos...\n')
            Multipla('Hoje')
            print('\n1 = sair\n2 = Voltar')
            s = input('DIGITE UM NUMERO: ')
            if s == '1':
                sys.exit()
            else:
                selec()
        elif m == '2':
            print('Ok, procurando jogos...\n')
            Multipla('Amanhã')
            print('\n1 = sair\n2 = Voltar')
            s = input('DIGITE UM NUMERO: ')
            if s == '1':
                sys.exit()
            else:
                selec()
        elif m == '3':
            print('Ok, procurando jogos...\n')
            Multipla('Handcap')
            print('\n1 = sair\n2 = Voltar')
            s = input('DIGITE UM NUMERO: ')
            if s == '1':
                sys.exit()
            else:
                selec()
        elif m == '4':
            print('Ok, procurando jogos...\n')
            Multipla('Cashout')
            print('\n1 = sair\n2 = Voltar')
            s = input('DIGITE UM NUMERO: ')
            if s == '1':
                sys.exit()
            else:
                selec()
        elif m == '5':
            print('Ok, procurando jogos...\n')
            Multipla('Vencedores')
            print('\n1 = sair\n2 = Voltar')
            s = input('DIGITE UM NUMERO: ')
            if s == '1':
                sys.exit()
            else:
                selec()
        elif m == '6':
            print('Ok, procurando jogos...\n')
            Multipla('Empates')
            print('\n1 = sair\n2 = Voltar')
            s = input('DIGITE UM NUMERO: ')
            if s == '1':
                sys.exit()
            else:
                selec()
        elif m == '7':
            print('Ok, procurando jogos...\n')
            Multipla('Altas')
            print('\n1 = sair\n2 = Voltar')
            s = input('DIGITE UM NUMERO: ')
            if s == '1':
                sys.exit()
            else:
                selec()
        elif m == '8':
            print('Ok, procurando jogos...\n')
            Multipla('Over1.5')
            print('\n1 = sair\n2 = Voltar')
            s = input('DIGITE UM NUMERO: ')
            if s == '1':
                sys.exit()
            else:
                selec()
        elif m == '9':
            print('Ok, procurando jogos...\n')
            Multipla('Over2.5')
            print('\n1 = sair\n2 = Voltar')
            s = input('DIGITE UM NUMERO: ')
            if s == '1':
                sys.exit()
            else:
                selec()
        
selec()
    


    

