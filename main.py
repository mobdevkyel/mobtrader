from iqoptionapi.stable_api import IQ_Option
from iqoptionapi.constants import ACTIVES
import iqoptionapi.country_id as Pais
from busca import *
from variaveis import *
from melhor_payout_par import *
import time, json, logging, configparser, os, csv, sys, io
from threading import Thread
from datetime import datetime, date, timedelta
from urllib.request import urlretrieve

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
    global hora_inicial
    global hora_X
    global espera
    global ATU
    global velasM
    global gales
    global MHI
    global MHI2
    global MHI3
    global MHI2_Maioria
    global MHI3_Maioria
    global Milhao_Minoria
    global Milhao_Maioria
    global Padrao_Impar
    global Torres_Gemeas
    global Tres_Mosqueteiros
    global C3
    global Melhor_de_3
    global Padrao_23
    global MHI_Maioria
    global autonomo
    global gerenciada
    global martingale
    global FL
    global catalogador_gale
    global catalogador_tempo
    global catalogador_moeda
    global paym
    global acerm
    global inverter
    global erros
    global VIT
    global DER
    global catalogo
    
    

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
    ATU = ''
    
    status = verificacao()
    if status != '':
        print(staus)
        sys.exit()

    else:
              
        if autonomo == 'nao':
            hora_X = '00:00:00'
        
        
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            if velasM == 'M1':
                minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
                entrar = True if (minutos >= 4.25 and minutos <= 5) or minutos >= 9.25 else False
                grana = 'R$ {:,.2f}'.format(atual)
                perdeu = DER
                ganhou = VIT
                

                print(f'{Verde} LOSS: {perdeu} / WIN: {ganhou} = Lucros: {grana} {Reset} - ' + datetime.now().strftime('%H:%M:%S'), end='\r')

                if entrar:
                    paridade, padrao, porcentagem, WIN, G1, G2, HIT, win, g1, g2, hit, ATU = catalogar(str(velasM),int(gales),int(erros),int(catalogo))
                    print(paridade)
                    if paridade == '':
                        print(f'NEHUM PADÃO TEM MENOS DE {erros} DERROTAS NO MOMENTO')
                        time.sleep(10)
                        buscar()
                        break 
                    
                    else:
                                                    
                        if int(porcentagem) < int(acerm):
                            print(f'PADRÃO LOCALIZADO {padrao} - {paridade} = {porcentagem}\nFAREI NOVA BUSCA, PORCENTAGEM MINIMA DE {acerm}%')
                            time.sleep(10)
                            buscar()
                            break

                        os.system('cls' if os.name == 'nt' else 'clear')
                        if tp == 'TOURNAMENT':
                            opcao = "binaria"
                            inicio(ganhos, percas, atual)
                        else:
                            print('Buscando melhor Payout')
                            opcao,percent,sta = most_profit_mode(iqo_api, paridade, 1, min_payout=(int(paym) / 100))
                            
                            time.sleep(5)
                            if opcao == 'turbo':
                                opcao = 'binaria'
                            if opcao == 'closed' or opcao == 'error' or opcao == 'payout':
                                print('Moeda fora de operação neste momento')
                                time.sleep(5)
                                buscar()
                                break
                            if percent < (int(paym) / 100):
                                print('payout = ',percent)
                                print(f'Payout Abaixo do padrão que é {paym}%, vamos esperar subir mais para entrar.')
                                time.sleep(5)
                                buscar()
                                break
                            else:
                                inicio(ganhos, percas, atual)
                                mta = stop(ganhos,percas)
                                
                                if mta:
                                    print('\n!!! MOBTRADER BOT, RESPEITE SEU GERENCIAMENTO!!!')
                                    sys.exit()
                                    
                                else:   
                                    if padrao == 'MHI':
                                        c3 = False
                                        MHI0()
                                        break
                                    
                                    elif padrao == 'MHI2':
                                        c3 = False
                                        MHI_2()
                                        break
                                        
                                    elif padrao == 'MHI3':
                                        c3 = False
                                        MHI_3()
                                        break
                                        
                                    elif padrao == 'MHI2 Maioria':
                                        c3 = False
                                        MHI2_MAIORIA()
                                        break
                                        
                                    elif padrao == 'MHI3 Maioria':
                                        c3 = False
                                        MHI3_MAIORIA()
                                        break
                                        
                                    elif padrao == 'Milhão Minoria':
                                        c3 = False
                                        MILHAO_MINORIA()
                                        break
                                        
                                    elif padrao == 'Milhão Maioria':
                                        c3 = False
                                        MILHAO_MAIORIA()
                                        break
                                        
                                    elif padrao == 'Padrão Impar':
                                        c3 = False
                                        PADRAO_IMPAR()
                                        break
                                        
                                    elif padrao == 'Torres Gêmeas':
                                        c3 = False
                                        TORRES_GEMEAS()
                                        break
                                        
                                    elif padrao == 'Três Mosqueteiros':
                                        c3 = False
                                        TRES_MOSQUETEIROS()
                                        break
                                                                       
                                    elif padrao == 'Melhor de 3':
                                        c3 = False
                                        MELHOR_DE_3()
                                        break
                                        
                                    elif padrao == 'Padrão 23':
                                        c3 = False
                                        PADRAO_23()
                                        break
                                        
                                    elif padrao == 'MHI Maioria':
                                        c3 = False
                                        MHI_MAIORIA()    
                                        break
                                    elif padrao == 'Five Flip':
                                        c3 = False
                                        FIVE_FLIP()    
                                        break  
                                    elif padrao == 'Três Vizinhos':
                                        c3 = False
                                        TRES_VIZINHOS()    
                                        break 
                                    else:
                                        print(f'PADRÃO DESABILITADO, BUSCANDO PROXIMO...')
                                        time.sleep(30)
                                        buscar()
                                        break
            
            elif velasM == 'M5':
                minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
                entrar = True if (minutos >= 4.25 and minutos <= 5) or minutos >= 9.25 else False
                grana = 'R$ {:,.2f}'.format(atual)
                perdeu = DER
                ganhou = VIT
                

                print(f'{Verde} LOSS: {perdeu} / WIN: {ganhou} = Lucros: {grana} {Reset} - ' + datetime.now().strftime('%H:%M:%S'), end='\r')

                if entrar:
                    paridade, padrao, porcentagem, WIN, G1, G2, HIT, win, g1, g2, hit, ATU = catalogar(str(velasM),int(gales),int(erros),int(catalogo))
                    print(paridade)
                    if paridade == '':
                        print(f'NEHUM PADÃO TEM MENOS DE {erros} DERROTAS NO MOMENTO')
                        time.sleep(10)
                        buscar()
                        break 
                    
                    else:
                                                    
                        if int(porcentagem) < int(acerm):
                            print(f'PADRÃO LOCALIZADO {padrao} - {paridade} = {porcentagem}\nFAREI NOVA BUSCA, PORCENTAGEM MINIMA DE {acerm}%')
                            time.sleep(10)
                            buscar()
                            break

                        os.system('cls' if os.name == 'nt' else 'clear')
                        if tp == 'TOURNAMENT':
                            opcao = "binaria"
                            inicio(ganhos, percas, atual)
                        else:
                            print('Buscando melhor Payout')
                            opcao,percent,sta = most_profit_mode(iqo_api, paridade, 5, min_payout=(int(paym) / 100))
                            
                            time.sleep(5)
                            if opcao == 'turbo':
                                opcao = 'binaria'
                            if opcao == 'closed' or opcao == 'error' or opcao == 'payout':
                                print('Moeda fora de operação neste momento')
                                time.sleep(5)
                                buscar()
                                break
                            if percent < (int(paym) / 100):
                                print('payout = ',percent)
                                print(f'Payout Abaixo do padrão que é {paym}%, vamos esperar subir mais para entrar.')
                                time.sleep(5)
                                buscar()
                                break
                            else:
                                inicio(ganhos, percas, atual)
                                mta = stop(ganhos,percas)
                                
                                if mta:
                                    print('\n!!! MOBTRADER BOT, RESPEITE SEU GERENCIAMENTO!!!')
                                    sys.exit()
                                    
                                else:   
                                    if padrao == 'MHI':
                                        c3 = False
                                        MHI0()
                                        break
                                    
                                    elif padrao == 'MHI2':
                                        c3 = False
                                        MHI_2()
                                        break
                                        
                                    elif padrao == 'MHI3':
                                        c3 = False
                                        MHI_3()
                                        break
                                        
                                    elif padrao == 'MHI2 Maioria':
                                        c3 = False
                                        MHI2_MAIORIA()
                                        break
                                        
                                    elif padrao == 'MHI3 Maioria':
                                        c3 = False
                                        MHI3_MAIORIA()
                                        break
                                        
                                    elif padrao == 'Milhão Minoria':
                                        c3 = False
                                        MILHAO_MINORIA()
                                        break
                                        
                                    elif padrao == 'Milhão Maioria':
                                        c3 = False
                                        MILHAO_MAIORIA()
                                        break
                                                                         
                                    elif padrao == 'Torres Gêmeas':
                                        c3 = False
                                        TORRES_GEMEAS()
                                        break
                                        
                                    elif padrao == 'Três Mosqueteiros':
                                        c3 = False
                                        TRES_MOSQUETEIROS()
                                        break
                                       
                                    elif padrao == 'MHI Maioria':
                                        c3 = False
                                        MHI_MAIORIA()    
                                        break
                                    elif padrao == 'Five Flip':
                                        c3 = False
                                        FIVE_FLIP()    
                                        break  
                                    elif padrao == 'Três Vizinhos':
                                        c3 = False
                                        TRES_VIZINHOS()    
                                        break
                                    elif padrao == 'MHI de Meio Ciclo':
                                        c3 = False
                                        MHI_MEIO()    
                                        break
                                    else:
                                        print(f'PADRÃO DESABILITADO, BUSCANDO PROXIMO...')
                                        time.sleep(30)
                                        buscar()
                                        break
                                    '''
                                    elif padrao == 'Padrão Impar':
                                        c3 = False
                                        PADRAO_IMPAR()
                                        break
                                    
                                    elif padrao == 'Melhor de 3':
                                        c3 = False
                                        MELHOR_DE_3()
                                        break
                                        
                                    elif padrao == 'Padrão 23':
                                        c3 = False
                                        PADRAO_23()
                                        break
                                    '''

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

