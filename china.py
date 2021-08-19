from iqoptionapi.stable_api import IQ_Option
from finta import TA
from time import time, sleep
from datetime import datetime
import pandas as pd
import os, sys
from urllib.request import urlretrieve
import requests

password = ""
login = ""
cliente = ""
nome = ""
derrotas = 0



def tendencia(par,tempo):
	
    #par = 'AUDCAD'
    timeframe = tempo

    velas = API.get_candles(par, (int(timeframe) * 60), 5,  time())

    ultimo = round(velas[0]['close'], 4)
    primeiro = round(velas[-1]['close'], 4)

    diferenca = abs( round( ( (ultimo - primeiro) / primeiro ) * 100, 3) )
    tendencia = "CALL" if ultimo < primeiro and diferenca > 0.01 else "PUT" if ultimo > primeiro and diferenca > 0.01 else False
    
    return tendencia

def confirma():
	global cliente
	global nome
	global login
	global password

	os.system('cls' if os.name == 'nt' else 'clear')
	print('BEM VINDO AO MOBTRADER ESTRATÉGIA CHINESA BASICA, DIGITE SUA CHAVE\n')
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
		
		
		
		if cliente == 'TESTE':
			os.system('cls' if os.name == 'nt' else 'clear')
			print('Desculpe, Somente para vip!!!')
			print('\n')
			print('ADQUIRA O BOT ENTRANDO EM CONTATO COM ZAP 11976159233')
			sys.exit()
				
		return True
		
	else:
		return resp.text

chaveN = str(confirma())
if chaveN == '0':
    os.system('cls' if os.name == 'nt' else 'clear')
    print('CHAVE NÃO ENCONTRADA!')
    sys.exit()

API = IQ_Option(login, password)
API.connect()
os.system('cls' if os.name == 'nt' else 'clear')
print(f"Olá, {nome}, vamos operar !!! ")

if cliente == "TESTE":
	print("Escolha a conta:\n1 = Real (somente para VIP)\n2 = Demo\n")
else:
	print("Escolha a conta:\n1 = Real\n2 = Demo\n")

nconta = input("Digite um numero: ")
if nconta == "1":
	if cliente == "TESTE":
		conta = "PRACTICE"
	else:
		conta = "REAL"
else:
	conta = "PRACTICE"



API.change_balance(conta) # PRACTICE / REAL


if API.check_connect():
	os.system('cls' if os.name == 'nt' else 'clear')
	print('Ok, Conectado com sucesso na iq!')
else:
	os.system('cls' if os.name == 'nt' else 'clear')
	print(' Erro ao conectar')
	input('\n\n Aperte enter para sair')
	exit()

def banca():
	global API
	return API.get_balance()
BANCAINICIAL = float(round(banca(), 2))

def get_data(par, timeframe, periods = 200,):
	global API
	
	
	velas = API.get_candles(par, timeframe * 60, periods, time())
	
	df = pd.DataFrame(velas)
	df.rename(columns={"max": "high", "min": "low"}, inplace=True)
	
	return df
	
def MovAvarDev(df, periods = 20):
	
	src = TA.SSMA(df, periods)
	
	calc = df.iloc[-1]['close'] - src.iloc[-1]

	return calc, 'green' if calc >= (df.iloc[-2]['close'] - src.iloc[-2]) else 'red'
	
