#!/bin/bash
#Criado por: Ezequiel - 2021
###
echo "Iniciar Mobtrader BOT"
echo
cd mobtrader
wget https://github.com/mobdevkyel/mobtrader/blob/main/mobtrader.py
wget https://github.com/mobdevkyel/mobtrader/blob/main/busca.py
wget https://github.com/mobdevkyel/mobtrader/blob/main/melhor_payout_par.py
wget https://github.com/mobdevkyel/mobtrader/blob/main/bet.py
python mobtrader.py
