from iqoptionapi.stable_api import IQ_Option
from finta import TA # pip install finta
from time import sleep, time
from datetime import datetime
import pandas as pd

API = IQ_Option('login', 'senha')
API.connect()

API.change_balance('PRACTICE') # PRACTICE / REAL

if API.check_connect():
	print(' Conectado com sucesso!')
else:
	print(' Erro ao conectar')
	input('\n\n Aperte enter para sair')
	exit()

def entrada(par, dir, valor, timeframe):
	global API
	
	print(f"\n [{datetime.now().strftime('%H:%M:%S')}] Abrindo operação em {par} - {dir} - {timeframe}")
	
	status, id = API.buy_digital_spot_v2(par, valor, dir, timeframe)
	
	if status:
		
		status = False
		while status == False:
			status, lucro = API.check_win_digital_v2(id)
		
		
		if lucro > 0:
			print(f'\n WIN, LUCRO DE {lucro}\n')
		else:
			print(f'\n LOSS, PERCA DE {lucro}\n')
		
		
	else:
		print('Erro ao abrir operação!', id)
	
pares = ['EURUSD', 'AUDCAD', 'EURJPY', 'NZDUSD']

timeframe = 1
valor_entrada = 10


while True:
	
	for par in pares:
		
		print(f" [{datetime.now().strftime('%H:%M:%S')}] Analisando {par}..", end='\r')
	
		velas = API.get_candles(par, 60, 200, time())
		
		df = pd.DataFrame(velas)
		df.rename(columns={'max': 'high', 'min': 'low'}, inplace=True)
		
		upper, _, lower = TA.BBANDS(df, period=20, std_multiplier=2.5).iloc[-1]
		
		rsi6 = TA.RSI(df, 6).iloc[-1] # 90 / 10
		rsi10 = TA.RSI(df, 10).iloc[-1] # 90 / 7
		
		cores = ['g' if velas[i]['open'] < velas[i]['close'] else 'r' if velas[i]['open'] > velas[i]['close'] else 'e' for i in [-1, -2, -3]]
		
		# Velas verdes
		if cores.count('g') == 3:
			
			# Analise da Bandas de Bollinger
			if velas[-1]['close'] >= upper:
				
				# Analise dos RSI's
				if rsi6 >= 90 and rsi10 >= 90:
					entrada(par, 'put', valor_entrada, timeframe)					
		
		# Velas Vermelhas
		if cores.count('r') == 3:
			
			# Analise da Bandas de Bollinger
			if velas[-1]['close'] <= lower:
				
				# Analise dos RSI's
				if rsi6 <= 10 and rsi10 <= 7:
					entrada(par, 'call', valor_entrada, timeframe)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	