def tendencia(par):
    #par = 'AUDCAD'
    timeframe = 5

    velas = iq.get_candles(par, (int(timeframe) * 60), 25,  time.time())

    ultimo = round(velas[0]['close'], 4)
    primeiro = round(velas[-1]['close'], 4)

    diferenca = abs( round( ( (ultimo - primeiro) / primeiro ) * 100, 3) )
    tendencia = "CALL" if ultimo < primeiro and diferenca > 0.01 else "PUT" if ultimo > primeiro and diferenca > 0.01 else False
    
    return tendencia

def stop(ganhos,percas):
    global stop_loss
    global stop_win
    global atual
    global STP
    global hora_inicial
    global hora_X
    global espera
    global AT
    global atual
    global espera
    
            
    if atual <= float('-' + str(abs(stop_loss))):
        
        inicio(ganhos, percas, atual)
        print('STOP LOSS ATINGIDO!!!')
        
        print('\nVAMOS PARAR POR HOJE NÉ!!!!')
        return True
        sys.exit()
        

        
    if atual >= float(abs(stop_win)):
        
        inicio(ganhos, percas, atual)
        print('STOP WIN ATINGIDO!!!')
        
        print('VAMOS POR ESSA NA CONTA E VOLTAR SO AMANHÃ NÉ!!!!')
        return True
        sys.exit()

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
    global hora_X
    global ATU
    global velasM
    global gerenciada
    global quantidade
    global martingale
    global ENT
    global gales
    global G
    global inverter
    global saldo
    global catalogo
    global cat
    global parfixo
    global padraoTrabalho
    global trabalho
    
    if gerenciada:
        modo = 'SOROSGALE'
        quantidade = ENT
    else:
        modo = 'MARTINGALE'
    if gales == 0:
        G = 'Mão fixa'
    if gales == 1:
        G = '1 Gale'
    if gales == 2:
        G = '2 Gale'
    
    if catalogo == 0:
        cat = 'Catalogação automatica'
    elif catalogo == 1:
        cat = 'Catalogação de mão fixa'
    elif catalogo == 2:
        cat = 'Catalogação de 1 gale'
    elif catalogo == 3:
        cat = 'Catalogação de 2 gale'
    
    
    

    if inverter:
        inver = 'ATIVO'   
    else:
        inver = 'DESATIVADO' 
    
    if trabalho == 'lista':
        padrao = 'LISTA'
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'{Amarelo}______  ___       ______  ________                _________{Reset}')              
        print(f'{Amarelo}___   |/  /______ ___  /_ ___  __/______________ _______  /_____ ________{Reset}')
        print(f'{Amarelo}__  /|_/ / _  __ \__  __ \__  /   __  ___/_  __ `/_  __  / _  _ \__  ___/{Reset}')
        print(f'{Amarelo}_  /  / /  / /_/ /_  /_/ /_  /    _  /    / /_/ / / /_/ /  /  __/_  /{Reset}')    
        print(f'{Amarelo}/_/  /_/   \____/ /_.___/ /_/     /_/     \__,_/  \__,_/   \___/ /_/ {Reset}\n')  
        print(f'{Azul}FULL MHI V 1.0{Reset} - Contato: +55 (11) 9 7615-9233\n')    
        print(f'Ganhos: {Verde}{round(ganhos, 2)}{Reset} || Percas: {Vermelho}{round(percas, 2)}{Reset} || Locros: {Amarelo}{round(atual, 2)}{Reset}\nConta: {Azul}{conta}{Reset}')
        print(f'VITORIAS: {Verde}{VIT}{Reset} // DERROTAS: {Vermelho}{DER}{Reset}\nSUA BANCA INICIAL: {Azul}{saldo}{Reset}\nSUA BANCA ATUAL: {Amarelo}{round(banca(), 2)}{Reset}')
        print(f'MOEDA: {Verde}{moeda}{Reset} || PADRÃO: {Verde}{padrao}{Reset}\nVELAS DE: {Amarelo}{velasM}{Reset} || ENTRADA: {Verde}{round(quantidade, 2)}{Reset}')#VITORIAS DE PRIMEIRA: {Verde}{WIN} - {win}% DE VITORIAS{Reset}\nVITORIAS NO GALE 1: {Verde}{G1} - {g1}% DE VITORIAS{Reset}\nVITORIAS NO GALE 2: {Verde}{G2} - {g2}% DE VITORIAS{Reset}\nHIT: {Vermelho}{HIT} - {hit}% DE DERROTAS{Reset}')
        print(f'GALES: {Azul}{gales}{Reset}')
        print(f'*********************************************************************************************')
    elif trabalho == 'fixo':
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'{Amarelo}______  ___       ______  ________                _________{Reset}')              
        print(f'{Amarelo}___   |/  /______ ___  /_ ___  __/______________ _______  /_____ ________{Reset}')
        print(f'{Amarelo}__  /|_/ / _  __ \__  __ \__  /   __  ___/_  __ `/_  __  / _  _ \__  ___/{Reset}')
        print(f'{Amarelo}_  /  / /  / /_/ /_  /_/ /_  /    _  /    / /_/ / / /_/ /  /  __/_  /{Reset}')    
        print(f'{Amarelo}/_/  /_/   \____/ /_.___/ /_/     /_/     \__,_/  \__,_/   \___/ /_/ {Reset}\n')  
        print(f'{Azul}FULL MHI V 1.0{Reset} - Contato: +55 (11) 9 7615-9233\n')    
        print(f'Ganhos: {Verde}{round(ganhos, 2)}{Reset} || Percas: {Vermelho}{round(percas, 2)}{Reset} || Locros: {Amarelo}{round(atual, 2)}{Reset}\nConta: {Azul}{conta}{Reset} || Opção: {Amarelo}{opcao.upper()}{Reset}')
        print(f'VITORIAS: {Verde}{VIT}{Reset} // DERROTAS: {Vermelho}{DER}{Reset}\nSUA BANCA INICIAL: {Azul}{saldo}{Reset}\nSUA BANCA ATUAL: {Amarelo}{round(banca(), 2)}{Reset}')
        print(f'MOEDA: {Verde}{parfixo}{Reset} || PADRÃO: {Verde}{padraoTrabalho}{Reset}\nVELAS DE: {Amarelo}{velasM}{Reset} || ENTRADA: {Verde}{round(quantidade, 2)}{Reset}')#VITORIAS DE PRIMEIRA: {Verde}{WIN} - {win}% DE VITORIAS{Reset}\nVITORIAS NO GALE 1: {Verde}{G1} - {g1}% DE VITORIAS{Reset}\nVITORIAS NO GALE 2: {Verde}{G2} - {g2}% DE VITORIAS{Reset}\nHIT: {Vermelho}{HIT} - {hit}% DE DERROTAS{Reset}')
        print(f'GALES: {Azul}{gales}{Reset} || INVERSÃO: {Azul}{inver}{Reset}')
        print(f'*********************************************************************************************')
    else:        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'{Amarelo}______  ___       ______  ________                _________{Reset}')              
        print(f'{Amarelo}___   |/  /______ ___  /_ ___  __/______________ _______  /_____ ________{Reset}')
        print(f'{Amarelo}__  /|_/ / _  __ \__  __ \__  /   __  ___/_  __ `/_  __  / _  _ \__  ___/{Reset}')
        print(f'{Amarelo}_  /  / /  / /_/ /_  /_/ /_  /    _  /    / /_/ / / /_/ /  /  __/_  /{Reset}')    
        print(f'{Amarelo}/_/  /_/   \____/ /_.___/ /_/     /_/     \__,_/  \__,_/   \___/ /_/ {Reset}\n')  
        print(f'{Azul}FULL MHI V 1.0{Reset} - Contato: +55 (11) 9 7615-9233\n')    
        print(f'Ganhos: {Verde}{round(ganhos, 2)}{Reset} || Percas: {Vermelho}{round(percas, 2)}{Reset} || Locros: {Amarelo}{round(atual, 2)}{Reset}\nConta: {Azul}{conta}{Reset} || Opção: {Amarelo}{opcao.upper()}{Reset}')
        print(f'VITORIAS: {Verde}{VIT}{Reset} // DERROTAS: {Vermelho}{DER}{Reset}\nSUA BANCA INICIAL: {Azul}{saldo}{Reset}\nSUA BANCA ATUAL: {Amarelo}{round(banca(), 2)}{Reset}')
        print(f'MOEDA: {Verde}{paridade}{Reset} || PADRÃO: {Verde}{padrao}  {porcentagem}%{Reset}\nVELAS DE: {Amarelo}{velasM}{Reset} || ENTRADA: {Verde}{round(quantidade, 2)}{Reset}')#VITORIAS DE PRIMEIRA: {Verde}{WIN} - {win}% DE VITORIAS{Reset}\nVITORIAS NO GALE 1: {Verde}{G1} - {g1}% DE VITORIAS{Reset}\nVITORIAS NO GALE 2: {Verde}{G2} - {g2}% DE VITORIAS{Reset}\nHIT: {Vermelho}{HIT} - {hit}% DE DERROTAS{Reset}')
        print(f'GALES: {Azul}{gales}{Reset} || INVERSÃO: {Azul}{inver}{Reset}')
        print(f'Catalogação: {Azul}{cat}{Reset}')
        print(f'*********************************************************************************************')

