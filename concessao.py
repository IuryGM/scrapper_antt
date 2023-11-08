from bs4 import BeautifulSoup
from urllib.request import urlopen

class Concessao:
    
    def __init__(self, url, descricao, titulo):
        self.__url = url
        self.__descricao = descricao
        self.__titulo = titulo
        self.__url_localizacao_pedagios = ''
        self.__url_tarifas = ''
        
    @property
    def url(self) -> str:
        return self.__url
    
    @property
    def descricao(self) -> str:
        return self.__descricao
    
    @property
    def titulo(self) -> str:
        return self.__titulo
    
    def extrair_dados_concessao(self):
        self.__extrair_dados_pagina_concessao()
        self.__extrair_pagina_tarifas_concessao()
    
    def __extrair_dados_pagina_concessao(self):
        html = urlopen(self.__url)
        bs = BeautifulSoup(html.read(), 'lxml')
        
        content_rows = bs.find('div', {'id': 'content'}).findChildren('div', recursive=False)        
        self.__nome = content_rows[0].find('h2').text

        elements_p_list = content_rows[1].find_all('p')

        self.__extrair_dados_gerais_concessao(elements_p_list)

        wrapper_dados_pedagio = content_rows[3].find('div', {'class': 'wrapper'})
    
        self.__extrair_urls_dados_praca(wrapper_dados_pedagio)
    
    def __extrair_dados_gerais_concessao(self, elements_p_list):
        self.__dados_gerais = {}
                
        for dados_element in elements_p_list:
            str_splitted = dados_element.text.replace('\xa0', ' ').split(': ')
            key, value = str_splitted[0], str_splitted[-1]
            self.__dados_gerais[key] = value        
            
    def __extrair_urls_dados_praca(self, element_wrapper):
        for element in element_wrapper.find_all('div', {'class': 'card great-cards'}):
            element_a = element.find('a', {'class': 'govbr-card-content'})
            text = element_a.find('span', {'class': 'titulo'}).text 
            if 'Localização' in text:
                self.__url_localizacao_pedagios = element_a['href']
            elif 'Tarifas' in text:
                self.__url_tarifas = element_a['href']
                
    def __extrair_pagina_tarifas_concessao(self):
        if self.__url_tarifas == '':
            return None
        
        self.__dados_tarifas = {}
        
        html = urlopen(self.__url_tarifas)
        bs = BeautifulSoup(html.read(), 'lxml')
        
        content_core = bs.find('div', {'id': 'content-core'})
                        
        # self.__extrair_pracas_concessao(content_core)
        
        self.__extrair_valores_tarifas_concessao(content_core)
        
    def __extrair_pracas_concessao(self, content_core_element):
        h3 = content_core_element.find('h3')
        if h3 != None:            
            pracas = h3.text.replace('\xa0', ' ').split(': ')
            self.__dados_tarifas[pracas[0]] = pracas[1].split(', ')
        
    def __extrair_valores_tarifas_concessao(self, content_core_element):
        table = content_core_element.find('table')
        
        if table == None:
            return
        
        table_rows = table.find_all('tr')
        
        atributos = [p.text for p in table_rows[0].find_all('p')]
        
        self.__tarifas = []
        
        inicio = 1
            
        p = table_rows[inicio].find('p')
        
        p_text = p.text
        
        if 'Praça' in p_text or 'P' in p_text:
            atributos = atributos[0 : len(atributos) - 1] + [p.text for p in table_rows[inicio].find_all('p')]                
            inicio = 2
        
        for i in range(inicio, len(table_rows)):
            valores = table_rows[i].find_all('p')
            
            row = {}
            
            for j in range(1, len(valores)):
                row[atributos[j]] = valores[j]
            
            self.__tarifas.append(row)