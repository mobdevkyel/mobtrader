from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta
from colorama import init, Fore, Back
from time import time
from variaveislista import *
import sys
import os

init(autoreset=True)

def catalogaragora(iq):
    global ISI

    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        arquivo = 'sinais.txt' 
        os.remove(arquivo)
    except:
        open('sinais.txt', 'a').write('novalista' + '\n')
        arquivo = 'sinais.txt' 
        os.remove(arquivo)
    
    def cataloga(par, dias, prct_call, prct_put, timeframe):
        data = []
        datas_testadas = []
        time_ = time()
        sair = False
        while sair == False:
            velas = iq.get_candles(par, (timeframe * 60), 1000, time_)
            velas.reverse()
            
            for x in velas:	
                if datetime.fromtimestamp(x['from']).strftime('%Y-%m-%d') not in datas_testadas: 
                    datas_testadas.append(datetime.fromtimestamp(x['from']).strftime('%Y-%m-%d'))
                    
                if len(datas_testadas) <= dias:
                    x.update({'cor': 'verde' if x['open'] < x['close'] else 'vermelha' if x['open'] > x['close'] else 'doji'})
                    data.append(x)
                else:
                    sair = True
                    break
                    
            time_ = int(velas[-1]['from'] - 1)

        analise = {}
        for velas in data:
            horario = datetime.fromtimestamp(velas['from']).strftime('%H:%M')
            if horario not in analise : analise.update({horario: {'verde': 0, 'vermelha': 0, 'doji': 0, '%': 0, 'dir': ''}})	
            analise[horario][velas['cor']] += 1
            
            try:
                analise[horario]['%'] = round(100 * (analise[horario]['verde'] / (analise[horario]['verde'] + analise[horario]['vermelha'] + analise[horario]['doji'])))
            except:
                pass
        
        for horario in analise:
            if analise[horario]['%'] > 50 : analise[horario]['dir'] = 'CALL'
            if analise[horario]['%'] < 50 : analise[horario]['%'],analise[horario]['dir'] = 100 - analise[horario]['%'],'PUT '
        
        return analise

    print('\n\nQual timeframe deseja analisar? 1, 5, 15 ou 30: ', end='')
    timeframe = int(input())
    if timeframe == 1:
        letra = 'M1'
    elif timeframe == 5:
        letra = 'M5'
    elif timeframe == 15:
        letra = 'M15'
    elif timeframe == 30:
        letra = 'M30'
    elif timeframe == 60:
        letra = 'H1'
    
    
    print('\nQuantos dias deseja analisar?: ', end='')
    dias = int(input())

    print('\nPorcentagem minima?: ', end='')
    porcentagem = int(input())

    print('\nQuantos Martingales?: ', end='')
    martingale = input()

    prct_call = abs(porcentagem)
    prct_put = abs(100 - porcentagem)

    P = iq.get_all_open_time()

    print('\n\n')

    catalogacao = {}
    for par in P['digital']:
        if P['digital'][par]['open'] == True:
            timer = int(time())
            print(Fore.GREEN + '*' + Fore.RESET + ' CATALOGANDO - ' + par + '.. ', end='')
            
            catalogacao.update({par: cataloga(par, dias, prct_call, prct_put, timeframe)})	
            
            for par in catalogacao:
                for horario in sorted(catalogacao[par]):
                    if martingale.strip() != '':					
                    
                        mg_time = horario
                        soma = {'verde': catalogacao[par][horario]['verde'], 'vermelha': catalogacao[par][horario]['vermelha'], 'doji': catalogacao[par][horario]['doji']}
                        
                        for i in range(int(martingale)):

                            catalogacao[par][horario].update({'mg'+str(i+1): {'verde': 0, 'vermelha': 0, 'doji': 0, '%': 0} })

                            mg_time = str(datetime.strptime((datetime.now()).strftime('%Y-%m-%d ') + str(mg_time), '%Y-%m-%d %H:%M') + timedelta(minutes=timeframe))[11:-3]
                            
                            if mg_time in catalogacao[par]:
                                catalogacao[par][horario]['mg'+str(i+1)]['verde'] += catalogacao[par][mg_time]['verde'] + soma['verde']
                                catalogacao[par][horario]['mg'+str(i+1)]['vermelha'] += catalogacao[par][mg_time]['vermelha'] + soma['vermelha']
                                catalogacao[par][horario]['mg'+str(i+1)]['doji'] += catalogacao[par][mg_time]['doji'] + soma['doji']
                                
                                catalogacao[par][horario]['mg'+str(i+1)]['%'] = round(100 * (catalogacao[par][horario]['mg'+str(i+1)]['verde' if catalogacao[par][horario]['dir'] == 'CALL' else 'vermelha'] / (catalogacao[par][horario]['mg'+str(i+1)]['verde'] + catalogacao[par][horario]['mg'+str(i+1)]['vermelha'] + catalogacao[par][horario]['mg'+str(i+1)]['doji']) ) )
                                
                                soma['verde'] += catalogacao[par][mg_time]['verde']
                                soma['vermelha'] += catalogacao[par][mg_time]['vermelha']
                                soma['doji'] += catalogacao[par][mg_time]['doji']
                            else:						
                                catalogacao[par][horario]['mg'+str(i+1)]['%'] = 'N/A'
            
            print('finalizado em ' + str(int(time()) - timer) + ' segundos')

    print('\n\n')

    for par in catalogacao:
        for horario in sorted(catalogacao[par]):
            ok = False		
            
            if catalogacao[par][horario]['%'] >= porcentagem:
                ok = True
            else:
                for i in range(int(martingale)):
                    if catalogacao[par][horario]['mg'+str(i+1)]['%'] >= porcentagem:
                        ok = True
                        break
            
            if ok == True:
            
                msg = Fore.YELLOW + par + Fore.RESET + ' - ' + horario + ' - ' + (Fore.RED if catalogacao[par][horario]['dir'] == 'PUT ' else Fore.GREEN) + catalogacao[par][horario]['dir'] + Fore.RESET + ' - ' + str(catalogacao[par][horario]['%']) + '% - ' + Back.GREEN + Fore.BLACK + str(catalogacao[par][horario]['verde']) + Back.RED + Fore.BLACK + str(catalogacao[par][horario]['vermelha']) + Back.RESET + Fore.RESET + str(catalogacao[par][horario]['doji'])
                
                if martingale.strip() != '':
                    for i in range(int(martingale)):
                        if str(catalogacao[par][horario]['mg'+str(i+1)]['%']) != 'N/A':
                            msg += ' | MG ' + str(i+1) + ' - ' + str(catalogacao[par][horario]['mg'+str(i+1)]['%']) + '% - ' + Back.GREEN + Fore.BLACK + str(catalogacao[par][horario]['mg'+str(i+1)]['verde']) + Back.RED + Fore.BLACK + str(catalogacao[par][horario]['mg'+str(i+1)]['vermelha']) + Back.RESET + Fore.RESET + str(catalogacao[par][horario]['mg'+str(i+1)]['doji'])
                        else:
                            msg += ' | MG ' + str(i+1) + ' - N/A - N/A' 
                           
                print(msg)
                	
                open('sinais.txt', 'a').write(str((datetime.now()).strftime('%d-%m-%Y')) + ' ' +horario + ',' + par + ',' + catalogacao[par][horario]['dir'].strip() + ',' + str(letra) + '\n')
                
                   
