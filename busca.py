
from selenium import webdriver

import time, os

def catalogar():
    URL = 'https://catalogador.ml/'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    # OR options.add_argument("--disable-gpu")
    
    os.environ['MOZ_HEADLESS'] = '1'
    browser = webdriver.Chrome("navegador/chromedriver", chrome_options=options)
    #browser = webdriver.Chrome('chromedriver', chrome_options=options)


    browser.get(URL)
    time.sleep(15)

    texto = browser.find_element_by_xpath('/html/body/main').text
    lista = [texto]
    lista2 = []
    for i in lista:
        dados = str(i).split('\n')
        paridade = dados[0]
        padrao = dados[1]
        porcentagem = dados[2].replace("%", "")
        dv1 = dados[4].split(' ')
        dv2 = dados[5].split(' ')
        WIN = dv1[0]
        G1 = dv1[1]
        G2 = dv1[2]
        HIT = dv1[3]
        win = dv2[0]
        g1 = dv2[1]
        g2 = dv2[2]
        hit = dv2[3]

        Melhor = paridade, padrao, porcentagem, WIN, G1, G2, HIT, win, g1, g2, hit
        #print(Melhor)

    return paridade, padrao, porcentagem, WIN, G1, G2, HIT, win, g1, g2, hit