def entrada(par, dir, timeframe):
	global API
	global valor
	global soros
	global nivelsoros
	global entradaI
	global payminima
	global derrotas
	global BANCAINICIAL
	global sorogale

	os.system('cls' if os.name == 'nt' else 'clear')
	print(f'\n Abrindo operação {par} - {valor}')
	payout = API.get_digital_payout(par)
	if payout < payminima:
		print(f"Recuzando entrada, payout ta menos de {payminima}%")
		pass
	else:	
		status, id = API.buy_digital_spot_v2(par, valor, dir, timeframe)
		
		if status:
			
			status = False
			while status == False:
				status, lucro = API.check_win_digital_v2(id)
				
			if lucro > 0:
				nivelsoros += 1
				if nivelsoros > soros and soros > 0:
					valor = entradaI
					derrotas = 0
					os.system('cls' if os.name == 'nt' else 'clear')
					print('WIN ✅, LUCRO DE', round(lucro, 2))
					print(f"Payout de: {payout}%")
					print(f"Soros nivel {soros} concluido!")
					print(f"Reiniciando entradas para R$: {valor}")


				elif nivelsoros >= soros and soros == 0:
					valor = entradaI
					nivelsoros = 0
					derrotas = 0
					os.system('cls' if os.name == 'nt' else 'clear')
					print('WIN ✅, LUCRO DE', round(lucro, 2))
					print(f"Payout de: {payout}%")
					

				else:	
					valor = round((valor + lucro), 2)
					os.system('cls' if os.name == 'nt' else 'clear')
					print('WIN, LUCRO DE', round(lucro, 2))
					saldo = round((float(round(banca(), 2)) - float(round(BANCAINICIAL, 2)) / 2), 2)
					print(f"Payout de: {payout}%")
					print(f"soro nivel {nivelsoros} ativado!")
					print(f"Proxima entrada será de R$: {valor}")
					
				

			else:
				if sorogale:
					os.system('cls' if os.name == 'nt' else 'clear')
					print('LOSS ❌, PERCA DE', round(lucro, 2))
					derrotas += 1
					if derrotas > 5:
						valor = entradaI
						print(f"Payout de: {payout}%")
						print(f"Reiniciando entradas para RS: {entradaI}")
						nivelsoros = 0
						derrotas = 0
					else:
						valor = abs((float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))) / 2)
						print(f"Payout de: {payout}%")
						print(f"Proxima entrada será RS: {entradaI}")
				else:
					os.system('cls' if os.name == 'nt' else 'clear')
					print('LOSS ❌, PERCA DE', round(lucro, 2))
					valor = abs((float(round(banca(), 2)) - float(round(BANCAINICIAL, 2))) / 2)
					print(f"Payout de: {payout}%")
					print(f"Proxima entrada será RS: {entradaI}")

					
				
			
			
		else:
			print('Erro ao abrir operação\n', id)
		
		print('\n')
	
par = ""
timeframe = 0
valor = 0
entradaI = 0
soros = 0
nivelsoros = 0
payminima = 0
payout = ""	
sorogale = True


def configurar():
	global par
	global timeframe
	global valor
	global entradaI
	global soros
	global nivelsoros
	global payminima
	global payout
	global sorogale


	
	par = input("Digite a moeda: ")
	par = par.upper()
	timeframe = input("Digite o tempo da vela: ")
	timeframe = int(timeframe)
	valor = input("Digite o valor de entrada: ").replace(",",".")
	valor = float(valor)
	entradaI = valor
	soros = input("Quantidade de soros: ")
	soros = int(soros)
	nivelsoros = 0
	payminima = input("Digite a payout minima para entrar: ")
	payminima = int(payminima)
	Tsorogale = input("Deseja fazer sorogale?:\n1 = SIM\n2 = NÃO\n\nDigite o numero: ")
	Tsorogale = int(Tsorogale)
	if Tsorogale == 1:
		sorogale = True
	else:
		sorogale = False

	try:
		payout = API.get_digital_payout(par)
	except:
		os.system('cls' if os.name == 'nt' else 'clear')
		print("você digitou a moeda de forma incorreta, tente novamente.")
		print("não use / nem - , somente o nome por exemplo eurusd ou EURUSD.")
		configurar()
	
	if int(payout) < int(payminima):
		os.system('cls' if os.name == 'nt' else 'clear')
		print(f"a payout atual da {par} é de {payout}%\nescolha outra moeda ou espera a payout aumentar para {payminima}%")
		configurar()	
	
	

configurar()


print('\n')
os.system('cls' if os.name == 'nt' else 'clear')
while True:
	saldo = round((float(round(banca(), 2)) - float(round(BANCAINICIAL, 2)) / 2), 2)
	df = get_data(par, timeframe, 200,)
	
	taxa, color = MovAvarDev(df, 20)
	ssma_3 = TA.SSMA(df, 3)
	ssma_50 = TA.SSMA(df, 50)
	
	if ssma_3.iloc[-1] <= ssma_50.iloc[-1] and ssma_3.iloc[-2] > ssma_50.iloc[-2] and color == 'red':
		entrada(par, 'put', timeframe)
	
	elif ssma_3.iloc[-1] >= ssma_50.iloc[-1] and ssma_3.iloc[-2] < ssma_50.iloc[-2] and color == 'green':
		entrada(par, 'call', timeframe)
		
		
	print(f"[{ datetime.now().strftime('%H:%M:%S') }]:: Aguardando {par}, Saldo: R$: {saldo}", end='\r')
	
	
