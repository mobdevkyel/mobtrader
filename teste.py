from iqoptionapi.stable_api import IQ_Option
from iqoptionapi.constants import ACTIVES
import iqoptionapi.country_id as Pais
from busca import *
from melhor_payout_par import *
import time, json, logging, configparser, os, csv, sys, io
from threading import Thread
from datetime import datetime, date, timedelta
import mysql.connector

#================ GLOBAIS ==============
Preto = '\033[1;30m'
Vermelho = '\033[1;31m'
Verde = '\033[1;32m'
Amarelo = '\033[1;33m'
Azul = '\033[1;34m'
Magenta = '\033[1;35m'
Cyan = '\033[1;36m'
Cinza_Claro = '\033[1;37m'
Cinza_Escuro = '\033[1;90m'
Vermelho_Claro ='\033[1;91m'
Verde_Claro ='\033[1;92m'
Amarelo_Claro =	'\033[1;93m'
Azul_Claro ='\033[1;94m'
Magenta_Claro = '\033[1;95m'
Cyan_Claro = '\033[1;96m'
Negrito ='\033[;1m'
Inverte = '\033[;7m'
Reset = '\033[0;0m'

LC = 0
ganhos = float(0)
percas = float(0)
atual = float(0)
conta = ''
ban = float(0)
paridade = ''
padrao = ''
porcentagem = 0
WIN = 0
G1 = 0
G2 = 0
HIT = 0
win = 0
g1 = 0
g2 = 0
hit = 0
M = ''
opcao = ''
quantidade = float(0)
martingale = 0
FL = float(0)
v2 = ''
v0 = ''
c3 = False
Banca_inicial = float(0)
novo = False
STP = False
STOPLOSS = 0
STOPWIN = 0
BANCAINICIAL = 0
atu = 0
tp = ''
sistema = 0
pas = ''
log = ''
iqo_api = ''
VIT = 0
DER = 0
VR = 0

VTS = 0
mao = 1
lucros = 0
gerencia = 1
preju = 0
Nv = 10
gerenciada = False

#===================================================================================

#====================================================================================
#==================================== inicio ========================================

