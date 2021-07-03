#!/bin/bash
echo "Opa!!!"
clear
then
    Menu() {
        clear
        
        echo "=========================="
        echo "     Mobtrader BOT    "
        echo "=========================="
        echo "Escolha sua opção"
        echo "__________________________"
        echo "[ 1 ] | Criar cadastro"
        echo "[ 2 ] | Fazer instalação"
        echo "[ 3 ] | Atualizar"
        echo "[ 4 ] | Iniciar"
        echo "[ 5 ] | Deletar Bot"
        echo "[ 0 ] | SAIR"
        echo -e '\n'
        echo "Escolha um numero"
        read App
        case $App in
        1) App1 ;;
        2) App2 ;;
        3) App3 ;;
        4) App4 ;;
        5) App5 ;;
        0) Sair ;;
        *) "Calma !!!" ; echo ; Menu;;
        esac
        }

    App1 () {
    clear
    echo "Em construção"
    Menu
    }
    App2 () {
    clear
    then
        cd
        #Install common tools
        pkg install python curl git -y
        #Update pip
        python -m pip install --upgrade pip
        #Install requests
        pip install requests
        #Install websocket
        pip install websocket-client==0.56
        #Install bs4
        pip install bs4
        #Install colorama
        pip install colorama
        #Install pandas
        pip install pandas
        #Install numpy
        pip install numpy
        #Install csv
        pip install csv
        #Baixar Bot
        git clone https://github.com/mobdevkyel/mobtrader
        clear
        Menu
        
    }
    App3 () {
    clear
    cd
    rm -R mobtrader - y
    git clone https://github.com/mobdevkyel/mobtrader
    Menu
    }
    App4 () {
    clear
    cd
    cd mobtrader
    python mobtrader.py
    }
    App5 () {
    clear
    cd
    rm -R mobtrader - y
    Menu
    }

    Voltar() {
    clear
    Menu
    }

    Sair() {
    clear
    exit
    }
    clear
    Menu
fi