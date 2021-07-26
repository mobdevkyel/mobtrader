from iqoptionapi.stable_api import IQ_Option
from iqoptionapi.constants import ACTIVES
import iqoptionapi.country_id as Pais
from variaveislista import *
from criarsinallista import *
import time, json, logging, configparser, os, csv, sys, io
from threading import Thread
from datetime import datetime, date, timedelta
from urllib.request import urlretrieve
import requests




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

def timestamp_converter2(x):  # Função para converter timestamp
    hora = datetime.strptime(datetime.utcfromtimestamp(
        x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))

    return hora

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

def banca():
    return iq.get_balance()

def tendencia(par,tempo):
    #par = 'AUDCAD'
    timeframe = tempo

    velas = iq.get_candles(par, (int(timeframe) * 60), 25,  time.time())

    ultimo = round(velas[0]['close'], 4)
    primeiro = round(velas[-1]['close'], 4)

    diferenca = abs( round( ( (ultimo - primeiro) / primeiro ) * 100, 3) )
    tendencia = "CALL" if ultimo < primeiro and diferenca > 0.01 else "PUT" if ultimo > primeiro and diferenca > 0.01 else False
    
    return tendencia

def datas():
    hora = datetime.now()
    hora = hora.strftime('%H:%M:%S')
    data_atual = date.today()
    data_em_texto = '{}/{}/{}'.format(data_atual.day,data_atual.month,data_atual.year)
    return data_em_texto

def horario():
    hora = datetime.now()
    hora = hora.strftime('%H:%M:%S')
    return hora

def telegram(timeframe,hora2,paridade,direcao,gales,tipo,re,qual):
    global nomeN
    global velasM
    global DER
    global VIT
    global soros
    
    info = ''                
    if qual == 1:
        info = "-1001405795828"
    elif qual == 2:
        info = "-598251971"

    chat_id = str(info)

    if tipo == "inicial":
        msg = f'''
        ⚠️⚠️ Atenção Traders!!! ⚠️⚠️

        Possivel entrada de {timeframe} as {hora2}

        🐔 Até {gales} Gales.
        💪🏻 Soros nivel {soros}
        
        Trader {nomeN} operando bot celular.

        🏴‍☠️ Paridade: {paridade}
        🔰 Direção: {direcao}
        📊 Resultado: {re}

        😱 Vitorias: {VIT}
        😱 Derrotas: {DER}
        ------------------------------------
        '''
    elif tipo == "final":
        msg = f'''
            ⚠️⚠️ Atenção Traders!!! ⚠️⚠️

        Resultado do trader {nomeN}.

        
        🏴‍☠️ Paridade: {paridade}
        🔰 Direção: {direcao}
        📊 Resultado: {re}

        😱 Vitorias: {VIT}
        😱 Derrotas: {DER}
        ------------------------------------
        '''
    elif tipo == "contra":
        msg = f'''
        ⚠️⚠️ Atenção Traders!!! ⚠️⚠️

        Entrada recusada {hora2} - {timeframe}

        🐔 Até {gales} Gales.
        
        Presente do Trader: {nomeN}

        🏴‍☠️ Paridade: {paridade}
        🔰 Direção: {direcao}
        📊 Resultado: {re}

        😱 Vitorias: {VIT}
        😱 Derrotas: {DER}
        ------------------------------------
        '''

    def send_message(chat_id, msg):
        requests.post('https://api.telegram.org/bot1124089653:AAFvtVnYoulqRCU3g80z0qM6hn__QIQKYeE/sendMessage', {'chat_id': chat_id, 'text': str(msg)})



    #msg = "testando bot"
    send_message(chat_id, msg)


# ============================================================== #
def alerta(entrada,saida,lucro,resultado,direcao,extrategia,moeda,data,horario):
    global chaveN
    global nome
    global conta
        
    data = {'chave': f'{chaveN}','nome': f'{nome}','moeda': f'{moeda}','direcao': f'{direcao}','extrategia': f'{extrategia}','data': f'{data}','entrada': f'{entrada}','saida': f'{saida}','lucro': f'{lucro}','resultado': f'{resultado}','conta': f'{conta}','hora': f'{horario}', 'acao': 'Cadastrar'}
    url = "http://mobtrader.atwebpages.com/alert/jogadores.php"    
    resp = requests.post(url, data)

def inicio():
    global conta
    global ban
    global opcao
    global VIT
    global DER
    global BANCAINICIAL
    global quantidade
    global gales
    global soros
    global ganhos
    global percas
    global atual
        
    conta2 = 'REAL'
    Mostra = ''
    if email == 'ezequieleoss1986@gmail.com':
        Mostra = conta2
    else:
        Mostra = conta   
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{Amarelo}______  ___       ______  ________                _________{Reset}')              
    print(f'{Amarelo}___   |/  /______ ___  /_ ___  __/______________ _______  /_____ ________{Reset}')
    print(f'{Amarelo}__  /|_/ / _  __ \__  __ \__  /   __  ___/_  __ `/_  __  / _  _ \__  ___/{Reset}')
    print(f'{Amarelo}_  /  / /  / /_/ /_  /_/ /_  /    _  /    / /_/ / / /_/ /  /  __/_  /{Reset}')    
    print(f'{Amarelo}/_/  /_/   \____/ /_.___/ /_/     /_/     \__,_/  \__,_/   \___/ /_/ {Reset}\n')  
    print(f'{Azul}MOBTRADER LISTAS 2.3.6(VIP){Reset} - Contato: +55 (11) 9 7615-9233\n')    
    print(f'Ganhos: {Verde}{round(ganhos, 2)}{Reset} || Percas: {Vermelho}{round(percas, 2)}{Reset} || Locros: {Amarelo}{round(atual, 2)}{Reset}\nConta: {Azul}{Mostra}{Reset}')
    print(f'VITORIAS: {Verde}{VIT}{Reset} // DERROTAS: {Vermelho}{DER}{Reset}\nSUA BANCA INICIAL: {Azul}{round(BANCAINICIAL, 2)}{Reset}\nSUA BANCA ATUAL: {Amarelo}{round(banca(), 2)}{Reset}')
    print(f'GALES: {Verde}{gales}{Reset} || SOROS MÃOS: {Verde}{soros}{Reset}\nENTRADA: {Verde}{round(quantidade, 2)}{Reset}')
    print(f'*********************************************************************************************')