def carregarM5(nomeArquivo):
	arquivo = open(str(nomeArquivo), encoding='UTF-8')
	lista = arquivo.read()
	arquivo.close
	
	lista = lista.split('\n')
	
	for index,a in enumerate(lista):
		if a == '':
			del lista[index]
	
	return lista

def alerta(entrada,saida,lucro,resultado,direcao,extrategia,moeda,data,horario):
    global chaveN
    global nome
    global conta
        
    data = {'chave': f'{chaveN}','nome': f'{nome}','moeda': f'{moeda}','direcao': f'{direcao}','extrategia': f'{extrategia}','data': f'{data}','entrada': f'{entrada}','saida': f'{saida}','lucro': f'{lucro}','resultado': f'{resultado}','conta': f'{conta}','hora': f'{horario}', 'acao': 'Cadastrar'}
    url = "http://mobtrader.myartsonline.com/alert/jogadores.php"    
    resp = requests.post(url, data)

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
    global gerenciada
    global resu
    global luc
    global quant
    global ENT
    global sorosmao
    global pulos
    global trabalho
    global moeda
    global timeframe
    global parfixo
    global padraoTrabalho
    

    if trabalho == 'fixo':
        ativo = parfixo
        padrao = padraoTrabalho 



    
    #print(NV)   
    if isinstance(id, int):
                        
        while True:

            data = datas()
            hora = horario()   


            status,lucro = iq.check_win_v4(id)
            if status:
                
                if lucro < 0 and NV > 0:
                    NV -= 1
                    CT += 1
                    percas += round(lucro, 2)
                    atual += round(lucro, 2)
                    ban = round(banca(), 2)
                    inicio(ganhos, percas, atual)

                    NOVA_ENTRADA = float(quantidade)*MT
                    entrada = 'R$ {:,.2f}'.format(NOVA_ENTRADA)
                    
                    print(f'{Amarelo}MARTINGALE: {Reset}'+str(CT)+ ' ' + padrao.upper() + ' ' +str(hora)+', ATIVO: '+str(ativo)+' - '+str(entrada))
                        
                    status,id = iq.buy(NOVA_ENTRADA, ativo, direcao, tempo)

                    if trabalho == 'lista':
                        Verifica_status(id,ativo,NOVA_ENTRADA,direcao,tempo,opcao,hora,NV,MT,CT,timeframe)
                    else:
                        Verifica_status(id,ativo,NOVA_ENTRADA,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                    
                    

                elif lucro > 0:
                    VTS += 1
                    ganhos += round(lucro, 2)
                    atual += round(lucro, 2)
                    ban = round(banca(), 2)
                    VIT += 1
                    lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                    
                    
                    if CT == 1:
                        alerta(round(quantidade, 2),round(lucro, 2),round(lucros, 2),"G1",direcao.upper(),padrao.upper(),ativo,data,hora)
                    elif CT == 2:
                        alerta(round(quantidade, 2),round(lucro, 2),round(lucros, 2),"G2",direcao.upper(),padrao.upper(),ativo,data,hora)
                    else:
                        alerta(round(quantidade, 2),round(lucro, 2),round(lucros, 2),"WIN",direcao.upper(),padrao.upper(),ativo,data,hora)

                    
                    inicio(ganhos, percas, atual)
                    
                    print(f'{Verde}{ativo} | {direcao.upper()} | VITORIA{Reset}')
                    print('Lucro:' + str(round(lucro, 2)))
                    
                    time.sleep(5)
                    mta = stop(ganhos,percas)
                    if mta:
                        print('\n!!! MOBTRADER BOT, RESPEITE SEU GERENCIAMENTO!!!')
                        sys.exit()
                        
                    if trabalho == 'lista':  
                        lista_sinais()
                    elif trabalho == 'fixo':
                        entradas_fixas(parfixo, padraoTrabalho)
                    else:
                        buscar()
                    
            
            
                elif lucro < 0:
                    
                    VTS = 0
                    percas += round(lucro, 2)
                    atual += round(lucro, 2)
                    ban = round(banca(), 2)
                    DER += 1
                    lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                    
                                        
                    alerta(round(quantidade, 2),round(lucro, 2),round(lucros, 2),"HIT",direcao.upper(),padrao.upper(),ativo,data,hora)
                    
                    
                    inicio(ganhos, percas, atual)
                                        
                    print(f'{Vermelho}{ativo} | {direcao.upper()} | DERROTA{Reset}')
                    print('Lucro:' + str(round(lucro, 2)))
                    
                    time.sleep(5)
                    mta = stop(ganhos,percas)
                    if mta:
                        print('\n!!! MOBTRADER BOT, RESPEITE SEU GERENCIAMENTO!!!')
                        sys.exit()
                    if trabalho == 'lista':  
                        lista_sinais()
                    elif trabalho == 'fixo':
                        entradas_fixas(parfixo, padraoTrabalho)
                    else:
                        buscar()
                        
                        
                else:
                    print(f'{Azul}{ativo} | {direcao.upper()} | DOJI{Reset}')
                    print('Lucro:' + str(round(lucro, 2)))
                    
                    time.sleep(5)
                    mta = stop(ganhos,percas)
                    if mta:
                        print('\n!!! MOBTRADER BOT, RESPEITE SEU GERENCIAMENTO!!!')
                        sys.exit()                    
                    alerta(round(quantidade, 2),round(lucro, 2),round(lucros, 2),"DOJI",direcao.upper(),padrao.upper(),ativo,data,hora)
                    if trabalho == 'lista':  
                        lista_sinais()
                    elif trabalho == 'fixo':
                        entradas_fixas(parfixo, padraoTrabalho)
                    else:
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
    global conta
    global resu
    global luc
    global quant
    global ENT
    global trabalho
    global moeda
    global timeframe
    global parfixo
    global padraoTrabalho

    if trabalho == 'fixo':
        ativo = parfixo
        padrao = padraoTrabalho
    

    
    
    #print(NV)
    if isinstance(id, int):
    #ui.listWidget_2.insertItem(0, f'{id} {ativo}')               
        while True:

            data = datas()
            hora = horario()
            
            status,lucro = iq.check_win_digital_v2(id)
            if status:
                
                if lucro < 0 and NV > 0:
                    NV -= 1
                    CT += 1
                    percas += round(lucro, 2)
                    atual += round(lucro, 2)
                    ban = round(banca(), 2)
                    inicio(ganhos, percas, atual)

                    NOVA_ENTRADA = float(quantidade)*MT
                    entrada = 'R$ {:,.2f}'.format(NOVA_ENTRADA)
                    print(f'{Amarelo}MARTINGALE: {Reset}'+str(CT)+ ' ' + padrao.upper() + ' ' +str(hora)+', ATIVO: '+str(ativo)+' - '+str(entrada))
                        
                    status,id = iq.buy_digital_spot(ativo, NOVA_ENTRADA, direcao, tempo)
                    
                    if trabalho == 'lista':
                        Verifica_status_D(id,ativo,NOVA_ENTRADA,direcao,tempo,opcao,hora,NV,MT,CT,timeframe)
                    else:
                        Verifica_status_D(id,ativo,NOVA_ENTRADA,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                    
                    

                elif lucro > 0:
                    VTS += 1
                    ganhos += round(lucro, 2)
                    atual += round(lucro, 2)
                    ban = round(banca(), 2)
                    VIT += 1
                    lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                    
                    
                    if CT == 1:
                        alerta(round(quantidade, 2),round(lucro, 2),round(lucros, 2),"G1",direcao.upper(),padrao.upper(),ativo,data,hora)
                    elif CT == 2:
                        alerta(round(quantidade, 2),round(lucro, 2),round(lucros, 2),"G2",direcao.upper(),padrao.upper(),ativo,data,hora)
                    else:
                        alerta(round(quantidade, 2),round(lucro, 2),round(lucros, 2),"WIN",direcao.upper(),padrao.upper(),ativo,data,hora)

                    inicio(ganhos, percas, atual)
                    
                    print(f'{Verde}{ativo} | {direcao.upper()} | VITORIA{Reset}')
                    print('Lucro:' + str(round(lucro, 2)))
                    
                    time.sleep(5)
                    mta = stop(ganhos,percas)
                    if mta:
                        print('\n!!! MOBTRADER BOT, RESPEITE SEU GERENCIAMENTO!!!')
                        sys.exit()
                    if trabalho == 'lista':  
                        lista_sinais()
                    elif trabalho == 'fixo':
                        entradas_fixas(parfixo, padraoTrabalho)
                    else:
                        buscar()
                    
                    
            
            
                elif lucro < 0:
                    
                
                    VTS = 0
                    percas += round(lucro, 2)
                    atual += round(lucro, 2)
                    ban = round(banca(), 2)
                    DER += 1
                    lucros = float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))
                    
                                        
                    alerta(round(quantidade, 2),round(lucro, 2),round(lucros, 2),"HIT",direcao.upper(),padrao.upper(),ativo,data,hora)
                    
                    inicio(ganhos, percas, atual)
                                        
                    print(f'{Vermelho}{ativo} | {direcao.upper()} | DERROTA{Reset}')
                    print('Lucro:' + str(round(lucro, 2)))
                    
                    time.sleep(5)
                    mta = stop(ganhos,percas)
                    if mta:
                        print('\n!!! MOBTRADER BOT, RESPEITE SEU GERENCIAMENTO!!!')
                        sys.exit()
                    if trabalho == 'lista':  
                        lista_sinais()

                    elif trabalho == 'fixo':
                        entradas_fixas(ativo, padraoTrabalho)
                        
                    else:
                        buscar()
                        
                        
                
                else:
                    print(f'{Azul}{ativo} | {direcao.upper()} | DOJI{Reset}')
                    print('Lucro:' + str(round(lucro, 2)))
                    
                    time.sleep(5)
                    mta = stop(ganhos,percas)
                    if mta:
                        print('\n!!! MOBTRADER BOT, RESPEITE SEU GERENCIAMENTO!!!')
                        sys.exit()
                    
                    alerta(round(quantidade, 2),round(lucro, 2),round(lucros, 2),"DOJI",direcao.upper(),padrao.upper(),ativo,data,hora)
                    if trabalho == 'lista':  
                        lista_sinais()
                    elif trabalho == 'fixo':
                        entradas_fixas(ativo, padraoTrabalho)
                    else:
                        buscar()
                                                    
                                    
            stop(ganhos,percas)

def confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par):
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global sorosmao
    global ENT
    global gales
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND


    dir = direcao
    if TEND:
        dica = tendencia(par)
        print(f'Tendencia = {dica}')

        if opcao == 'binaria':
            ban = round(banca(), 2)
            entrada = 'R$ {:,.2f}'.format(quantidade)
            print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
            print(f'Direção: {dir}\n')
            if pulos == 0:
                status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
            elif pulos == 1 and velasM == 'M1': 
                time.sleep(60)
                status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
            elif pulos == 2 and velasM == 'M1':
                time.sleep(120)
                status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
            elif pulos == 1 and velasM == 'M5':
                time.sleep(300)
                status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
            elif pulos == 2 and velasM == 'M5':
                time.sleep(600)
                status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))

            if id:
                Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                
            else:
                print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))
                                     
                
        elif opcao == 'digital':
            ban = round(banca(), 2)
            entrada = 'R$ {:,.2f}'.format(quantidade)
            print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
            print(f'Direção: {dir}\n')
            
            if pulos == 0:
                status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
            elif pulos == 1 and velasM == 'M1': 
                time.sleep(60)
                status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
            elif pulos == 2 and velasM == 'M1':
                time.sleep(120)
                status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
            elif pulos == 1 and velasM == 'M5':
                time.sleep(300)
                status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
            elif pulos == 2 and velasM == 'M5':
                time.sleep(600)
                status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))

            if id:
                Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                
            else:
                print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

           
    else:
        dica = tendencia(par)
        print(f'Tendencia = {dica}')
        if direcao.upper() == dica.upper():
            if opcao == 'binaria':
                ban = round(banca(), 2)
                entrada = 'R$ {:,.2f}'.format(quantidade)
                print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                print(f'Direção: {dir}\n')
                if pulos == 0:
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                elif pulos == 1 and velasM == 'M1': 
                    time.sleep(60)
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                elif pulos == 2 and velasM == 'M1':
                    time.sleep(120)
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                elif pulos == 1 and velasM == 'M5':
                    time.sleep(300)
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                elif pulos == 2 and velasM == 'M5':
                    time.sleep(600)
                    status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))

                if id:
                    Verifica_status(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                    
                else:
                    print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

            
                                
                    
            elif opcao == 'digital':
                ban = round(banca(), 2)
                entrada = 'R$ {:,.2f}'.format(quantidade)
                print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                print(f'Direção: {dir}\n')
                
                if pulos == 0:
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                elif pulos == 1 and velasM == 'M1': 
                    time.sleep(60)
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                elif pulos == 2 and velasM == 'M1':
                    time.sleep(120)
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                elif pulos == 1 and velasM == 'M5':
                    time.sleep(300)
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                elif pulos == 2 and velasM == 'M5':
                    time.sleep(600)
                    status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))

                if id:
                    Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                    
                else:
                    print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))
            
        else:
            print('ENTRADA CONTRA TENDENCIA, IREI RECUSAR ESTA...')
            time.sleep(2)
            if trabalho == 'lista':
                inicioLista(ganhos, percas, atual, moeda, timeframe)
            elif trabalho == 'fixo':
                inicioFixo(ganhos, percas, atual)
            else:
                inicio(ganhos, percas, atual)