def verificar_se_fez_a_conexao(_iq: IQ_Option, _account_type: str = 'PRACTICE') -> bool:
    check, reason = _iq.connect()
    error_password = """{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
    requests_limit_exceeded = """{"code":"requests_limit_exceeded","message":"The number of requests has been exceeded. Try again in 10 minutes.","ttl":600}"""
    if check:
        print("Checando dados...")
        _iq.change_balance(_account_type)
        return True
    else:
        if reason == "[Errno -2] email ou senha invalida":
            print("No Network")
        elif reason == error_password:
            error_message = ast.literal_eval(error_password)
            print(error_message['message'])
        elif reason == requests_limit_exceeded:
            error_message = ast.literal_eval(requests_limit_exceeded)
            print(error_message['message'])

    print("encerrando bot, verifique seus dados.")
    return False

def format_currency_value(_currency_account: str, _value: float) -> str:
    return '$ {:,.2f}'.format(_value) if _currency_account == 'USD' else 'R$ {:,.2f}'.format(_value)

def get_color_candle(_candle: dict) -> str:
    return 'G' if _candle['open'] < _candle['close'] else 'R' if _candle['open'] > _candle['close'] else 'D'

def perfil():
    perfil = json.loads(json.dumps(iq.get_profile_ansyc()))
    
    return perfil

def timestamp_converter(_timestamp: int) -> str:
    hora = datetime.strptime(datetime.utcfromtimestamp(_timestamp).strftime(DATE_TIME_FORMAT), DATE_TIME_FORMAT)
    hora = hora.replace(tzinfo=tz.gettz('GMT'))
    return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-9]

def filter_columns(_candles: list) -> list:
    return [{k: v for k, v in candle.items() if k in {'from', 'open', 'close'}} for candle in _candles]

def adjust_catalog(_pariedade: str, _candle: dict) -> dict:
    return {
        'pariedade': _pariedade,
        'hora': timestamp_converter(_candle['from']).split(' ')[1],
        'green': 1 if get_color_candle(_candle) == 'G' else 0,
        'red': 1 if get_color_candle(_candle) == 'R' else 0,
        'doji': 1 if get_color_candle(_candle) == 'D' else 0
    }

def buscar():
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global ganhos
    global percas
    global atual
    global c3
    global opcao
    global tp

    paridade = ''
    padrao = ''
    porcentagem = 0
    WIN = 0
    G1 = 0
    G2 = 0
    HIT = 0
    win = 0
    g1 = 0
    g2 = 0
    hit = 0
    opcao = ''

    paridade, padrao, porcentagem, WIN, G1, G2, HIT, win, g1, g2, hit = catalogar()
    os.system('cls')
    if tp == 'TOURNAMENT':
        opcao = "binaria"
        inicio(ganhos, percas, atual)
    else:
        print('Buscando melhor Payout')
        opcao,percent,sta = most_profit_mode(iqo_api, paridade, 1, min_payout=0.5)
        #opcao = pay(paridade, "melhor", 1)
        time.sleep(5)
        if opcao == 'turbo':
            opcao = 'binaria'
        inicio(ganhos, percas, atual)
    mta = stop(ganhos,percas)
    
    if mta:
        print('\n!!! MOBTRADER BOT !!!')
    else:   
        if padrao == 'MHI':
            c3 = False
            MHI()
        elif padrao == 'MHI2':
            c3 = False
            MHI_2()
            
        elif padrao == 'MHI3':
            c3 = False
            MHI_3()
            
        elif padrao == 'MHI2 Maioria':
            c3 = False
            MHI2_MAIORIA()
            
        elif padrao == 'MHI3 Maioria':
            c3 = False
            MHI3_MAIORIA()
            
        elif padrao == 'Milhão Minoria':
            c3 = False
            MILHAO_MINORIA()
            
        elif padrao == 'Milhão Maioria':
            c3 = False
            MILHAO_MAIORIA()
            
        elif padrao == 'Padrão Impar':
            c3 = False
            PADRAO_IMPAR()
            
        elif padrao == 'Torres Gêmeas':
            c3 = False
            TORRES_GEMEAS()
            
        elif padrao == 'Três Mosqueteiros':
            c3 = False
            TRES_MOSQUETEIROS()
            
        elif padrao == 'C3':
            c3 = True
            C3()
            #buscar()
            
        elif padrao == 'Melhor de 3':
            c3 = False
            MELHOR_DE_3()
            
        elif padrao == 'Padrão 23':
            c3 = False
            PADRAO_23()
            
        elif padrao == 'MHI Maioria':
            c3 = False
            MHI_MAIORIA()       

def buscar2():
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global ganhos
    global percas
    global atual
    global c3
    global opcao
    global iqo_api
    

    paridade, padrao, porcentagem, WIN, G1, G2, HIT, win, g1, g2, hit = catalogar()
    os.system('cls')
    if tp == 'TOURNAMENT':
        opcao = "binaria"
        inicio(ganhos, percas, atual)
    else:
        print('Buscando melhor Payout')
        opcao,percent,sta = most_profit_mode(iqo_api, paridade, 1, min_payout=0.5)
        #opcao = pay(paridade, "melhor", 1)
        time.sleep(5)
        if opcao == 'turbo':
            opcao = 'binaria'
        inicio(ganhos, percas, atual)

    print('DESEJA CATALOGAR NOVAMENTE OU CONFIRMAR ESTA ESCOLHA ACIMA? LEMBRANDO QUE ESTA ERA A MELHOR NO MOMENTO QUE VERIFIQUEI!')
    print(f"1 = FAZER NOVA CATALOGAÇÃO\n2 = INICIAR NA MOEDA {paridade} MESMO\n\n")
    selecao = input("DIGITE: ")
    
    

    if selecao == '1':
        buscar2()
    elif selecao == '2':
        if padrao == 'MHI':
            MHI()
        elif padrao == 'MHI2':
            c3 = False
            MHI_2()
            
        elif padrao == 'MHI3':
            c3 = False
            MHI_3()
            
        elif padrao == 'MHI2 Maioria':
            c3 = False
            MHI2_MAIORIA()
            
        elif padrao == 'MHI3 Maioria':
            c3 = False
            MHI3_MAIORIA()
            
        elif padrao == 'Milhão Minoria':
            c3 = False
            MILHAO_MINORIA()
            
        elif padrao == 'Milhão Maioria':
            c3 = False
            MILHAO_MAIORIA()
            
        elif padrao == 'Padrão Impar':
            c3 = False
            PADRAO_IMPAR()
            
        elif padrao == 'Torres Gêmeas':
            c3 = False
            TORRES_GEMEAS()
            
        elif padrao == 'Três Mosqueteiros':
            c3 = False
            TRES_MOSQUETEIROS()
            
        elif padrao == 'C3':
            c3 = True
            buscar()
            #C3()
            
        elif padrao == 'Melhor de 3':
            c3 = False
            MELHOR_DE_3()
            
        elif padrao == 'Padrão 23':
            c3 = False
            PADRAO_23()
            
        elif padrao == 'MHI Maioria':
            c3 = False
            MHI_MAIORIA()
               
def inicio(ganhos, percas, atual):
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global opcao
    global STP
    global VIT
    global DER
    global BANCAINICIAL

    
    os.system('cls')
    print(f'{Amarelo}______  ___       ______  ________                _________{Reset}')              
    print(f'{Amarelo}___   |/  /______ ___  /_ ___  __/______________ _______  /_____ ________{Reset}')
    print(f'{Amarelo}__  /|_/ / _  __ \__  __ \__  /   __  ___/_  __ `/_  __  / _  _ \__  ___/{Reset}')
    print(f'{Amarelo}_  /  / /  / /_/ /_  /_/ /_  /    _  /    / /_/ / / /_/ /  /  __/_  /{Reset}')    
    print(f'{Amarelo}/_/  /_/   \____/ /_.___/ /_/     /_/     \__,_/  \__,_/   \___/ /_/ {Reset}\n')  
    print(f'{Azul}FULL MHI V 1.0{Reset} - Contato: +55 (11) 9 7615-9233\n')    
    print(f'Ganhos: {Verde}{round(ganhos, 2)}{Reset} || Percas: {Vermelho}{round(percas, 2)}{Reset} || Locros: {Amarelo}{round(atual, 2)}{Reset} || Conta: {Vermelho}{conta}{Reset} || Opção: {Amarelo}{opcao}{Reset}\n')
    print(f'VITORIAS: {Verde}{VIT}{Reset} // DERROTAS: {Vermelho}{DER}{Reset} // SUA BANCA INICIAL: {Vermelho}{round(BANCAINICIAL, 2)}{Reset} // SUA BANCA ATUAL: {Amarelo}{round(banca(), 2)}{Reset}\n')
    print(f'MELHOR MOEDA: {Verde}{paridade}{Reset} || PADRÃO: {Verde}{padrao}{Reset}\nPORCENTAGEM DE ACERTOS: {Verde}{porcentagem}%{Reset}\nVITORIAS DE PRIMEIRA: {Verde}{WIN} - {win} VITORIAS{Reset}\nVITORIAS NO GALE 1: {Verde}{G1} - {g1} VITORIAS{Reset}\nVITORIAS NO GALE 2: {Verde}{G2} - {g2} VITORIAS{Reset}\nHIT: {Vermelho}{HIT} - {hit} DERROTAS{Reset}')
    print(f'FONTE: {Azul}catalogador.ml{Reset}')
    print(f'*********************************************************************************************')

    #if STP:
        #sys.exit()

def stop(ganhos,percas):
    global stop_loss
    global stop_win
    global atual
    global STP

            
    if atual <= float('-' + str(abs(stop_loss))):
        STP = True
        inicio(ganhos, percas, atual)
        print('Stop Loss batido!')
        print('Vamos finalizar por hoje né!!!!!')
        return STP
        
        
        
    if atual >= float(abs(stop_win)):
        STP = True
        inicio(ganhos, percas, atual)
        print('STOP WIN ATINGIDO')
        print('VAMOS POR ESSA NA CONTA E VOLTAR SO AMANHÃ NÉ!!!!')
        return STP
        
def sorosgale(ativo,quantidade, direcao, tempo,hora,opcao,NV,MT,CT,tempo2):
    global martingale
    lucro_total = 0
    nivel = 1
    mao = 1
    lucro = 0
    qt = (quantidade / 2)
    entrada = 'R$ {:,.2f}'.format(qt)
    print('PERCA: '+str(quantidade)+' | ENTRADA INICIAL: '+str(entrada)+' - '+str(ativo))
    

    while True:
        
        resultado,lucro,stop = entradas(ativo,(quantidade / 2)+lucro,direcao,tempo,opcao,NV,MT,CT)
        
        if mao > 2:
            nivel += 1
            mao = 1
        if resultado == 'win':
            
            if nivel > int(martingale):
                entrada = 'R$ {:,.2f}'.format(quantidade)
                entrada2 = 'R$ {:,.2f}'.format(lucro_total)
                print('SOROSGALE FINALIZADO, Perca: '+str(entrada)+' / Ganho: '+str(entrada2)+' - '+str(ativo))
                
                break
            else:
                entrada = 'R$ {:,.2f}'.format(quantidade)
                lucro_total += lucro
                print('SOROSGALE = Mão: '+str(mao)+' - Nivel: '+str(nivel)+' | Perca: '+str(entrada)+' - '+str(ativo))
                mao += 1
        else:
            if nivel > int(martingale):
                entrada = 'R$ {:,.2f}'.format(quantidade)
                entrada2 = 'R$ {:,.2f}'.format(lucro_total)
                print('SOROSGALE FINALIZADO, Perca: '+str(entrada)+' / Ganho: '+str(entrada2)+' - '+str(ativo))
                
                break
            else:
                entrada = 'R$ {:,.2f}'.format(quantidade)
                print('SOROSGALE = Mão: '+str(mao)+' - Nivel: '+str(nivel)+' | Perca: '+str(entrada)+' - '+str(ativo))
                lucro_total = 0
                quantidade += quantidade / 2
                mao += 1
            
        
        if lucro_total >= quantidade:
            entrada = 'R$ {:,.2f}'.format(quantidade)
            entrada2 = 'R$ {:,.2f}'.format(lucro_total)
            print('SOROSGALE FINALIZADO, Perca: '+str(entrada)+' / Ganho: '+str(entrada2)+' - '+str(ativo))
            time.sleep(5)
            buscar()
            break
        else:
            entrada = 'R$ {:,.2f}'.format(quantidade)
            entrada2 = 'R$ {:,.2f}'.format(lucro_total)
     
def Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2):
    global LC
    global stop_loss
    global stop_win
    global BANCAINICIAL
    global ganhos
    global percas
    global atual
    global ban
    global v2
    global v0
    global c3
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global martingale
    global VIT
    global DER
    global VTS
    
    if c3 == False:
        if isinstance(id, int):
                            
            while True:
                    
                status,lucro = iq.check_win_v4(id)
                if status:
                                        
                    if lucro < 0 and NV >= 1 and CT < (int(martingale) - 1):
                        NV -= 1
                        CT += 1
                        percas += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        inicio(ganhos, percas, atual)
                        NOVA_ENTRADA = float(quantidade)*MT
                        entrada = 'R$ {:,.2f}'.format(NOVA_ENTRADA)
                        print(f'{Amarelo}MARTINGALE: {Reset}'+str(CT)+' NO SINAL DAS '+str(hora)+', ATIVO: '+str(ativo)+' - '+str(entrada))
                        #print('Lucro:' + str(round(lucro, 2)))
                        status,id = iq.buy(NOVA_ENTRADA, ativo, direcao, tempo)
                        
                        Verifica_status(id,ativo,NOVA_ENTRADA,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                        break
                    
                    elif lucro > 0:
                        VTS += 1
                        ganhos += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        VIT += 1
                        lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                        inicio(ganhos, percas, atual)
                        #print('Banca: ' + str(round(banca(), 2)))
                        #lucros = float(round(banca(), 2)) - float(round(Banca_inicial, 2))
                        #print('Lucros: ' + str(round(lucros, 2)))
                        print(f'{Verde}{ativo} | {direcao.upper()} | VITORIA{Reset}')
                        print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(5)
                        buscar()
                        break


                    elif lucro < 0:
                        VTS = 0
                        percas += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        DER += 1
                        lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                        inicio(ganhos, percas, atual)
                        #print('Banca: ' + str(round(banca(), 2))) 
                        #lucros = float(round(banca(), 2)) - float(round(Banca_inicial, 2))
                        #print('Lucros: ' + str(round(lucros, 2)))                     
                        print(f'{Vermelho}{ativo} | {direcao.upper()} | DERROTA{Reset}')
                        print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(5)
                        buscar()
                        
                        break
                    

                    else:
                        print(f'{Azul}{ativo} | {direcao.upper()} | DOJI{Reset}')
                        print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(5)
                        buscar()

                                            
                                            
                    stop(ganhos,percas)
    else:
        if isinstance(id, int):
                                        
            while True:
                    
                status,lucro = iq.check_win_v4(id)
                if status:
                    
                    if lucro < 0 and NV >= 1 and CT < (int(martingale) - 1):
                        NV -= 1
                        CT += 1
                        percas += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        inicio(ganhos, percas, atual)
                        NOVA_ENTRADA = float(quantidade)*MT
                        entrada = 'R$ {:,.2f}'.format(NOVA_ENTRADA)
                        print(f'{Amarelo}MARTINGALE: {Reset}'+str(CT)+' NO ATIVO: '+str(ativo)+' - '+str(entrada))
                        #print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(60)
                        dir = False
                        velas = iq.get_candles(ativo, 60, 5, time.time())
                        velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                        velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                        velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                        velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                        velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
                        
                        #print(cores)
                        if velas[4] == 'verde':
                            dir = 'call'
                            print(f'{Verde}{padrao} = {dir}{Reset}')
                        elif velas[4] == 'vermelha':
                            dir = 'put'
                            print(f'{Vermelho}{padrao} = {dir}{Reset}')
                        else:
                            dir = False
                            buscar()
                            break
                             
                                        
                        if dir:
                            status,id = iq.buy(NOVA_ENTRADA, ativo, dir, tempo)
                            
                            Verifica_status(id,ativo,NOVA_ENTRADA,dir,tempo,opcao,hora,NV,MT,CT,tempo2)
                            
                            break
                    
                    elif lucro > 0:
                        VTS += 1
                        ganhos += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        VIT += 1
                        lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                        inicio(ganhos, percas, atual)
                        #print('Banca: ' + str(round(banca(), 2)))
                        #lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                        #print('Lucros: ' + str(round(lucros, 2)))
                        print(f'{Verde}{ativo} | {direcao.upper()} | VITORIA{Reset}')
                        print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(5)
                        buscar()
                        break

                    elif lucro < 0:
                        VTS = 0
                        percas += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        DER += 1
                        lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                        inicio(ganhos, percas, atual)
                        #print('Banca: ' + str(round(banca(), 2))) 
                        #lucros = float(round(banca(), 2)) - float(round(Banca_inicial, 2))
                        #print('Lucros: ' + str(round(lucros, 2)))                     
                        print(f'{Vermelho}{ativo} | {direcao.upper()} | DERROTA{Reset}')
                        print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(5)
                        buscar()
                        
                        break
                    

                    else:
                        print(f'{Azul}{ativo} | {direcao.upper()} | DOJI{Reset}')
                        print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(5)
                        buscar()
                                            
                                            
                    stop(ganhos,percas)

def Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2):
    global LC
    global stop_loss
    global stop_win
    global BANCAINICIAL
    global ganhos
    global percas
    global atual
    global ban
    global v2
    global v0
    global c3
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global VIT
    global DER
    global VTS
    
    if c3 == False:
        if isinstance(id, int):
        #ui.listWidget_2.insertItem(0, f'{id} {ativo}')               
            while True:
                
                status,lucro = iq.check_win_digital_v2(id)
                if status:
                    
                    if lucro < 0 and NV >= 1 and CT < (int(martingale) - 1):
                        percas += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        inicio(ganhos, percas, atual)                                                   
                        NV -= 1
                        CT += 1
                        NOVA_ENTRADA = float(quantidade)*MT
                        entrada = 'R$ {:,.2f}'.format(NOVA_ENTRADA)
                        print(f'{Amarelo}MARTINGALE: {Reset}'+str(CT)+' NO ATIVO: '+str(ativo)+' - '+str(entrada))
                        #print('Lucro:' + str(round(lucro, 2)))
                        
                        status,id = iq.buy_digital_spot(ativo, NOVA_ENTRADA, direcao, tempo)
                        
                        Verifica_status_D(id,ativo,NOVA_ENTRADA,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                        break
                    
                    elif lucro > 0:
                        VTS += 1
                        ganhos += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        VIT += 1
                        lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                        inicio(ganhos, percas, atual)
                        #print('Banca: ' + str(round(banca(), 2))) 
                        #lucros = float(round(banca(), 2)) - float(round(Banca_inicial, 2))
                        print(f'{Verde}{ativo} | {direcao.upper()} | VITORIA{Reset}')
                        print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(5)
                        buscar()
                        break

                    elif lucro < 0:
                        VTS = 0
                        percas += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        DER += 1
                        lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                        inicio(ganhos, percas, atual)
                        #print('Banca: ' + str(round(banca(), 2))) 
                        #lucros = float(round(banca(), 2)) - float(round(Banca_inicial, 2))
                        #print('Lucros: ' + str(round(lucros, 2)))                     
                        print(f'{Vermelho}{ativo} | {direcao.upper()} | DERROTA{Reset}')
                        print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(5)
                        buscar()
                        
                        break
                    

                    else:
                        print(f'{Azul}{ativo} | {direcao.upper()} | DOJI{Reset}')
                        print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(5)
                        buscar()

                                            
                    stop(ganhos,percas)
    else:
        if isinstance(id, int):
        #ui.listWidget_2.insertItem(0, f'{id} {ativo}')               
            while True:
                
                status,lucro = iq.check_win_digital_v2(id)
                if status:
                                        
                    if lucro < 0 and NV >= 1 and CT < (int(martingale) - 1):
                        percas += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        inicio(ganhos, percas, atual)                                                   
                        NV -= 1
                        CT += 1
                        NOVA_ENTRADA = float(quantidade)*MT
                        entrada = 'R$ {:,.2f}'.format(NOVA_ENTRADA)
                        print(f'{Amarelo}MARTINGALE: {Reset}'+str(CT)+' NO ATIVO: '+str(ativo)+' - '+str(entrada))
                        #print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(60)
                        dir = False
                        velas = iq.get_candles(ativo, 60, 5, time.time())
                        velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                        velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                        velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                        velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                        velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
                        
                        #print(cores)
                        if velas[4] == 'verde':
                            dir = 'call'
                            print(f'{Verde}{padrao} = {dir}{Reset}')
                        elif velas[4] == 'vermelha':
                            dir = 'put'
                            print(f'{Vermelho}{padrao} = {dir}{Reset}')
                        else:
                            dir = False
                            buscar()
                            break
                             
                                        
                        if dir:
                            status,id = iq.buy_digital_spot(ativo, NOVA_ENTRADA, dir, tempo)
                            
                            Verifica_status_D(id,ativo,NOVA_ENTRADA,dir,tempo,opcao,hora,NV,MT,CT,tempo2)
                            
                            break
                    
                    elif lucro > 0:
                        VTS += 1
                        ganhos += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        VIT += 1
                        lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                        inicio(ganhos, percas, atual)
                        #print('Banca: ' + str(round(banca(), 2))) 
                        #lucros = float(round(banca(), 2)) - float(round(Banca_inicial, 2))
                        print(f'{Verde}{ativo} | {direcao.upper()} | VITORIA{Reset}')
                        print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(5)
                        buscar()
                        break

                    elif lucro < 0:
                        VTS = 0
                        percas += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        DER += 1
                        lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                        inicio(ganhos, percas, atual)
                        #print('Banca: ' + str(round(banca(), 2))) 
                        #lucros = float(round(banca(), 2)) - float(round(Banca_inicial, 2))
                        #print('Lucros: ' + str(round(lucros, 2)))                     
                        print(f'{Vermelho}{ativo} | {direcao.upper()} | DERROTA{Reset}')
                        print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(5)
                        buscar()
                        
                        break
                    

                    else:
                        print(f'{Azul}{ativo} | {direcao.upper()} | DOJI{Reset}')
                        print('Lucro:' + str(round(lucro, 2)))
                        time.sleep(5)
                        buscar()

                                            
                    stop(ganhos,percas)

def entradas(ativo,entrada,sentido,tempo,op,NV,MT,CT):
    global LC
    global stop_loss
    global stop_win
    global Banca_inicial
    global ganhos
    global percas
    global atual
    global ban
    global v2
    global v0
    global c3
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global BANCAINICIAL
    global STOPLOSS
    global STOPWIN
    global martingale
    
    
     
    if op == 'digital':
        status,id = iq.buy_digital_spot(str(ativo),float(entrada),str(sentido), int(tempo))
        

        if status:
            # STOP WIN/STOP LOSS
            banca_att = banca()
            stop_loss = False
            stop_win = False
            
            if round((banca_att - float(BANCAINICIAL)), 2) <= (abs(float(STOPLOSS)) * -1.0):
                stop_loss = True
                
            if round((banca_att - float(BANCAINICIAL)), 2) >= abs(float(STOPWIN)):
                stop_win = True
            
            while True:
                
                status,lucro = iq.check_win_digital_v2(id)
                if status:

                    if lucro > 0:
                        ganhos += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        return 'win',round(lucro, 2),stop_win
                        
                    else:
                        percas += round(lucro, 2)
                        atual += round(lucro, 2)
                        ban = round(banca(), 2)
                        return 'loss',round(lucro, 2),stop_loss
                    break
                
    
    elif op == 'binaria':
        status,id = iq.buy(ativo, entrada, sentido, tempo)


        if status:
            
            # STOP WIN/STOP LOSS
            banca_att = banca()
            stop_loss = False
            stop_win = False
            
            if round((banca_att - float(BANCAINICIAL)), 2) <= (abs(float(STOPLOSS)) * -1.0):
                stop_loss = True
                
            if round((banca_att - float(BANCAINICIAL)), 2) >= abs(float(STOPWIN)):
                stop_win = True

            while True:
                
                status,lucro = iq.check_win_v4(id)
                
                if status:
                    if lucro > 0:
                        
                        return 'win',round(lucro, 2),stop_win
                    else:
                    
                        return 'loss',round(lucro, 2),stop_loss
                    break

def Gales(tipo, valor, payout):
    if tipo == 'simples':
        return valor * 2.2
    else:
    
        lucro_esperado = float(valor) * float(payout)
        perca = valor
        while True:
            if round(float(valor) * float(payout), 2) > round(float(abs(perca)) + float(lucro_esperado), 2):
                return round(valor, 2)
                break
            valor += 0.01

def payout(par, tipo, timeframe = 1):
    if tipo == 'binaria':
        a = iq.get_all_profit()
        return int(100 * a[par]['binary'])
        
    elif tipo == 'digital':
    
        iq.subscribe_strike_list(par, timeframe)
        while True:
            d = iq.get_digital_current_profit(par, timeframe)
            if d != False:
                d = int(d)
                break
            time.sleep(1)
        iq.unsubscribe_strike_list(par, timeframe)
        return d
    iq.subscribe_strike_list(par, 1)
    while True:
        d = iq.get_digital_current_profit(par, 1)
        if d != False:
            d = round(int(d) / 100, 2)
            break
        time.sleep(1)
    iq.unsubscribe_strike_list(par, 1)
    
    return d

def checar_ativo(ativo, opcao,tempo2):
    tentar = ''
    ATIVOS = iq.get_all_open_time()
    
    if ATIVOS[opcao][ativo]["open"] == False:
        if opcao == 'digital':
            tentar = 'turbo'
            print('Digital: Fexado')
            if ATIVOS[tentar][ativo]["open"] == False:
                
                return False, tentar
            else:
                print('Binaria: Aberto')
                return True, tentar

        elif opcao == 'binaria':
            tentar = 'turbo'
            print('Binaria: Fexado')
            if ATIVOS[tentar][ativo]["open"] == False:
                
                return False, tentar
            else:
                print('Digital: Aberto')
                return True, tentar
            
    else:
        tentar = opcao
        return True, tentar

def pay(ativo, opcao, tempo):
    at = ativo
    DI = 0
    BI = 0
               
    BI = payout(ativo, 'turbo', tempo)
    BI = int(BI)
    
    DI = payout(ativo, 'digital', tempo)
    DI = int(DI)

    print('Payout = Digital: '+str(DI)+'%, Binarias: '+str(BI)+'%'+' - '+str(at))
    
    if opcao == 'melhor':
        opcao = 'digital' if DI > BI else 'binaria'
        print(f'Ativo {at}, melhor payout {opcao}')
        st,op = checar_ativo(at,opcao,tempo)
        if st:
            print('O ativo: '+str(at)+', esta ok na '+str(op))
            return op
                        
        else:
            print('O ativo: '+str(at)+', esta fechado na binarias e na digital')
        
        

    else:
        st,op = checar_ativo(at, opcao,tempo)
        if st:
            print('O ativo: '+str(at)+', esta ok na '+str(op))
            return op     
        else:
            print('O ativo: '+str(at)+', esta fechado na binarias e na digital')
        
def horario():
    hora = datetime.now()
    hora = hora.strftime('%H:%M')
    return hora

def banca():
    return iq.get_balance()

def MHI():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 3, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
            velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)

                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)
          
def MHI_2():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 3, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
            velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                time.sleep(60)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)

def MHI_3():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 3, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
            velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                time.sleep(120)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)
    
def MHI_MAIORIA():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 3, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
            velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)
    
def MHI2_MAIORIA():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 3, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
            velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                time.sleep(60)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)

def MHI3_MAIORIA():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 3, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
            velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                time.sleep(120)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)

def MILHAO_MAIORIA():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 5, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
            velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
            velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2] + ' ' + velas[3]	+ ' ' + velas[4]	
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)

def MILHAO_MINORIA():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 5, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
            velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
            velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2] + ' ' + velas[3]	+ ' ' + velas[4]	
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)

def PADRAO_IMPAR():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 3, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
            velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cor = velas[2]
            #print(cores)

            if cor == 'verde':
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif cor == 'vermelha':
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)

def MELHOR_DE_3():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 4, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
            velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
            
            
            cores = velas[1] + ' ' + velas[2] + ' ' + velas[3]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                time.sleep(120)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)

def TRES_MOSQUETEIROS():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if minutos == 2.58  or minutos == 7.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 1, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                        
            cor = velas[0]	
            #print(cor)

            if cor == 'verde':
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif cor == 'vermelha':
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)

def C3():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL
    global v2
    global v0
    global c3


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    c = []
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 5, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
            velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
            velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2] + ' ' + velas[3] + ' ' + velas[4]
            c.append(velas[2])
            c.append(velas[0])

            v2 = c[0]
            v0 = c[1]
            #print(cores)
        
            if velas[4] == 'verde':
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif velas[4] == 'vermelha':
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)

def TORRES_GEMEAS():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 3.58 and minutos <= 5) or minutos >= 8.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 4, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
            velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
            
            
            cores = velas[3]		
            #print(cores)

            if cores == 'verde':
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif cores == 'vermelha':
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)
   
def PADRAO_23():
    global LC
    global stop_loss
    global stop_win
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global paridade
    global padrao
    global porcentagem
    global WIN
    global G1
    global G2
    global HIT
    global win
    global g1
    global g2
    global hit
    global quantidade
    global opcao
    global STP
    global martingale
    global FL


    tempo = 1
    NV = int(martingale)
    MT = float(FL)
    CT = 0
    tempo2 = 'M1'

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
            
        BANCA_ATUAL = banca()
                        
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if minutos == 0.58 or minutos == 5.58 else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            velas = iq.get_candles(par, 60, 1, time.time())
            
            velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            
            
            cores = velas[0]	
            #print(cores)
            if cores == 'verde':
                dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif cores == 'vermelha':
                dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                dir = False
                STP = True   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                                       
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    print(f'Direção: {dir}\n')
                
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                        
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                    break
                    
        time.sleep(1)

def gerenciamento(resultado, lucro, entrada):
    global BANCAINICIAL
    global gerencia
    global mao
    global preju
    global STOPLOSS
    global VTS
    global VR
    global Nv
    global lucros
        
    
    if resultado == 'win':
        
        if int(VTS) >= 2:
            print('REINICIANDO GERENCIAMENTO')
            entrada = float(VR)
            preju = 0
            gerencia = 1
            mao = 1
            BANCAINICIAL = banca()
            VTS = 0
            lucros = 0

            return entrada
            
        else:
            mao += 1
            entrada = float(entrada) + float(lucro)
            preju = 0

            return entrada
            
    else:
        
        if int(gerencia) == int(Nv) and mao == 2:
            print('REINICIANDO GERENCIAMENTO')
            entrada = float(VR)
            preju = 0
            gerencia = 1
            mao = 1
            BANCAINICIAL = banca()
            VTS = 0
            lucros = 0

            return entrada

        gerencia += 1
        mao = 1
        preju = float(BANCAINICIAL) - float(banca())
        entrada = float(preju) / 2
        VTS = 0
    
        return entrada    

if atu == 0:
    atu = 1
    #======================================================================================
    #:===============================================================:#
    os.system('cls')
    print('INFORME SEU EMAIL\n')
    login = input('EMAIL: ')
    if login == '':
        login = ''
    password = input('SENHA: ')
    if password == '':
        password = ''

    os.system('cls')
    print('INFORME O TIPO DA CONTA\n')
    print('1 = CONTA TREINO')
    print('2 = CONTA REAL')
    print('3 = TORNEIO\n')
    ct = input('ESCOLHA UM NUMERO: ')
    if ct == '1':
        account_type = 'PRACTICE'
    elif ct == '2':
        account_type = 'REAL'
    elif ct == '3':
        account_type = 'TOURNAMENT'
    tp = account_type

    os.system('cls')
    print('Informe o valor da primeira entrada')
    VR = int(input('Valor: '))
    quantidade = float(VR)

    STOPLOSS = float(input('Stop loss: '))
    STOPWIN = float(input('Stop win: '))
    stop_win = float(STOPWIN)
    stop_loss = float(STOPLOSS)

    os.system('cls')
    print('Informe o sistema de gale')
    print('1 = Martingale simples')
    print('2 = Sair\n')
    sistema = int(input('ESCOLHA UM NUMERO: '))
    if sistema == 1:
        os.system('cls')
        print('Informe a quantidade de martingales')
        GL = int(input('Gales: '))
        martingale = GL
        martingale += 1
        print('\nFator multiplicador do gale')
        FL = float(input('Multiplicar por: '))

    elif sistema == 2:
        print('***')
        

    # Aqui começa a configuração da API, não alterar
    #:===============================================================:#
    iq = IQ_Option(login, password)
    iqo_api = iq
    if not verificar_se_fez_a_conexao(iq, account_type):
        sys.exit(0)

    conta = account_type
    currency_account = iq.get_currency()
    account_balance = iq.get_balance()
    DATE_TIME_FORMAT = '%Y-%m-%d %H:%M'
    os.system('cls')
    x = perfil()
    nome = str(x['name'])
    saldo = (f"{'Conta de treino saldo' if account_type == 'PRACTICE'  else 'Saldo'}: {Amarelo}{format_currency_value(currency_account, account_balance)}{Reset}")
    print(saldo)
    BANCAINICIAL = float(round(banca(), 2))
    time.sleep(3)
    #======================================================================================
    
    buscar2()
else:
    buscar()

    