def Verifica_status(id,ativo,quant,direcao,tempo,opcao,hora2,NV,MT,CT,tempo2):
    global BANCAINICIAL
    global ganhos
    global percas
    global atual
    global ban
    global VIT
    global DER
    global conta
    global email
    global sr
    global ONLINE
    global MULT
    global entrada
    global soros
    global quantidade
    global tele
    global ativar_soros
    global ativar_sorogale
    global Sorogale
    global sg
      
    if isinstance(id, int):
        result = ''                
        while True:

            data = datas()
            hora = horario()   
            padrao = 'LISTA'

            status,lucro = iq.check_win_v4(id)
            if status:
                
                if lucro < 0 and NV > 0:
                    NV -= 1
                    CT += 1
                    percas += round(lucro, 2)
                    atual += round(lucro, 2)
                    ban = round(banca(), 2)
                    
                    NOVA_ENTRADA = float(quant)*MT
                    entrada2 = 'R$ {:,.2f}'.format(NOVA_ENTRADA)
                    inicio()
                    print(f'{Amarelo}MARTINGALE: {Reset}'+str(CT)+ ' ' + ativo.upper() + ' ' +str(hora)+', ATIVO: '+str(ativo)+' - '+str(entrada2))
                        
                    status,id = iq.buy(NOVA_ENTRADA, ativo, direcao, tempo)
                    #Verifica_status(id,ativo,NOVA_ENTRADA,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                    if MULT:
                        Lm = Thread(target=Verifica_status, args=(id,ativo,NOVA_ENTRADA,direcao,tempo,opcao,hora,NV,MT,CT,tempo2,))
                        Lm.daemon = True
                        Lm.start()
                    else:
                        Verifica_status(id,ativo,NOVA_ENTRADA,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                    
                    

                elif lucro > 0:
                    #VTS += 1
                    ganhos += round(lucro, 2)
                    atual += round(lucro, 2)
                    ban = round(banca(), 2)
                    VIT += 1
                    lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                    
                                                                             
                    
                    if CT == 1:
                        if ativar_soros:
                            sr = 0
                            quantidade = float(entrada)
                        result = 'Win no Gale 1 ✅🐔'    
                        alerta(round(quant, 2),round(lucro, 2),round(lucros, 2),"G1",direcao.upper(),padrao.upper(),ativo,data,hora)
                    elif CT == 2:
                        if ativar_soros:
                            sr = 0
                            quantidade = float(entrada)
                        result = 'Win no Gale 2 ✅🐔🐔' 
                        alerta(round(quant, 2),round(lucro, 2),round(lucros, 2),"G2",direcao.upper(),padrao.upper(),ativo,data,hora)
                    else:
                        if ativar_soros:
                            sr += 1
                            if soros > 0:
                                if sr > soros:
                                    quantidade = float(entrada)
                                    sr = 0
                                    print(f'SOROS NIVEL {soros} CONCLUIDO, VAMOS REINICIAR AS ENTRADAS.')
                                else:
                                    quantidade = (float(quant) + float(lucro))
                                    print(f'SOROS NIVEL {sr} NA PROXIMA ENTRADA') 
                            else:
                                sr = 0
                                quantidade = float(entrada)
                        result = 'Win de primeira ✅' 
                        alerta(round(quant, 2),round(lucro, 2),round(lucros, 2),"WIN",direcao.upper(),padrao.upper(),ativo,data,hora)

                    
                    
                    

                       

                    if tele:
                        if conta == 'REAL' or email == 'ezequieleoss1986@gmail.com':
                            telegram(tempo2,hora2,ativo,direcao,gales,'final',result,1)
                        
                    
                    print(f'{Verde}{ativo} | {direcao.upper()} | VITORIA{Reset}')
                    print('Lucro:' + str(round(lucro, 2)))
                    time.sleep(5)
                    inicio()                        
                    if ONLINE:
                        lista_sinais_online()
                    else:
                        lista_sinais()
                    
            
            
                elif lucro < 0:
                    
                    #VTS = 0
                    percas += round(lucro, 2)
                    atual += round(lucro, 2)
                    ban = round(banca(), 2)
                    DER += 1
                    lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                    sr = 0
                    
                                        
                    alerta(round(quant, 2),round(lucro, 2),round(lucros, 2),"HIT",direcao.upper(),padrao.upper(),ativo,data,hora)
                    
                    
                    #inicio(ganhos, percas, atual)
                                        
                    print(f'{Vermelho}{ativo} | {direcao.upper()} | DERROTA{Reset}')
                    print('Lucro:' + str(round(lucro, 2)))
                    result = 'Derrota ❌' 

                    if tele:
                        if conta == 'REAL' or email == 'ezequieleoss1986@gmail.com':
                            telegram(tempo2,hora2,ativo,direcao,gales,'final',result,1)
                    if ativar_soros:
                        quantidade = float(entrada)
                    time.sleep(5)
                    inicio()
                    if ONLINE:
                        lista_sinais_online()
                    else:
                        lista_sinais()
                        
                        
                else:
                    print(f'{Azul}{ativo} | {direcao.upper()} | DOJI{Reset}')
                    print('Lucro:' + str(round(lucro, 2)))
                    result = 'Empate(DOJI) 🔁' 

                    if tele:
                        if conta == 'REAL' or email == 'ezequieleoss1986@gmail.com':
                            telegram(tempo2,hora2,ativo,direcao,gales,'final',result,1)

                    time.sleep(5)
                    if ONLINE:
                        lista_sinais_online()
                    else:
                        lista_sinais()
                                                           
def Verifica_status_D(id,ativo,quant,direcao,tempo,opcao,hora2,NV,MT,CT,tempo2):
    global BANCAINICIAL
    global ganhos
    global percas
    global atual
    global ban
    global VIT
    global DER
    global conta
    global email
    global sr
    global ONLINE
    global MULT
    global entrada
    global soros
    global quantidade
    global G
    global tele
    global ativar_soros
    global ativar_sorogale
    global Sorogale
    global sg

    #print(NV)
    if isinstance(id, int):
    #ui.listWidget_2.insertItem(0, f'{id} {ativo}')               
        while True:

            data = datas()
            hora = horario()
            padrao = 'LISTA'
            
            status,lucro = iq.check_win_digital_v2(id)
            if status:
                
                if lucro < 0 and NV > 0 and ativar_sorogale == False:
                    
                    NV -= 1
                    CT += 1
                    if CT == 1:
                        quant = entrada
                    percas += round(lucro, 2)
                    atual += round(lucro, 2)
                    ban = round(banca(), 2)
                    inicio()

                    NOVA_ENTRADA = float(quant)*MT
                    entrada2 = 'R$ {:,.2f}'.format(NOVA_ENTRADA)
                    print(f'{Amarelo}MARTINGALE: {Reset}'+str(CT)+ ' ' + ativo.upper() + ' ' +str(hora)+', ATIVO: '+str(ativo)+' - '+str(entrada2))
                        
                    status,id = iq.buy_digital_spot_v2(ativo, NOVA_ENTRADA, direcao, tempo)
                    Lm = Thread(target=Verifica_status_D, args=(id,ativo,NOVA_ENTRADA,direcao,tempo,opcao,hora,NV,MT,CT,tempo2,))
                    if MULT:
                        Lm = Thread(target=Verifica_status_D, args=(id,ativo,NOVA_ENTRADA,direcao,tempo,opcao,hora,NV,MT,CT,tempo2,))
                        Lm.daemon = True
                        Lm.start()
                        break
                    else:
                        Verifica_status_D(id,ativo,NOVA_ENTRADA,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                    
                    

                elif lucro > 0:
                    #VTS += 1
                    ganhos += round(lucro, 2)
                    atual += round(lucro, 2)
                    ban = round(banca(), 2)
                    VIT += 1
                    lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                    
                                                                             
                    
                    if CT == 1:
                        if ativar_soros:
                            sr = 0
                            quantidade = float(entrada)
                        result = 'Win no Gale 1 ✅🐔'    
                        alerta(round(quant, 2),round(lucro, 2),round(lucros, 2),"G1",direcao.upper(),padrao.upper(),ativo,data,hora)
                    elif CT == 2:
                        if ativar_soros:
                            sr = 0
                            quantidade = float(entrada)
                        result = 'Win no Gale 2 ✅🐔🐔' 
                        alerta(round(quant, 2),round(lucro, 2),round(lucros, 2),"G2",direcao.upper(),padrao.upper(),ativo,data,hora)
                    else:
                        resultado = 'win'
                        if ativar_soros:
                            sr += 1
                            if soros > 0:
                                if sr > soros:
                                    quantidade = float(entrada)
                                    sr = 0
                                    print(f'SOROS NIVEL {soros} CONCLUIDO, VAMOS REINICIAR AS ENTRADAS.')
                                else:
                                    quantidade = (float(quant) + float(lucro))
                                    print(f'SOROS NIVEL {sr} NA PROXIMA ENTRADA') 
                            else:
                                sr = 0
                                quantidade = float(entrada)
                        if ativar_sorogale:
                            soroGale(resultado, lucro, quant)
                        result = 'Win de primeira ✅' 
                        alerta(round(quant, 2),round(lucro, 2),round(lucros, 2),"WIN",direcao.upper(),padrao.upper(),ativo,data,hora)

                                   

                    if tele:
                        if conta == 'REAL' or email == 'ezequieleoss1986@gmail.com':
                            telegram(tempo2,hora2,ativo,direcao,gales,'final',result,1)
                        
                    
                    print(f'{Verde}{ativo} | {direcao.upper()} | VITORIA{Reset}')
                    print('Lucro:' + str(round(lucro, 2)))
                    time.sleep(5)
                    inicio()                        
                    if ONLINE:
                        lista_sinais_online()
                    else:
                        lista_sinais()
                    
            
                elif lucro < 0:
                    
                    #VTS = 0
                    percas += round(lucro, 2)
                    atual += round(lucro, 2)
                    ban = round(banca(), 2)
                    DER += 1
                    lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                    sr = 0
                    
                                        
                    alerta(round(quant, 2),round(lucro, 2),round(lucros, 2),"HIT",direcao.upper(),padrao.upper(),ativo,data,hora)
                    
                    
                    #inicio(ganhos, percas, atual)
                                        
                    print(f'{Vermelho}{ativo} | {direcao.upper()} | DERROTA{Reset}')
                    print('Lucro:' + str(round(lucro, 2)))
                    result = 'Derrota ❌' 

                    if tele:
                        if conta == 'REAL' or email == 'ezequieleoss1986@gmail.com':
                            telegram(tempo2,hora2,ativo,direcao,gales,'final',result,1)
                    if ativar_soros:
                        quantidade = float(entrada)
                    resultado = 'loss'
                    if ativar_sorogale:
                        soroGale(resultado, lucro, quant)
                    time.sleep(5)
                    inicio()
                    if ONLINE:
                        lista_sinais_online()
                    else:
                        lista_sinais()
                        
                        
                
                else:
                    sr = 0
                    print(f'{Azul}{ativo} | {direcao.upper()} | DOJI{Reset}')
                    print('Lucro:' + str(round(lucro, 2)))
                    result = 'Derrota(DOJI) ❌' 

                    if tele:
                        if conta == 'REAL' or email == 'ezequieleoss1986@gmail.com':
                            telegram(tempo2,hora2,ativo,direcao,gales,'final',result,1)

                    alerta(round(quant, 2),round(lucro, 2),round(lucros, 2),"DOJI",direcao.upper(),padrao.upper(),ativo,data,hora)
                    if ativar_soros:
                        quantidade = float(entrada)
                    resultado = 'loss'
                    if ativar_sorogale:
                        soroGale(resultado, lucro, quant)
                    time.sleep(5)
                    inicio()
                    if ONLINE:
                        lista_sinais_online()
                    else:
                        lista_sinais()

def confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par):
    global ganhos
    global percas
    global atual
    global conta
    global ban
    global quantidade
    global opcao
    global gales
    global TEND
    global DER
    global VIT
    global conta
    global email
    global ONLINE
    global MULT
    global tele

    os.system('cls' if os.name == 'nt' else 'clear')
    inicio()
    try:
        dir = direcao
                
        if TEND == False:
            dica = tendencia(par,tempo)
                        
            if opcao == 'binaria':
                ban = round(banca(), 2)
                entrada = 'R$ {:,.2f}'.format(quantidade)
                print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                if id:
                    if MULT:
                        Lm = Thread(target=Verifica_status, args=(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2,))
                        Lm.daemon = True
                        Lm.start()  
                    else:                  
                        Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                else:
                    print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))
                    if ONLINE:
                        lista_sinais_online()
                    else:
                        lista_sinais()
                    
            elif opcao == 'digital':
                ban = round(banca(), 2)
                entrada = 'R$ {:,.2f}'.format(quantidade)
                print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                status,id = iq.buy_digital_spot_v2(str(ativo),float(quantidade),str(direcao), int(tempo))
                if id:
                    if MULT:
                        Lm = Thread(target=Verifica_status_D, args=(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2,))
                        Lm.daemon = True
                        Lm.start()  
                    else:                  
                        Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                else:
                    print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))
                    if ONLINE:
                        lista_sinais_online()
                    else:
                        lista_sinais()
            
        else:
            dica = tendencia(par,tempo)
            
            if direcao.upper() == dica.upper():
                if opcao == 'binaria':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                    if id:
                        if MULT:
                            Lm = Thread(target=Verifica_status, args=(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2,))
                            Lm.daemon = True
                            Lm.start()  
                        else:                  
                            Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))
                        if ONLINE:
                            lista_sinais_online()
                        else:
                            lista_sinais()
                        
                elif opcao == 'digital':
                    ban = round(banca(), 2)
                    entrada = 'R$ {:,.2f}'.format(quantidade)
                    print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                    
                    status,id = iq.buy_digital_spot_v2(str(ativo),float(quantidade),str(direcao), int(tempo))
                    if id:
                        if MULT:
                            Lm = Thread(target=Verifica_status_D, args=(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2,))
                            Lm.daemon = True
                            Lm.start()  
                        else:                  
                            Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                    else:
                        print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))
                        if ONLINE:
                            lista_sinais_online()
                        else:
                            lista_sinais()

                    
                
            else:
                print('ENTRADA CONTRA TENDENCIA, IREI RECUSAR ESTA...')
                result = "Contra Tendencia"
                if tele:
                    if conta == 'REAL' or email == 'ezequieleoss1986@gmail.com':
                        telegram(tempo2,hora,ativo,direcao,gales,'contra',result,1)
                                
                if ONLINE:
                    lista_sinais_online()
                else:
                    lista_sinais()
    
    except:
        if ONLINE:
            lista_sinais_online()
        else:
            lista_sinais()