def entradas_fixas(parfixo, padraoTrabalho):
    global paridade
    global opcao
    global TEND
    global trabalho
    global op_definida
    global iqo_api
    

    paridade = parfixo
    

    os.system('cls' if os.name == 'nt' else 'clear')
    
    while True:
        
        
        print('Buscando melhor Payout')
        if velasM == 'M1':
            opcao,percent,sta = most_profit_mode(iqo_api, paridade, 1, min_payout=(int(paym) / 100))
        elif velasM == 'M5':
            opcao,percent,sta = most_profit_mode(iqo_api, paridade, 5, min_payout=(int(paym) / 100))
        
        
        if opcao == 'turbo':
            opcao = 'binaria'
        if opcao == 'closed' or opcao == 'error' or opcao == 'payout':
            print('Moeda fora de operação neste momento')
            time.sleep(5)
            entradas_fixas(parfixo, padraoTrabalho)
           
        
        if percent < (int(paym) / 100):
            print('payout = ',percent)
            print(f'Payout Abaixo do padrão que é {paym}%, vamos esperar subir mais para entrar.')
            time.sleep(5)
            entradas_fixas(parfixo, padraoTrabalho)
              
            
        else:
            inicio(ganhos, percas, atual)
                        
            mta = stop(ganhos,percas)
        
        if mta:
            print('\n!!! MOBTRADER BOT, RESPEITE SEU GERENCIAMENTO!!!')
            sys.exit()
            
        else:
            if padraoTrabalho == 'MHI':
                c3 = False
                MHI0()
                break
            
            elif padraoTrabalho == 'MHI2':
                c3 = False
                MHI_2()
                break
                
            elif padraoTrabalho == 'MHI3':
                c3 = False
                MHI_3()
                break
                
            elif padraoTrabalho == 'MHI2_Maioria':
                c3 = False
                MHI2_MAIORIA()
                break
                
            elif padraoTrabalho == 'MHI3_Maioria':
                c3 = False
                MHI3_MAIORIA()
                break
                
            elif padraoTrabalho == 'Milhao_Minoria':
                c3 = False
                MILHAO_MINORIA()
                break
                
            elif padraoTrabalho == 'Milhao_Maioria':
                c3 = False
                MILHAO_MAIORIA()
                break
                
            elif padraoTrabalho == 'Padrao_Impar':
                c3 = False
                PADRAO_IMPAR()
                break
                
            elif padraoTrabalho == 'Torres_Gemeas':
                c3 = False
                TORRES_GEMEAS()
                break
                
            elif padraoTrabalho == 'Tres_Mosqueteiros':
                c3 = False
                TRES_MOSQUETEIROS()
                break
                          
            elif padraoTrabalho == 'Melhor_de_3':
                c3 = False
                MELHOR_DE_3()
                break
                
            elif padraoTrabalho == 'Padrao_23':
                c3 = False
                PADRAO_23()
                break
                
            elif padraoTrabalho == 'MHI_Maioria':
                c3 = False
                MHI_MAIORIA()    
                break   

            elif padraoTrabalho == 'Five_Flip':
                c3 = False
                FIVE_FLIP()    
                break

            elif padraoTrabalho == 'Tres_vizinhos':
                c3 = False
                TRES_VIZINHOS()    
                break
            
            elif padrao == 'MHI_de_Meio_Ciclo':
                c3 = False
                MHI_MEIO()    
                break
            else:
                time.sleep(10)
                entradas_fixas(parfixo, padraoTrabalho)
                break

def carregar_sinais():
    global minha_lista
    global chaveN

    data = {'chave': f'{chaveN}', 'acao': 'logar'}
    url = "http://mobtrader.myartsonline.com/lista/list.php"    
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

def lista_sinais():
    global quantidade
    global gales
    global FL
    global iqo_api
    global paym
    global DER
    global VIT
    global atual
    global opcao
    global padrao
    global paridade
    
    opcao = 'digital'
    lista = carregar_sinais()

    NV = int(gales)
    MT = float(FL)
    CT = 0

    grana = 'R$ {:,.2f}'.format(atual)
    perdeu = DER
    ganhou = VIT


    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        to = 0
        data = datetime.now() .strftime('%Y-%m-%d %H:%M:%S')
        i = 0

        print(f'{Amarelo} LOSS: {perdeu} / WIN: {ganhou} = Lucros: {grana} {Reset} - ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        
        for sinal in lista:
            to = to + 1
            dados = sinal.split(',')
            dia = (str(dados[0]))
            hora = (dados[1])+':00'
            moeda = (str(dados[2])).upper()
            direcao = (dados[3]).lower()
            timeframe = (dados[4]).upper()

            agora = datetime.now()
            data_atual = agora.strftime('%d')

            hora_pay = datetime.now() + timedelta(seconds=40)
            hora_atual_pay = hora_pay.strftime('%H:%M:%S')
            
            now = datetime.now() + timedelta(seconds=3)
            hora_atual = now.strftime('%H:%M:%S')

            entrada = float(quantidade)

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
            paridade = moeda
            padrao = 'LISTA'
            if data_atual == dia:
                #print(hora_atual, hora)
                if hora_atual_pay == hora:
                    time.sleep(0.5)
                    #inicioLista(ganhos, percas, atual, moeda, timeframe)
                    inicio(ganhos, percas, atual)
                    print('Buscando melhor Payout')
                    opcao,percent,sta = most_profit_mode(iqo_api, moeda, tempo, min_payout=(int(paym) / 100))
                    #opcao = pay(paridade, "melhor", 1)
                    time.sleep(1)
                    if sta == False:
                        print(f'Moeda {moeda}, não disponivel, aguarde....')
                        time.sleep(2)
                        lista_sinais()
                        
                        

                    if opcao == 'turbo':
                        opcao = 'binaria'
                    if opcao == 'closed' or opcao == 'error' or opcao == 'payout':
                        print('Moeda fora de operação neste momento')
                        time.sleep(5)
                        lista_sinais()
                    if percent < (int(paym) / 100):
                        print('payout = ',percent)
                        print(f'Payout Abaixo do padrão que é {paym}%, Recusarei este sinal, aguarde....')
                        time.sleep(2)
                        lista_sinais()
                    break

                if hora_atual == hora:
                    time.sleep(0.5)
                    inicio(ganhos, percas, atual)
                    if opcao == 'binaria':
                        entrada = 'R$ {:,.2f}'.format(quantidade)
                        print('Entrada realizada, valor '+str(entrada)+' - '+str(moeda))
                        print(f'Direção: {direcao.upper()}\n')
                                                
                        status,id = iq.buy(float(quantidade), str(moeda), str(direcao), int(tempo))
                        
                        Verifica_status(id,moeda,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,timeframe)
                    
                                              
                    elif opcao == 'digital':
                        ban = round(banca(), 2)
                        entrada = 'R$ {:,.2f}'.format(quantidade)
                        print('Entrada realizada, valor '+str(entrada)+' - '+str(moeda))
                        print(f'Direção: {direcao.upper()}\n')
                        
                        
                        status,id = iq.buy_digital_spot(str(moeda),float(quantidade),str(direcao), int(tempo))
                        
                        Verifica_status_D(id,moeda,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,timeframe)
                        
                    
                    else:
                        ban = round(banca(), 2)
                        entrada = 'R$ {:,.2f}'.format(quantidade)
                        print('Entrada realizada, valor '+str(entrada)+' - '+str(moeda))
                        print(f'Direção: {direcao.upper()}\n')
                        
                        
                        status,id = iq.buy_digital_spot(str(moeda),float(quantidade),str(direcao), int(tempo))
                        
                        Verifica_status_D(id,moeda,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,timeframe)
                        
        
        time.sleep(1)

# === PADROES =====================

def MHI0():
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global sorosmao
    global ENT
    global gales
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho




    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('HM5.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
                              
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            #print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar()
           
            if dir:
                direcao = str(dir)
                ativo = str(par)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)
                break

def MHI_2():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('HM5.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            #print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar()
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                if velasM == 'M1':
                    time.sleep(60)
                elif velasM == 'M5':
                    time.sleep(300)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)
                        

                    
        time.sleep(1)

def MHI_3():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('HM5.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            #print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar() 
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                if velasM == 'M1':
                    time.sleep(120)
                elif velasM == 'M5':
                    time.sleep(600)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)
                        

                    
        time.sleep(1)
    
def MHI_MAIORIA():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('HM5.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            #print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar()  
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)
                        
                    
        time.sleep(1)
    
def MHI2_MAIORIA():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('HM5')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            #print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar()  
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                if velasM == 'M1':
                    time.sleep(60)
                elif velasM == 'M5':
                    time.sleep(300)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)
                        
                    
        time.sleep(1)

def MHI3_MAIORIA():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('HM5.txt')
            for horaM5 in lista5:
                    entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            #print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar()   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                if velasM == 'M1':
                    time.sleep(120)
                elif velasM == 'M5':
                    time.sleep(600)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)
                        
                    
        time.sleep(1)

def MILHAO_MAIORIA():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('HM5.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 5, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
            
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 5, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
                velas[5] = 'verde' if velas[5]['open'] < velas[5]['close'] else 'vermelha' if velas[5]['open'] > velas[5]['close'] else 'doji'
            
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 5, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2] + ' ' + velas[3]	+ ' ' + velas[4]+ ' ' + velas[5]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            #print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR EMPATE OU DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar()
                
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)
                        
                    
        time.sleep(1)

