#!/bin/bash
#Criado por: Ezequiel - 2021
###
echo "instalador Mobtrader BOT"
echo
chmod +x mobtrader.sh
pkg install git
git clone https://github.com/mobdevkyel/mobtrader
cd mobtrader
pkg install python
pip install requirements.txt
./mobtrader.sh