def checar_ativo(ativo, opcao,tempo2):
    tentar = ''
    ATIVOS = iq.get_all_open_time()
    if tempo2 == 'M30' or tempo2 == 'H1':
        if ATIVOS[opcao]['digital']["open"] == False:
            tentar = 'turbo'
            print('O ativo: '+str(ativo)+', esta fechado')
            return False, tentar
        else:
            return True, tentar
    else:
        if ATIVOS[opcao][ativo]["open"] == False:
            if opcao == 'digital':
                tentar = 'turbo'
                print('Digital: Fexado')
                if ATIVOS[tentar][ativo]["open"] == False:
                    
                    return False, tentar
                else:
                    print('Binaria: Aberto')
                    return True, tentar

            elif opcao == 'turdo':
                tentar = 'digital'
                print('Binaria: Fexado')
                if ATIVOS[tentar][ativo]["open"] == False:
                    
                    return False, tentar
                else:
                    print('Digital: Aberto')
                    return True, tentar
                
        else:
            tentar = opcao
            return True, tentar
   
def testadorlista():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'checando lista')
    arquivo = "sinais.txt"
    arquivo = open(arquivo, 'r').read()
    arquivo = arquivo.split('\n')

        
    
    win = 0
    loss = 0
    g1 = 0
    g2 = 0
    total = 0
    for dados in sorted(arquivo):
        
        if dados.strip() != '':
            dados = dados.split(',') # 2020-09-30 05:40,USDJPY,PUT,M1
            # [0] -> horario
            # [1] -> paridade
            # [2] -> direcao	
            # [3] -> tempo	

            if str(dados[3]) == 'M1':
                timeframe = 1
            if str(dados[3]) == 'M5':
                timeframe = 5
            if str(dados[3]) == 'M15':
                timeframe = 15
            if str(dados[3]) == 'M30': 
                timeframe = 30  
            if str(dados[3]) == 'H1': 
                timeframe = 60	
            
            horario = datetime.strptime(dados[0] + ':00', '%d-%m-%Y %H:%M:%S')
            horarios = datetime.strptime(dados[0] + ':00', '%d-%m-%Y %H:%M:%S')
            horario = datetime.timestamp(horario)
            horario1 = horarios + timedelta(minutes=timeframe)
            horarioG1 = datetime.timestamp(horario1)
            horario2 = horario1 + timedelta(minutes=timeframe)
            horarioG2 = datetime.timestamp(horario2)
            
            velas = iq.get_candles(dados[1].upper(), (timeframe * 60), 1, int(horario))
            #print(horario1, horario2)
            
            if int(velas[0]['from']) == int(horario):
                
                dir = 'call' if velas[0]['open'] < velas[0]['close'] else 'put' if velas[0]['open'] > velas[0]['close'] else 'doji'
                
                if dir == dados[2].lower():
                    print(Fore.YELLOW + str(dados[0])+' '+str(dados[1])+' '+str(dados[2])+ Fore.RESET+' '+' = '+' '+Fore.GREEN+'✅'+Fore.RESET)
                    win += 1
                else:
                    velas = iq.get_candles(dados[1].upper(), (timeframe * 60), 1, int(horarioG1))
                    #print(horario1, horario2)
                    
                    if int(velas[0]['from']) == int(horarioG1):
                        
                        dir = 'call' if velas[0]['open'] < velas[0]['close'] else 'put' if velas[0]['open'] > velas[0]['close'] else 'doji'
                        
                        if dir == dados[2].lower():
                            print(Fore.YELLOW + str(dados[0])+' '+str(dados[1])+' '+str(dados[2])+ Fore.RESET+' '+' = '+' '+Fore.GREEN+'✅🐔'+Fore.RESET)
                            
                            g1 += 1
                        else:
                            velas = iq.get_candles(dados[1].upper(), (timeframe * 60), 1, int(horarioG2))
                            #print(horario1, horario2)
                            
                            if int(velas[0]['from']) == int(horarioG2):
                                
                                dir = 'call' if velas[0]['open'] < velas[0]['close'] else 'put' if velas[0]['open'] > velas[0]['close'] else 'doji'
                                
                                if dir == dados[2].lower():
                                    print(Fore.YELLOW + str(dados[0])+' '+str(dados[1])+' '+str(dados[2])+ Fore.RESET+' '+' = '+' '+Fore.GREEN+'✅🐔🐔'+Fore.RESET)
                                    g2 += 1
                                else:
                                    print(Fore.YELLOW + str(dados[0])+' '+str(dados[1])+' '+str(dados[2])+ Fore.RESET+' '+' = '+' '+Fore.RED+'❌'+Fore.RESET)
                                    loss += 1
                            else:
                                print(Fore.YELLOW + str(dados[0])+' '+str(dados[1])+' '+str(dados[2])+ Fore.RESET+' '+' = '+' '+'Não foi possível capturar esta')
                    else:
                        print(Fore.YELLOW + str(dados[0])+' '+str(dados[1])+' '+str(dados[2])+ Fore.RESET+' '+' = '+' '+'Não foi possível capturar esta')
            else:
                print(Fore.YELLOW + str(dados[0])+' '+str(dados[1])+' '+str(dados[2])+ Fore.RESET+' '+' = '+' '+'Não foi possível capturar esta')


    

    print(' ')
    total = (win+g1+g2+loss)
    print('TOTAL: ' + str(total))
    print('SEM GALE - ACERTOU: ' + str(win) + ' / ERROU: ' + str(total-win))
    print('COM 1 GALE - ACERTOU: ' + str(g1+win) + ' / ERROU: ' + str(total-(g1+win)))
    print('COM 2 GALE - ACERTOU: ' + str(g2+win+g1) + ' / ERROU: ' + str(total-(g2+win+g1)))
    print(f'OK, {total} SINAIS VERIFICADOS')
    print('\n')