def MILHAO_MINORIA():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('HM5.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 5, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
            
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 5, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
                velas[5] = 'verde' if velas[5]['open'] < velas[5]['close'] else 'vermelha' if velas[5]['open'] > velas[5]['close'] else 'doji'
            
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 5, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2] + ' ' + velas[3]	+ ' ' + velas[4]	
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            #print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar()
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)
                        
                    
        time.sleep(1)

def TRES_VIZINHOS():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 2.58 and minutos <= 5) or minutos >= 7.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('M5tresvizinhos.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 5, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 5, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 5, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
            
            
            cor = velas[0]
            #print(cores)

            if cor == 'verde':
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif cor == 'vermelha':
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar()
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)
                        
                    
        time.sleep(1)

def PADRAO_IMPAR():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('M5tresvizinhos.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cor = velas[2]
            #print(cores)

            if cor == 'verde':
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif cor == 'vermelha':
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar()  
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)
        
        time.sleep(1)

def MELHOR_DE_3():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('M5tresvizinhos.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 4, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'

            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 4, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'

            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 4, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
            
            cores = velas[1] + ' ' + velas[2] + ' ' + velas[3]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            #print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar()   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                time.sleep(120)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)


        time.sleep(1)

def TRES_MOSQUETEIROS():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if minutos == 2.58 or minutos == 7.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('M5tresmosqueteiros.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 1, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
               
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 1, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
               
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 1, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                        
            cor = velas[0]	
            #print(cor)

            if cor == 'verde':
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif cor == 'vermelha':
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar() 
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)


        time.sleep(1)

def FIVE_FLIP():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 3.58 and minutos <= 5) or minutos >= 8.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('M5fiveflip.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 4, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'

            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 4, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'

            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 4, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
            
            cor = velas[0]
            #print(cores)

            if cor == 'verde':
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif cor == 'vermelha':
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar()

            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                #time.sleep(60)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)
        
        time.sleep(1)

def C30():
    global gales
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
    global v4
    global c3
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global parfixo
    global padraoTrabalho
    global trabalho

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        elif velasM == 'M5':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 5.58 and minutos <= 30) else False
        elif velasM == 'M15':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 5.58 and minutos <= 60) else False
        #print('Aguardando: '+str(minutos))
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        #time.sleep(0.5)
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 5, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
            
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 5, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
            
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 5, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                velas[4] = 'verde' if velas[4]['open'] < velas[4]['close'] else 'vermelha' if velas[4]['open'] > velas[4]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2] + ' ' + velas[3] + ' ' + velas[4]
           

            v4 = velas[4]
            v2 = velas[2]
            v0 = velas[0]
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
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
   
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 3.58 and minutos <= 5) or minutos >= 8.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('M5fiveflip.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 4, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 4, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 4, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                velas[3] = 'verde' if velas[3]['open'] < velas[3]['close'] else 'vermelha' if velas[3]['open'] > velas[3]['close'] else 'doji'
                
            
            cores = velas[3]		
            #print(cores)

            if cores == 'verde':
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif cores == 'vermelha':
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                buscar()
                break  
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                if TEND:
                    dica = tendencia(par)
                    print(f'Tendencia = {dica}')
                    if opcao == 'binaria':
                        ban = round(banca(), 2)
                        entrada = 'R$ {:,.2f}'.format(quantidade)
                        print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                        print(f'Direção: {dir}\n')
                        if pulos == 0:
                            status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                        elif pulos == 1:
                            time.sleep(60)
                            status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                        elif pulos == 2:
                            time.sleep(120)
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
                        
                        if pulos == 0:
                            status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                        elif pulos == 1:
                            time.sleep(60)
                            status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                        elif pulos == 2:
                            time.sleep(120)
                            status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                        
                        if id:
                            Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                            
                        else:
                            print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                        break
                else:
                    dica = tendencia(par)
                    print(f'Tendencia = {dica}')
                    if direcao.upper() == dica.upper():
                        if opcao == 'binaria':
                            ban = round(banca(), 2)
                            entrada = 'R$ {:,.2f}'.format(quantidade)
                            print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                            print(f'Direção: {dir}\n')
                            if pulos == 0:
                                status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                            elif pulos == 1:
                                time.sleep(60)
                                status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                            elif pulos == 2:
                                time.sleep(120)
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
                            
                            if pulos == 0:
                                status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                            elif pulos == 1:
                                time.sleep(60)
                                status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                            elif pulos == 2:
                                time.sleep(120)
                                status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                            
                            if id:
                                Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                                
                            else:
                                print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                            break
                    else:
                        print('ENTRADA CONTRA TENDENCIA, IREI RECUSAR ESTA...')
                        time.sleep(2)
                        if trabalho == 'lista':
                            inicioLista(ganhos, percas, atual, moeda, timeframe)
                        elif trabalho == 'fixo':
                            inicioFixo(ganhos, percas, atual)
                        else:
                            inicio(ganhos, percas, atual)
                        break
                    
        time.sleep(1)
   
def PADRAO_23():
    global gales
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho


    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if minutos == 0.58 or minutos == 5.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('M5fiveflip.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
        
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        
                    
        #ui.listWidget_2.insertItem(0, 'Hora de entrar? '+str(entrar)+'/ Minutos: '+str(minutos))
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            print('Verificando cores..')
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 1, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
               
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 1, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
               
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 1, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
            
            cores = velas[0]	
            #print(cores)
            if cores == 'verde':
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            elif cores == 'vermelha':
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                buscar()
                break   
                
                
            
            if dir:
                #print('Direção: '+str(dir))
                direcao = str(dir)
                ativo = str(par)
                if TEND:
                    dica = tendencia(par)
                    print(f'Tendencia = {dica}')
                    if opcao == 'binaria':
                        ban = round(banca(), 2)
                        entrada = 'R$ {:,.2f}'.format(quantidade)
                        print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                        print(f'Direção: {dir}\n')
                        if pulos == 0:
                            status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                        elif pulos == 1:
                            time.sleep(60)
                            status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                        elif pulos == 2:
                            time.sleep(120)
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
                        
                        if pulos == 0:
                            status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                        elif pulos == 1:
                            time.sleep(60)
                            status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                        elif pulos == 2:
                            time.sleep(120)
                            status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                        
                        if id:
                            Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                            
                        else:
                            print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                        break
                else:
                    dica = tendencia(par)
                    print(f'Tendencia = {dica}')
                    if direcao.upper() == dica.upper():
                        if opcao == 'binaria':
                            ban = round(banca(), 2)
                            entrada = 'R$ {:,.2f}'.format(quantidade)
                            print('Entrada a ser realizada, valor '+str(entrada)+' - '+str(ativo))
                            print(f'Direção: {dir}\n')
                            if pulos == 0:
                                status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                            elif pulos == 1:
                                time.sleep(60)
                                status,id = iq.buy(float(quantidade), str(ativo), str(direcao), int(tempo))
                            elif pulos == 2:
                                time.sleep(120)
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
                            
                            if pulos == 0:
                                status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                            elif pulos == 1:
                                time.sleep(60)
                                status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                            elif pulos == 2:
                                time.sleep(120)
                                status,id = iq.buy_digital_spot(str(ativo),float(quantidade),str(direcao), int(tempo))
                            
                            if id:
                                Verifica_status_D(id,ativo,quantidade,direcao,tempo,opcao,hora,NV,MT,CT,tempo2)
                                
                            else:
                                print('Entrada recusada pela iq: '+str(ativo)+', '+str(tempo2))

                            break
                    else:
                        print('ENTRADA CONTRA TENDENCIA, IREI RECUSAR ESTA...')
                        time.sleep(2)
                        if trabalho == 'lista':
                            inicioLista(ganhos, percas, atual, moeda, timeframe)
                        elif trabalho == 'fixo':
                            inicioFixo(ganhos, percas, atual)
                        else:
                            inicio(ganhos, percas, atual)
                        break
                    
        time.sleep(1)

def MHI_MEIO():
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
    global velasM
    global gerenciada
    global resu
    global luc
    global quant
    global sorosmao
    global ENT
    global gales
    global inverter
    global pulos
    global parfixo
    global padraoTrabalho
    global trabalho
    global TEND

    if trabalho == 'fixo':
        paridade = parfixo
        padrao = padraoTrabalho




    
    NV = int(gales)
    MT = float(FL)
    CT = 0
    
    tempo2 = str(velasM)
    if tempo2 == 'M1':
        tempo = 1
    elif tempo2 == 'M5':
        tempo = 5
    elif tempo2 == 'M15':
        tempo = 15

    par = paridade.upper()

    inicio(ganhos, percas, atual)
    print(f'AGUARDE, BUSCANDO PADRÃO {padrao.upper()}\n')
    while True:
        #print(str(round(LC, 2)))                         
        #print(str(round(BANCA_ATUAL, 2)))
        if velasM == 'M1':
            minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
            entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
        elif velasM == 'M5':
            lista5 = carregarM5('MHIMEIO.txt')
            for horaM5 in lista5:
                entrar = True if horaM5 == datetime.now().strftime('%H:%M:%S') else False
                              
        
        print('Aguardando: ' + datetime.now().strftime('%H:%M:%S'), end='\r')
        
        hora = horario()
        if entrar:
            inicio(ganhos, percas, atual)
            #print('Iniciando operação!')
            dir = False
            
            if velasM == 'M1':
                velas = iq.get_candles(par, 60, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            if velasM == 'M5':
                velas = iq.get_candles(par, 300, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
                
            if velasM == 'M15':
                velas = iq.get_candles(par, 900, 3, time.time())
            
                velas[0] = 'verde' if velas[0]['open'] < velas[0]['close'] else 'vermelha' if velas[0]['open'] > velas[0]['close'] else 'doji'
                velas[1] = 'verde' if velas[1]['open'] < velas[1]['close'] else 'vermelha' if velas[1]['open'] > velas[1]['close'] else 'doji'
                velas[2] = 'verde' if velas[2]['open'] < velas[2]['close'] else 'vermelha' if velas[2]['open'] > velas[2]['close'] else 'doji'
            
            
            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            #print(cores)
            verd = int(cores.count('verde'))
            verme = int(cores.count('vermelha'))
            #print(f'{Verde}verdes{Reset} {verd} | {Vermelho}vermelha {Reset}{verme} ')
            if verd > verme: 
                if inverter:
                    dir = 'call'
                else:
                    dir = 'put'
                print(f'{Vermelho}{padrao} = {dir}{Reset}')
            elif verme > verd: 
                if inverter:
                    dir = 'put'
                else:
                    dir = 'call'
                print(f'{Verde}{padrao} = {dir}{Reset}')
            else:
                print('ENTRADA RECUSADA POR CAUSA DO DOJI')
                dir = False
                STP = True   
                if trabalho == 'lista':  
                    lista_sinais()
                elif trabalho == 'fixo':
                    entradas_fixas(parfixo, padraoTrabalho)
                else:
                    buscar()
           
            if dir:
                direcao = str(dir)
                ativo = str(par)
                confirmadas(direcao,ativo,tempo,tempo2,hora,NV,MT,CT,par)
                break

#=========================================
def pegar_id(user_chave):
    global Pconta
    global Pentrada
    global Pstoploss
    global Pstopwin
    global Pgales
    global Pvelas
    global PMHI
    global PMHI2
    global PMHI3
    global PMHI2_Maioria
    global PMHI3_Maioria
    global PMilhao_Minoria
    global PMilhao_Maioria
    global PPadrao_Impar
    global PTorres_Gemeas
    global PTres_Mosqueteiros
    global PMelhor_de_3
    global PPadrao_23
    global PMHI_Maioria
    global Ppaym
    global Pacerm
    global Perros
    global Pinverter
    global Ppular
    global sua_chave
    global user_id

    data = {'chave': f'{user_chave}', 'acao': 'logar'}
    url = "http://mobtrader.myartsonline.com/jogadores.php"    
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
        Pentrada = lista2[4]
        Pstoploss = lista2[5]
        Pstopwin = lista2[6]
        Pgales = int(lista2[9])
        Pvelas = lista2[11]
        PMHI = int(lista2[12])
        PMHI2 = int(lista2[13])
        PMHI3 = int(lista2[14])
        PMHI2_Maioria = int(lista2[15])
        PMHI3_Maioria = int(lista2[16])
        PMilhao_Minoria = int(lista2[17])
        PMilhao_Maioria = int(lista2[18])
        PPadrao_Impar = int(lista2[19])
        PTorres_Gemeas = int(lista2[20])
        PTres_Mosqueteiros = int(lista2[21])
        PMelhor_de_3 = int(lista2[23])
        PPadrao_23 = int(lista2[24])
        PMHI_Maioria = int(lista2[25])
        Ppaym = int(lista2[32])
        Pacerm = int(lista2[33])
        Perros = int(lista2[34])
        Pinverter = int(lista2[35])
        Ppular = int(lista2[36])
        user_id = int(lista2[28])
        
        return sua_chave

def verificacao():
    global ver
    
    bot = 'mobtradertermux'
    data = {'desenvolvedor': f'{bot}','acao': 'verificar'}
    url = "http://mobtrader.myartsonline.com/bot/jogadores.php"    
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
        return f'{Vermelho}{msg}{Reset}\n{Amarelo}Sua versão ={Reset} {Vermelho}{ver}{Reset}\n{Amarelo}Versão atual ={Reset} {Verde}{versao}{Reset}\n{Amarelo}Entre em:{Reset} {Verde}{link}{Reset}\n\n{Azul}(MOBTRADER BOT !!!){Reset}'
    else:
        return ''

def confirma():
    global nome
    global senha
    global email
    global conta
    global entrada
    global stoploss
    global stopwin
    global autonomo
    global horas
    global gales
    global fator
    global velasM
    global MHI
    global MHI2
    global MHI3
    global MHI2_Maioria
    global MHI3_Maioria
    global Milhao_Minoria
    global Milhao_Maioria
    global Padrao_Impar
    global Torres_Gemeas
    global Tres_Mosqueteiros
    global C3
    global Melhor_de_3
    global Padrao_23
    global MHI_Maioria
    global ativacao
    global soroGales
    global login
    global password
    global tp
    global quantidade
    global STOPLOSS
    global STOPWIN
    global stop_win
    global stop_loss
    global sistema
    global espera
    global FL
    global gerenciada
    global GL
    global AT
    global account_type
    global tp
    global martingale
    global chaveN
    global ENT
    global G
    global paym
    global acerm
    global erros
    global inverter
    global pulos
    global Pconta
    global Pentrada
    global Pstoploss
    global Pstopwin
    global Pgales
    global Pvelas
    global PMHI
    global PMHI2
    global PMHI3
    global PMHI2_Maioria
    global PMHI3_Maioria
    global PMilhao_Minoria
    global PMilhao_Maioria
    global PPadrao_Impar
    global PTorres_Gemeas
    global PTres_Mosqueteiros
    global PMelhor_de_3
    global PPadrao_23
    global PMHI_Maioria
    global Ppaym
    global Pacerm
    global Perros
    global Pinverter
    global Ppular
    global user_id
    global catalogo
    global cliente
    global cat
    global chaveN
    global trabalho
    global padrao_fixo
    global TEND
    global op_definida

    os.system('cls' if os.name == 'nt' else 'clear')
    print('OK, BEM VINDO AO MOBTRADER, DIGITE SUA CHAVE\n')
    chaveN = str(input(': '))
    data = {'chave': f'{chaveN}', 'acao': 'logar'}
    url = "http://mobtrader.myartsonline.com/jogadores.php"    
    resp = requests.post(url, data)
    listaRetorno = []
    if resp.text != '0':
        lista = resp.text.split(',')
                        
        for i in lista:
            listaRetorno.append(i)
        nome = listaRetorno[0].replace(' ','')
        senha = listaRetorno[1].replace(' ','')
        email = listaRetorno[2].replace(' ','')
        conta = listaRetorno[3].replace(' ','')
        entrada = listaRetorno[4].replace(' ','')
        stoploss = listaRetorno[5].replace(' ','')
        stopwin = listaRetorno[6].replace(' ','')
        autonomo = listaRetorno[7].replace(' ','')
        horas = listaRetorno[8].replace(' ','')
        gales = listaRetorno[9].replace(' ','')
        fator = listaRetorno[10].replace(' ','')
        velasM = listaRetorno[11].replace(' ','')
        if listaRetorno[12].replace(' ','') == '0':
            MHI = False
        else:
            MHI = True
        if listaRetorno[13].replace(' ','') == '0':
            MHI2 = False
        else:
            MHI2 = True
        if listaRetorno[14].replace(' ','') == '0':
            MHI3 = False
        else:
            MHI3 = True
        if listaRetorno[15].replace(' ','') == '0':
            MHI2_Maioria = False
        else:
            MHI2_Maioria = True
        if listaRetorno[16].replace(' ','') == '0':
            MHI3_Maioria = False
        else:
            MHI3_Maioria = True
        if listaRetorno[17].replace(' ','') == '0':
            Milhao_Minoria = False
        else:
            Milhao_Minoria = True
        if listaRetorno[18].replace(' ','') == '0':
            Milhao_Maioria = False
        else:
            Milhao_Maioria = True
        if listaRetorno[19].replace(' ','') == '0':
            Padrao_Impar = False
        else:
            Padrao_Impar = True
        if listaRetorno[20].replace(' ','') == '0':
            Torres_Gemeas = False
        else:
            Torres_Gemeas = True
        if listaRetorno[21].replace(' ','') == '0':
            Tres_Mosqueteiros = False
        else:
            Tres_Mosqueteiros = True
        if listaRetorno[22].replace(' ','') == '0':
            C3 = False
        else:
            C3 = True            
        if listaRetorno[23].replace(' ','') == '0':
            Melhor_de_3 = False
        else:
            Melhor_de_3 = True           
        if listaRetorno[24].replace(' ','') == '0':
            Padrao_23 = False
        else:
            Padrao_23 = True
        if listaRetorno[25].replace(' ','') == '0':
            MHI_Maioria = False
        else:
            MHI_Maioria = True     
        ativacao = listaRetorno[26].replace(' ','')
        soroGales = listaRetorno[27].replace(' ','')

        paym = int(listaRetorno[32])
        acerm = int(listaRetorno[33])
        erros = int(listaRetorno[34])
        inver = int(listaRetorno[35])
        pulos = int(listaRetorno[36])
        catalogo = int(listaRetorno[37])
        cliente = str(listaRetorno[38])
        if cliente == 'TESTE':
            conta = 'PRACTICE'

        if catalogo == 0:
            cat = 'Catalogação automatica'
        elif catalogo == 1:
            cat = 'Catalogação de mão fixa'
        elif catalogo == 2:
            cat = 'Catalogação de 1 gale'
        elif catalogo == 3:
            cat = 'Catalogação de 2 gale'
        


        if inver == 0:
            inverter = False
        else:
            inverter = True
                        

        login = str(email)
        password = str(senha)
        account_type = str(conta)
        tp = account_type
        quantidade = float(entrada)
        ENT = float(entrada)
        STOPLOSS = float(stoploss)
        STOPWIN = float(stopwin)
        stop_win = float(STOPWIN)
        stop_loss = float(STOPLOSS)
        sistema = str(autonomo)
        if soroGales == 'sim':
            gerenciada = True
        else:
            gerenciada = False
        
        if sistema == 'sim':
            AT = True
            
            martingale = int(gales)
            #martingale += 1
            FL = float(fator)
            espera = int(horas)
        
        elif sistema == 'nao':
            AT = False
            
            martingale = int(gales)
            martingale += 1
            FL = float(fator)
        if int(gales) == 0:
            G = 'Mão fixa'
        if int(gales) == 1:
            G = '1 Gale'
        if int(gales) == 2:
            G = '2 Gale'       
        
        
        return True
        
        
    else:
        return resp.text




check = str(verificacao())
if check != '':
    os.system('cls' if os.name == 'nt' else 'clear')
    print(check)
    time.sleep(5)
    pass
else:
    pass
chave = str(confirma())
if chave == '0':
    os.system('cls' if os.name == 'nt' else 'clear')
    print('CHAVE NÃO ENCONTRADA!')
    sys.exit()
    
else:
    os.system('cls' if os.name == 'nt' else 'clear')
    if ativacao != 'ok':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('VERIFIQUE O APLICATIVO DE CONFIGURAÇÕES!')
        sys.exit()
    

os.system('cls' if os.name == 'nt' else 'clear')
print('QUAL O TIPO DE OPERAÇÃO?\n\n1 = FIXA\n2 = AUTOMATICA\n3 = LISTA\n ')
modo_catalogar = int(input('Digite um numero: '))
os.system('cls' if os.name == 'nt' else 'clear')
print('POSSO OPERAR CONTRA A TENDENCIA?\n\n1 = SIM\n2 = NÃO\n')
tem = int(input('digite um numero: '))
if tem == 1:
    TEND = True
else:
    TEND = False
if modo_catalogar == 1:
    trabalho = 'fixo'
    os.system('cls' if os.name == 'nt' else 'clear')
    disponiveis = disponiveis(str(velasM),int(gales))
    to = -1
    list_dispo = []
    print('SELECIONE UM NUMERO:')
    for i in disponiveis:
        to += 1
        list_dispo.append(i)

        print(f'{to} = {i}')
    npar = int(input(': '))
    if npar == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'OK, ENTÃO ESCOLHA O MODO AUTOMATICO PARA USAR TODOS!')
        sys.exit()
    parfixo = list_dispo[npar]
    paridade = parfixo
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'AGORA ESCOLHA O NUMERO DO PADRÃO DESEJADO: ')
    print('1 = MHI')
    print('2 = MHI2')
    print('3 = MHI3')
    print('4 = MHI_Maioria')
    print('5 = MHI2_Maioria')
    print('6 = MHI3_Maioria')
    print('7 = Milhao_Minoria')
    print('8 = Milhao_Maioria')
    print('9 = Padrao_Impar')
    print('10 = Torres_Gemeas')
    print('11 = Tres_Mosqueteiros')
    print('12 = Melhor_de_3')
    print('13 = Padrao_23')
    print('14 = Five_Flip')
    print('15 = Tres_vizinhos')
    print('16 = MHI_de_Meio_Ciclo')
    padraoEscolha = int(input(': '))
    if padraoEscolha == 1:
        padraoTrabalho = 'MHI'
    elif padraoEscolha == 2:
        padraoTrabalho = 'MHI2'
    elif padraoEscolha == 3:
        padraoTrabalho = 'MHI3'
    elif padraoEscolha == 4:
        padraoTrabalho = 'MHI_Maioria'
    elif padraoEscolha == 5:
        padraoTrabalho = 'MHI2_Maioria'
    elif padraoEscolha == 6:
        padraoTrabalho = 'MHI3_Maioria'
    elif padraoEscolha == 7:
        padraoTrabalho = 'Milhao_Minoria'
    elif padraoEscolha == 8:
        padraoTrabalho = 'Milhao_Maioria'
    elif padraoEscolha == 9:
        padraoTrabalho = 'Padrao_Impar'
    elif padraoEscolha == 10:
        padraoTrabalho = 'Torres_Gemeas'
    elif padraoEscolha == 11:
        padraoTrabalho = 'Tres_Mosqueteiros'
    elif padraoEscolha == 12:
        padraoTrabalho = 'Melhor_de_3'
    elif padraoEscolha == 13:
        padraoTrabalho = 'Padrao_23'
    elif padraoEscolha == 14:
        padraoTrabalho = 'Five_Flip'
    elif padraoEscolha == 15:
        padraoTrabalho = 'Tres_vizinhos'
    elif padraoEscolha == 16:
        padraoTrabalho = 'MHI_de_Meio_Ciclo'
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'OK, VAMOS TRABALHAR FIXO NA MOEDA {Amarelo}{parfixo}{Reset} COM PADRÃO {Verde}{padraoTrabalho}{Reset}')
elif modo_catalogar == 2:
    trabalho = 'automatico'
elif modo_catalogar == 3:
    trabalho = 'lista'

print(f'{Verde}SUAS CONFIGURAÇÕES SÃO:{Reset}')
print(f'{Amarelo}CONTA:{Reset} {Azul}{conta}{Reset}')
print(f'{Amarelo}VALOR DE ENTRADA:{Reset} {Azul}{entrada}{Reset}')
print(f'{Amarelo}MARTINGALES:{Reset} {Azul}{gales}{Reset}')
print(f'{Amarelo}CATALOGAÇÃO:{Reset} {Azul}{cat}{Reset}')
print(f'{Amarelo}PULAR{Reset} {Azul}{pulos}{Reset} {Amarelo}VELAS{Reset} ')
print(f'{Amarelo}INVERSÃO:{Reset} {Azul}{inverter}{Reset}')
print(f'{Amarelo}STOPLOSS:{Reset} {Azul}{STOPLOSS}{Reset}')
print(f'{Amarelo}STOPWIN:{Reset} {Azul}{STOPWIN}{Reset}')
print(f'{Amarelo}VELAS DE:{Reset} {Azul}{velasM}{Reset}')
time.sleep(5)
os.system('cls' if os.name == 'nt' else 'clear')
print(f'AGORA VOU CONECTAR COM A IQ, AGUARDE...')


# Aqui começa a configuração da API, não alterar
#:===============================================================:#

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

if trabalho == 'fixo':
    entradas_fixas(parfixo, padraoTrabalho)
elif trabalho == 'automatico':
    buscar()
if trabalho == 'lista':
    buscar()


