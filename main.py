from urllib.request import urlopen
from bs4 import BeautifulSoup 
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
from concessao import Concessao

def scrap_main_page_antt():
    url = 'https://www.gov.br/antt/pt-br/assuntos/rodovias/concessionarias/lista-de-concessoes'
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'lxml')

    concessoes_elems = bs.find('div', {'class': 'wrapper'}).find_all('div')

    concessoes_list = []

    for element in concessoes_elems:
        a_element = element.find('a')
        if a_element:
            url = a_element['href']
            titulo = a_element.find('span', {'class': 'front'}).find('span', {'class': 'titulo'}).text
            descricao = a_element.find('span', {'class': 'back'}).find('span', {'class': 'descricao'}).text
            
            concessoes_list.append(Concessao(url=url, titulo=titulo, descricao=descricao))
                
    return concessoes_list

concessoes_list = scrap_main_page_antt()

for concessao in concessoes_list:
    concessao.extrair_dados_concessao()
    
print('')