def soro(lucro):
    global quantidade
    global sr
    global ciclos
    global soros
    global entrada
    
    if soros == 0:
        quantidade = float(entrada)
        quantidade = float(quantidade)
        sr = 0
        inicio()
        return quantidade
    else:
        ciclos = True
        srt = soros
        srt = int(srt)
        
        if sr > srt:
            quantidade = float(entrada)
            quantidade = float(quantidade)
            sr = 0

            return quantidade

         

        else:
            print(f'SOROS NIVEL {sr} NA PROXIMA ENTRADA')  
            quantidade = (float(quantidade) + float(lucro))
            inicio()
            return quantidade

def soroGale(resultado, lucro, entrada):
    global BANCAINICIAL
    global gerencia
    global mao
    global preju
    global stop_loss
    global VTS
    global ENT
    global Nv
    global lucrosSG
    global quantidade
    global Sorogale
    global sg
    global atual
    

            
    if Sorogale > 0:
        entrada = float(ui.lineEdit_2.text())
        quantidade = float(entrada)
        sg = 0

    else:
        ciclos = True
        Nv = int(ui.comboBox_16.currentText())
        Banca_inicial = float(ui.label_14.text())
        Banca_inicial = float(round(Banca_inicial, 2))
        
        if resultado == 'win':
            
            if int(VTS) >= 2:
                ui.label_28.setText('BANCA RECUPERADA!')
                entrada = float(ui.lineEdit_2.text())
                preju = 0
                gerencia = 1
                mao = 1
                BANCAINICIAL = banca()
                VTS = 0
                lucrosSG = 0

                quantidade = float(ENT)
                print(quantidade)
                
            else:
                mao += 1
                entrada = float(entrada) + float(lucro)
                preju = 0

                quantidade = float(entrada)
                print(quantidade)
                
        else:
            
            if int(gerencia) == int(Nv) and mao == 2:
                ui.label_28.setText('REINICIANDO CICLOS DE SOROGALE')
                entrada = float(ui.lineEdit_2.text())
                preju = 0
                gerencia = 1
                mao = 1
                BANCAINICIAL = banca()
                VTS = 0
                lucrosSG = 0

                quantidade = float(entrada)
                print(quantidade)
            else:
                gerencia += 1
                mao = 1
                preju = (float(Banca_inicial) - float(banca()))
                entrada = float(preju) / 2
                VTS = 0
            
                quantidade = float(entrada)
                print(quantidade)

