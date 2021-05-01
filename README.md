  # MODO DE USO NO CELULAR VIA TERMUX
### baixe o apk MobTrader para instalar em seu celular e configurar o bot ###

https://github.com/mobdevkyel/mobtrader/raw/main/MobTrader.apk

### baixe o apk Termux para instalar em seu celular e iniciar o bot###

https://play.google.com/store/apps/details?id=com.termux&hl=pt_BR&gl=US

### COMO FAZER INSTALAÇÃO PELO APK TERMUX ###

pkg install python

pkg install git

git clone https://github.com/mobdevkyel/mobtrader

cd mobtrader

pip install requests

pip install websocket-client==0.56

pip install bs4

python mobtrader.py

### COMO INICIAR ###

cd mobtrader

python mobtrader.py

### COMO ATUALIZAR ###
cd

rm -R mobtrader

git clone https://github.com/mobdevkyel/mobtrader

cd mobtrader

python mobtrader.py

![image](https://user-images.githubusercontent.com/79609322/113521180-271bb300-956e-11eb-9dc8-171970933fc0.png)
