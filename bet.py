import requests
from bs4 import BeautifulSoup
import json

url = 'https://catalogador.ml/api/porcentagemGale2/M1'

class_list = set()
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
List_Hora = []
List_Data = []
List_Casa = []
List_Fora = []
List_Tip = []
List_Dica = []

todos = json.loads(page.content)

par01 = todos['Todos'][0]
percent = par01[0]
par = par01[1]
padrao = par01[2]
per = par01[3]
taxa = per[1]
print(taxa)


    