def listaDeEntradas():
    arquivo = open('sinais.txt', encoding='UTF-8')
    lista = arquivo.read()
    arquivo.close
    
    lista = lista.split('\n')
    
    for index,a in enumerate(lista):
        if a == '':
            del lista[index]
    
    return lista

def carregar_sinais():
    global minha_lista
    global chaveN

    data = {'chave': f'{chaveN}', 'acao': 'logar'}
    url = "http://mobtrader.atwebpages.com/lista/list.php"    
    resp = requests.post(url, data)
    retorno = resp.text
    lista = resp.text.replace('<br />', '\n')
    lista2 = []
    lista3 = []
    lista2.append(lista)
    for i in lista2:
        dados = i.split('\n')
        lista3.append(dados)
        for l in lista3[0]:
            minha_lista.append(l)
    
    for index,a in enumerate(minha_lista):
        if a == '':
            del minha_lista[index]
    
    return minha_lista

def lista_sinais_online():
    global iqo_api
    global DER
    global VIT
    global opcao
    global nomeN
    global conta
    global email
    global quantidade
    global gales
    global FL
    global DER
    global VIT
    global velasM
    global tele
    

    
    lista = carregar_sinais()
    
    NV = int(gales)
    MT = float(FL)
    CT = 0

    grana = 'R$ {:,.2f}'.format(atual)
    perdeu = DER
    ganhou = VIT

    tempo = 1
    
    #os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        to = 0
        data = datetime.now() .strftime('%Y-%m-%d %H:%M:%S')
        i = 0
        
        print(f'{Amarelo} Aguardando sinal... - ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        
        for sinal in lista:
            #print(sinal)
            to = to + 1
            dados = sinal.split(',')
            hora = (str(dados[0])+':00')
            h = hora.split(' ')
            hora2 = h[1]
            moeda = str(dados[1]).upper()
            direcao = str(dados[2]).lower()
            timeframe = str(dados[3]).upper()

            agora = datetime.now()
            data_atual = agora.strftime('%d/%m/%Y')

            hora_pay = datetime.now() + timedelta(seconds=35)
            hora_atual_pay = hora_pay.strftime('%H:%M:%S')

            hora_sinal_vip = datetime.now() + timedelta(minutes=50)
            hora_atual_sinal = hora_sinal_vip.strftime('%H:%M:%S')

            hora_sinal_free = datetime.now() + timedelta(minutes=30)
            hora_atual_sinal2 = hora_sinal_free.strftime('%H:%M:%S')
            
            now = datetime.now() + timedelta(seconds=2)
            hora_atual = now.strftime('%H:%M:%S')
            
            if timeframe == 'M1':
                    tempo = 1
            elif timeframe == 'M5':
                    tempo = 5
            elif timeframe == 'M15':
                    tempo = 15
            elif timeframe == 'M30':
                    tempo = 30
            elif timeframe == 'H1':
                    tempo = 60
            velasM = timeframe
            ativo = moeda
            re = 'Aguardando 🕐'
            #print(hora_atual, hora2)
            #print(hora2, hora_atual_pay)
            if hora_atual_sinal == hora2:
                if tele:
                    if conta == 'REAL' or email == 'ezequieleoss1986@gmail.com':
                        telegram(timeframe,hora2,ativo,direcao,gales,'inicial',re,1)
            if hora_atual_pay == hora2:
                '''
                if conta == 'REAL' or email == 'ezequieleoss1986@gmail.com':
                    telegram(timeframe,hora2,ativo,direcao,gales,'inicial',re,1)
                    telegram(timeframe,hora2,ativo,direcao,gales,'inicial',re,2)
                '''
                
                print(f'VERIFICANDO - {hora},{moeda.upper()},{direcao.upper()},{timeframe}')
                                
                st, op = checar_ativo(ativo,opcao,timeframe)
                if op == 'turbo':
                    op = 'binaria'
                
                if st:
                    opcao = op
                    print(f'OK, NA {opcao.upper()}')
                    
                    
                else:
                    print('MOEDA INDISPONIVEL NO MOMENTO, IREI PARA O PROXIMO SINAL')
                    lista_sinais()
                    break
            
            if hora_atual == hora2:
                print(f'SINAL ACEITO = {hora},{moeda} - {direcao.upper()}')
                momento = datetime.now()
                hm = datetime.now()
                h = hm.strftime('%H:%M')
                hora_atual = hm.strftime('%H:%M:%S')
                depois = datetime.now() + timedelta(minutes= 0)
                partiu = depois.strftime('%H:%M:%S')
                ativo = str(moeda)
                tempo2 = str(moeda)
                par = str(moeda)


                if MULT:
                    Lm = Thread(target=confirmadas, args=(direcao,ativo,tempo,timeframe,hora2,NV,MT,CT,par,))
                    Lm.daemon = True
                    Lm.start()  
                else:                  
                    confirmadas(direcao,ativo,tempo,timeframe,hora2,NV,MT,CT,par)
                
                #L = Thread(target=confirmadas, args=(direcao,ativo,tempo,timeframe,hora2,NV,MT,CT,par,))
                #L.daemon = True
                #L.start()
                        
        
        time.sleep(1)

def lista_sinais():
    global iqo_api
    global DER
    global VIT
    global opcao
    global nomeN
    global conta
    global email
    global quantidade
    global gales
    global FL
    global DER
    global VIT
    global velasM
    global tele
        
    
    lista = listaDeEntradas()
    
    
    NV = int(gales)
    MT = float(FL)
    CT = 0

    grana = 'R$ {:,.2f}'.format(atual)
    perdeu = DER
    ganhou = VIT

    tempo = 1
    
    #os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        to = 0
        data = datetime.now() .strftime('%Y-%m-%d %H:%M:%S')
        i = 0
        
        print(f'{Amarelo} Aguardando sinal... - ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        
        for sinal in lista:
            #print(sinal)
            to = to + 1
            dados = sinal.split(',')
            hora = (str(dados[0])+':00')
            h = hora.split(' ')
            hora2 = h[1]
            moeda = str(dados[1]).upper()
            direcao = str(dados[2]).lower()
            timeframe = str(dados[3]).upper()

            agora = datetime.now()
            data_atual = agora.strftime('%d/%m/%Y')

            hora_pay = datetime.now() + timedelta(seconds=25)
            hora_atual_pay = hora_pay.strftime('%H:%M:%S')

            hora_sinal_vip = datetime.now() + timedelta(minutes=50)
            hora_atual_sinal = hora_sinal_vip.strftime('%H:%M:%S')

            hora_sinal_free = datetime.now() + timedelta(minutes=30)
            hora_atual_sinal2 = hora_sinal_free.strftime('%H:%M:%S')
            
            now = datetime.now() + timedelta(seconds=2)
            hora_atual = now.strftime('%H:%M:%S')
            
            if timeframe == 'M1':
                    tempo = 1
            elif timeframe == 'M5':
                    tempo = 5
            elif timeframe == 'M15':
                    tempo = 15
            elif timeframe == 'M30':
                    tempo = 30
            elif timeframe == 'H1':
                    tempo = 60
            velasM = timeframe
            ativo = moeda
            re = 'Aguardando 🕐'
            #print(hora_atual, hora2)
            #print(hora2, hora_atual_pay)
            if hora_atual_sinal == hora2:
                if tele:
                    if conta == 'REAL' or email == 'ezequieleoss1986@gmail.com':
                        telegram(timeframe,hora2,ativo,direcao,gales,'inicial',re,1)
            if hora_atual_pay == hora2:
                '''
                if conta == 'REAL' or email == 'ezequieleoss1986@gmail.com':
                    telegram(timeframe,hora2,ativo,direcao,gales,'inicial',re,1)
                    telegram(timeframe,hora2,ativo,direcao,gales,'inicial',re,2)
                '''
                
                print(f'VERIFICANDO - {hora},{moeda.upper()},{direcao.upper()},{timeframe}')
                                
                st, op = checar_ativo(ativo,opcao,timeframe)
                if op == 'turbo':
                    op = 'binaria'
                
                if st:
                    opcao = op
                    print(f'OK, NA {opcao.upper()}')
                    
                    
                else:
                    print('MOEDA INDISPONIVEL NO MOMENTO, IREI PARA O PROXIMO SINAL')
                    lista_sinais()
                    break
            
            if hora_atual == hora2:
                print(f'SINAL ACEITO = {hora},{moeda} - {direcao.upper()}')
                momento = datetime.now()
                hm = datetime.now()
                h = hm.strftime('%H:%M')
                hora_atual = hm.strftime('%H:%M:%S')
                depois = datetime.now() + timedelta(minutes= 0)
                partiu = depois.strftime('%H:%M:%S')
                ativo = str(moeda)
                tempo2 = str(moeda)
                par = str(moeda)


                if MULT:
                    Lm = Thread(target=confirmadas, args=(direcao,ativo,tempo,timeframe,hora2,NV,MT,CT,par,))
                    Lm.daemon = True
                    Lm.start()  
                else:                  
                    confirmadas(direcao,ativo,tempo,timeframe,hora2,NV,MT,CT,par)
                
                #L = Thread(target=confirmadas, args=(direcao,ativo,tempo,timeframe,hora2,NV,MT,CT,par,))
                #L.daemon = True
                #L.start()
                        
        
        time.sleep(1)

def pegar_id(user_chave):
    global Pconta
    global sua_chave
    global user_id

    data = {'chave': f'{user_chave}', 'acao': 'logar'}
    url = "http://mobtrader.atwebpages.com/jogadores.php"    
    resp = requests.post(url, data)
    retorno = resp.text
    if retorno == '':
        print('CHAVE INCORRETA!')
        sys.exit()
    else:
        lista = resp.text.split(',')
        lista2 = []
        for i in lista:
            lista2.append(i)
        sua_chave = int(lista2[28])
        Pconta = lista2[3]
        user_id = int(lista2[28])
        
        return sua_chave

def confirma():
    global nomeN
    global nome
    global senha
    global email
    global conta
    global cliente
    global login
    global password
    global account_type
    global tp
    global chaveN

    

    os.system('cls' if os.name == 'nt' else 'clear')
    print('OK, BEM VINDO AO MOBTRADER LISTA, DIGITE SUA CHAVE\n')
    chaveN = str(input(': '))
    data = {'chave': f'{chaveN}', 'acao': 'logar'}
    url = "http://mobtrader.atwebpages.com/jogadores.php"    
    resp = requests.post(url, data)
    listaRetorno = []
    if resp.text != '0':
        lista = resp.text.split(',')
                        
        for i in lista:
            listaRetorno.append(i)
        nomeN = listaRetorno[0].replace(' ','')
        nome = nomeN
        senha = listaRetorno[1].replace(' ','')
        email = listaRetorno[2].replace(' ','')
        conta = listaRetorno[3].replace(' ','')
        cliente = str(listaRetorno[38])
        login = str(email)
        password = str(senha)
        account_type = str(conta)
        tp = account_type
        
        if cliente == 'TESTE':
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Desculpe, Somente para vip!!!')
            print('\n')
            print('ADQUIRA O BOT ENTRANDO EM CONTATO COM ZAP 11976159233')
            sys.exit()
               
        return True
        
    else:
        return resp.text


chave = str(confirma())
if chave == '0':
    os.system('cls' if os.name == 'nt' else 'clear')
    print('CHAVE NÃO ENCONTRADA!')
    sys.exit()
    
    
# Aqui começa a configuração da API, não alterar
#:===============================================================:#
os.system('cls' if os.name == 'nt' else 'clear')
iq = IQ_Option(login, password)
iqo_api = iq
if not verificar_se_fez_a_conexao(iq, account_type):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('OPA!, VERIFIQUE O APLICATICO, EMAIL OU SENHA ESTA INCORRETA.')
    sys.exit(0)
conta = account_type
currency_account = iq.get_currency()
account_balance = iq.get_balance()
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M'
os.system('cls' if os.name == 'nt' else 'clear')
x = perfil()
nome = str(x['name'])
saldo = (f"{'Conta de treino saldo' if account_type == 'PRACTICE'  else 'Saldo'}: {Amarelo}{format_currency_value(currency_account, account_balance)}{Reset}")
print(saldo)
BANCAINICIAL = float(round(banca(), 2))
time.sleep(3)

os.system('cls' if os.name == 'nt' else 'clear')
print('QUAL O TIPO DE OPÇAO?\n\n1 = DIGITAL\n2 = BINARIA\n ')
Nopcao = int(input('Digite um numero: '))
if Nopcao == 1:
    opcao = 'digital'
elif Nopcao == 2:
    opcao = 'binaria'
os.system('cls' if os.name == 'nt' else 'clear')
print('DESEJA HABILITAR MULTIPLAS ENTRADAS?\n\n1 = SIM\n2 = NÃO\n ')
Nmult = int(input('Digite um numero: '))
if Nmult == 1:
    MULT = True
elif Nmult == 2:
    MULT = False
os.system('cls' if os.name == 'nt' else 'clear')
print('DESEJA HABILITAR TENDÊNCIA?\n\n1 = SIM\n2 = NÃO\n ')
Ntend = int(input('Digite um numero: '))
if Ntend == 1:
    TEND = True
elif Ntend == 2:
    TEND = False
os.system('cls' if os.name == 'nt' else 'clear')
print('QUAL O TIPO DE OPERAÇÃO?\n\n1 = LISTA CADASTRADA\n2 = LISTA LOCAL\n ')
modo_catalogar = int(input('Digite um numero: '))
if modo_catalogar == 1:
    ONLINE = True
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\nQUAL VALOR DE ENTRADA?: ', end='')
    quantidade = int(input())
    print('\nQUAL INICIAL?: ', end='')
    entrada = int(input())
    print('\nQUANTOS MARTINGALES?: ', end='')
    gales = int(input())
    print('\nQUANTOS SOROS?: ', end='')
    soros = int(input())
    if soros > 0:
        ativar_soros = True
    else:
        ativar_soros = False
    print('\nQUANTOS SOROSGALE?: ', end='')
    Sorogale = int(input())
    if Sorogale > 0:
        ativar_sorogale = True
    else:
        ativar_sorogale = False
    
    inicio()
    lista_sinais_online()
elif modo_catalogar == 2:
    ONLINE = False
    os.system('cls' if os.name == 'nt' else 'clear')
    print('ESCOLHA:\n\n1 = TESTAR ULTIMA LISTA CATALOGADA\n2 = CATALOGAR NOVA LISTA\n3 = INICIAR ULTIMA LISTA CATALOGADA\n ')
    modo = int(input('Digite um numero: '))
    if modo == 1:
        testadorlista()
        print('\nESCOLHA:\n\n1 = INICIAR\n2 = TESTAR\n3 = SAIR\n')
        modo2 = int(input('Digite um numero: '))
    elif modo == 2:
        catalogaragora(iq) 
        print('\nESCOLHA:\n\n1 = INICIAR\n2 = TESTAR\n3 = SAIR\n')
        modo2 = int(input('Digite um numero: '))
        if modo2 == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('\nQUAL VALOR DE ENTRADA?: ', end='')
            quantidade = int(input())
            print('\nQUAL VALOR INICIAL?: ', end='')
            entrada = int(input())
            print('\nQUANTOS MARTINGALES?: ', end='')
            gales = int(input())
            print('\nQUANTOS SOROS?: ', end='')
            soros = int(input())
            if soros > 0:
                ativar_soros = True
            else:
                ativar_soros = False
            print('\nQUANTOS SOROSGALE?: ', end='')
            Sorogale = int(input())
            if Sorogale > 0:
                ativar_sorogale = True
            else:
                ativar_sorogale = False
            inicio()
            lista_sinais()
        elif modo2 == 2:
            testadorlista()
        elif modo2 == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('!! MOBTRADER LISTAS DE SINAIS !!')
            sys.exit()
    elif modo == 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\nQUAL VALOR DE ENTRADA?: ', end='')
        quantidade = int(input())
        print('\nQUAL VALOR INICIAL?: ', end='')
        entrada = int(input())
        print('\nQUANTOS MARTINGALES?: ', end='')
        gales = int(input())
        print('\nQUANTOS SOROS?: ', end='')
        soros = int(input())
        if soros > 0:
            ativar_soros = True
        else:
            ativar_soros = False
        print('\nQUANTOS SOROSGALE?: ', end='')
        Sorogale = int(input())
        if Sorogale > 0:
            ativar_sorogale = True
        else:
            ativar_sorogale = False
        inicio()
        lista_sinais()
elif modo_catalogar == 000:
    ONLINE = False
    Tele = True
    os.system('cls' if os.name == 'nt' else 'clear')
    print('ESCOLHA:\n\n1 = TESTAR ULTIMA LISTA CATALOGADA\n2 = CATALOGAR NOVA LISTA\n3 = INICIAR ULTIMA LISTA CATALOGADA\n ')
    modo = int(input('Digite um numero: '))
    if modo == 1:
        testadorlista()
        print('\nESCOLHA:\n\n1 = INICIAR\n2 = TESTAR\n3 = SAIR\n')
        modo2 = int(input('Digite um numero: '))
    elif modo == 2:
        catalogaragora(iq) 
        print('\nESCOLHA:\n\n1 = INICIAR\n2 = TESTAR\n3 = SAIR\n')
        modo2 = int(input('Digite um numero: '))
        if modo2 == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('\nQUAL VALOR DE ENTRADA?: ', end='')
            quantidade = int(input())
            print('\nQUAL VALOR INICIAL?: ', end='')
            entrada = int(input())
            print('\nQUANTOS MARTINGALES?: ', end='')
            gales = int(input())
            print('\nQUANTOS SOROS?: ', end='')
            soros = int(input())
            if soros > 0:
                ativar_soros = True
            else:
                ativar_soros = False
            print('\nQUANTOS SOROSGALE?: ', end='')
            Sorogale = int(input())
            if Sorogale > 0:
                ativar_sorogale = True
                ativar_soros = False
            else:
                ativar_sorogale = False
            inicio()
            lista_sinais()
        elif modo2 == 2:
            testadorlista()
        elif modo2 == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('!! MOBTRADER LISTAS DE SINAIS !!')
            sys.exit()
    elif modo == 3:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\nQUAL VALOR DE ENTRADA?: ', end='')
        quantidade = int(input())
        print('\nQUAL VALOR INICIAL?: ', end='')
        entrada = int(input())
        print('\nQUANTOS MARTINGALES?: ', end='')
        gales = int(input())
        print('\nQUANTOS SOROS?: ', end='')
        soros = int(input())
        if soros > 0:
            ativar_soros = True
        else:
            ativar_soros = False
        if Sorogale > 0:
            ativar_sorogale = True
        else:
            ativar_sorogale = False
        inicio()
        lista_sinais()
