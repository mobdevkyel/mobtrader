#!/bin/bash
#Criado por: Ezequiel - 2021
###
echo "instalador Mobtrader BOT"
echo
pkg install python
pkg install git
pkg install wget
git clone https://github.com/mobdevkyel/mobtrader
cd mobtrader
pip install requirements.txt
python mobtrader.py