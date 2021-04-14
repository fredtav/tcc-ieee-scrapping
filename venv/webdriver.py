from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import os
from os import path
import csv
import json
import pandas

class artigo() :
    def __init__(self, seq, lan, abstract, title, pages, key_words):
        self.seq = seq
        self.lan = lan
        self.abstract = abstract
        self.title = title
        self.pages = pages
        self.key_words = key_words

class autor() :
    def __init__(self, article, authorFirstname, authorMiddlename, authorLastname, authorAffiliation, authorCountry, authorEmail, orcid):
        self.article = article
        self.authorFirstname = authorFirstname
        self.authorMiddlename = authorMiddlename
        self.authorLastname = authorLastname
        self.authorAffiliation = authorAffiliation
        self.authorCountry = authorCountry
        self.authorEmail = authorEmail
        self.orcid = orcid

def salvar_autores(lista_autores):
    filename = "C:\\Users\\Fred\\Desktop\\TCC\\arquivo2.csv"
    try:
        with open(filename, mode='a') as arquivo:
            field_names = ['article', 'authorFirstname', 'authorMiddlename', 'authorLastname', 'authorAffiliation',
                           'authorAffiliationEn', 'authorCountry', 'authorEmail', 'orcid', 'authorBio', 'authorBioEn']
            writer = csv.writer(arquivo, delimiter=';', lineterminator='\n')
            if os.stat(filename).st_size == 0:
                writer.writerow(field_names)
            for aut in lista_autores:
                writer.writerow([aut.article, aut.authorFirstname, aut.authorMiddlename, aut.authorLastname,
                                 aut.authorAffiliation, aut.authorCountry, aut.authorEmail, aut.orcid])
            arquivo.close()
    except BaseException as e:
        print('Excecao: ', filename)

def monta_obj_artigo(seq, link, strPag):
    driver.get(link)
    pagina = strPag.split(":")
    num_pag = pagina[1].split("-")
    qtd_pag = int(num_pag[1].strip()) - int(num_pag[0].strip()) + 1 # removendo espacos em branco
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, 'document-title')))
    resumo = driver.find_element_by_class_name('abstract-text.row')
    print("Abstract: ", resumo.text)
    titulo = driver.find_element_by_class_name("document-title")
    print("Titulo: ", titulo.text)

    keys = driver.find_elements_by_xpath('//*[@id="keywords"]/xpl-document-keyword-list/section/div/ul/li/ul')
    chaves = str("")
    for k in keys:
        chaves = chaves + str(k.text) + ","

    chaves = chaves[: chaves.__len__() - 1]
    print(chaves)
    a = artigo(seq, 'EN', resumo.text, titulo.text, qtd_pag, chaves)

    new_link = link.replace('keywords#keywords','authors#authors')
    driver.get(new_link)

    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,
                                                                     '//*[@id="authors"]/div[1]/xpl-author-item/div/div/div/div[1]/a')))
    autores = driver.find_elements_by_xpath('//*[@id="authors"]/div/xpl-author-item/div/div/div/div[1]/a')
    filiacoes = driver.find_elements_by_xpath('//*[@id="authors"]/div/xpl-author-item/div/div/div/div[2]/div')

    monta_obj_autor(seq, autores, filiacoes)
    return a

def monta_obj_autor(seq, autores, filiacoes):

    lista_autores = []
    for i in range(autores.__len__()):
        nome_autor = autores[i].text.split(' ')
        primeiro_nome = nome_autor[0]
        ultimo_nome = nome_autor[nome_autor.__len__() - 1]
        nome_meio = ""
        ran = int(nome_autor.__len__() - 2)
        for j in range(0, ran):
            nome_meio = nome_meio + nome_autor[j+1] + " "
        nome_meio = nome_meio.strip()
        filiacao = filiacoes[i].text
        texto = filiacao.split(',')
        country = ""
        if texto.__len__() > 1:
            country = texto[texto.__len__()-1].strip()  ## pode ser que mude
        filiacao = texto[0]

        aut = autor(seq, primeiro_nome, nome_meio, ultimo_nome, filiacao, country, '', '')
        lista_autores.append(aut)

    salvar_autores(lista_autores)


def salvar_artigos(lista_artigos):
    filename = "C:\\Users\\Fred\\Desktop\\TCC\\arquivo.csv"
    try:
        with open(filename, 'w') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['seq','lan','abstract','title','pages','keyWords'])
            for art in lista_artigos:
                writer.writerow([art.seq, art.lan, art.abstract.encode("utf-8"), art.title, art.pages, art.key_words.encode("utf-8")])
            f.close()
    except BaseException as e:
        print('Excecao: ', filename)

def pegar_links_artigos(link_simposio):
    quant = driver.find_element_by_xpath('//*[@id="publicationIssueMainContent"]/div[1]/xpl-issue-search-dashboard/div/div[2]/div[1]/div/div/span[1]/span[2]')
    print(quant.text)

    total_artigos = int(quant.text) // 25
    if int(quant.text) % 25 > 0:
        total_artigos = total_artigos + 1

    print(total_artigos)

    # pegar links da primeira pagina

    # artigos = driver.find_elements_by_xpath('//*[@id="publicationIssueMainContent"]/div[2]/div/div[2]/div/xpl-issue-results-list/div[2]/div')

    artigos = driver.find_elements_by_xpath('//div/xpl-issue-results-items/div[1]/div[2]/ul/li[2]/xpl-view-html/div/a')
    quant_artigos = artigos.__len__()

    paginas = driver.find_elements_by_xpath('//*[@id="publicationIssueMainContent"]/div[2]/div/div[2]/div/xpl-issue-results-list/div[2]/div/div/xpl-issue-results-items/div[1]/div[1]/div[2]/div/div/span[3]')
    quant_paginas = paginas.__len__()
    corte = quant_paginas - quant_artigos
    print(corte)
    print(paginas)

    nova_lista_artigos = []
    k = 0

    lista_links = []
    lista_paginas = []

    for art in artigos:

        link_artigo = art.get_attribute('href')
        lista_links.append(str(link_artigo + "keywords#keywords"))
        print(link_artigo)
        pag = paginas[k + corte].text
        lista_paginas.append(pag)
        print(pag)
        k = k + 1


    # for para pegar links a partir da segunda pagina
    for i in range(total_artigos - 1):
        pag = i + 2
        url = link_simposio + "?pageNumber=" + str(pag)
        print(url)
        driver.get(url)
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="publicationIssueMainContent"]/div[1]/xpl-issue-search-dashboard/div/div[2]/div[1]/div/div/span[1]/span[2]')))
        artigos = driver.find_elements_by_xpath('//div/xpl-issue-results-items/div[1]/div[2]/ul/li[2]/xpl-view-html/div/a')
        quant_artigos = artigos.__len__()
        k = 0
        paginas = driver.find_elements_by_xpath(
            '//*[@id="publicationIssueMainContent"]/div[2]/div/div[2]/div/xpl-issue-results-list/div[2]/div/div/xpl-issue-results-items/div[1]/div[1]/div[2]/div/div/span[3]')
        quant_paginas = paginas.__len__()
        corte = quant_paginas - quant_artigos


        for art in artigos:
            # artigo = art.find_element_by_xpath('/div/xpl-issue-results-items/div[1]/div[1]/div[2]/h2/a')
            print(art.get_attribute('href'))
            link_artigo = art.get_attribute('href')
            lista_links.append(str(link_artigo + "keywords#keywords"))
            pag = paginas[k + corte].text
            print(pag)
            lista_paginas.append(pag)
            k = k + 1

    k = 0
    for i in range(lista_links.__len__()):
        obj_artigo = monta_obj_artigo(k + 1, lista_links[k], lista_paginas[k])
        nova_lista_artigos.append(obj_artigo)
        k = k + 1

    print("Pegou todos os artigos")
    salvar_artigos(nova_lista_artigos)



chrome_options = Options()

# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")

# Caminho relativo, preciso revisar
basepath = path.dirname(__file__)
parent_dir = path.abspath(path.join(basepath, os.pardir))
filepath = path.abspath(path.join(parent_dir, "chromedriver.exe"))
print(filepath)
driver = webdriver.Chrome(executable_path=filepath, options=chrome_options)

start_url = "https://ieeexplore.ieee.org/xpl/conhome/1000131/all-proceedings"
driver.get(start_url)
driver.maximize_window()
print(driver.page_source.encode("utf-8"))

WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'conference-records')))
# conferences = driver.find_elements_by_xpath('//*[@id="LayoutWrapper"]/div/div/div/div[4]/div/xpl-root/div/xpl-xpl-delegate/xpl-conference-home/div/div[1]/div[3]/div/section/xpl-conference-toc/div[1]/div[2]/div/xpl-conference-all-proceedings/div/div/div[2]/ul/li')
conferences = driver.find_elements_by_class_name('conference-records')
list_conferences_string = '//*[@id="LayoutWrapper"]/div/div/div/div[3]/div/xpl-root/div/xpl-xpl-delegate/xpl-conference-home/div/div[1]/div[3]/div/section/xpl-conference-toc/div[1]/div[2]/div/xpl-conference-all-proceedings/div/div/div[2]/ul/li'
list_conferences = driver.find_elements_by_xpath(list_conferences_string)

lista_artigos = []

i = 1
for conference in list_conferences:
    s = list_conferences_string + '[' + str(i) + ']/a'
    lista_artigos.append(driver.find_element_by_xpath(s).get_attribute('href'))
    i = i + 1


print("teste")
# proceeding_url = "https://ieeexplore.ieee.org/xpl/conhome/8094486/proceeding"
# driver.get(proceeding_url);
#
# WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="publicationIssueMainContent"]/div[2]/div/div[2]/div/xpl-issue-results-list/div[2]')))
# publicacoes = driver.find_elements_by_xpath('//*[@id="publicationIssueMainContent"]/div[2]/div/div[2]/div/xpl-issue-results-list/div[2]/div')

"""Entrando no evento"""
artigo_url = str(lista_artigos[0])
driver.get(artigo_url)

WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="publicationIssueMainContent"]/div[1]/xpl-issue-search-dashboard/div/div[2]/div[1]/div/div/span[1]/span[2]')))

pegar_links_artigos(artigo_url)

driver.quit()
exit()

WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="LayoutWrapper"]/div/div/div/div[5]/div/xpl-root/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[3]/div[1]/div/div/div')))
resumo = driver.find_element_by_xpath('//*[@id="LayoutWrapper"]/div/div/div/div[5]/div/xpl-root/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[3]/div[1]/div/div/div')

#resumo_div = resumo.find_elements_by_xpath('//xpl-document-abstract/section/div[3]/div[1]/div/div/div')

resumo_texto = resumo.text

#resumao = resumo

print(resumo_texto)

#autores
#autores = driver.find_elements_by_class_name('authors-info')

# autores2 = driver.find_element_by_id('authors-header')

# ActionChains(driver).move_to_element(autores2).click()
#autores2.click()

artigo_url = artigo_url + "/authors#authors"
driver.get(artigo_url)


WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'authors-accordion-container')))

list_autores = driver.find_elements_by_class_name('authors-accordion-container')

nome_autor = list_autores[0].find_element_by_xpath('//div/div/div/div/a')
filiacao_autor = list_autores[0].find_element_by_xpath('//div/div/div/div/div')

for autor in list_autores:
    autor_texto = str.splitlines(autor.text)
    autor_nome = autor_texto[0]
    autor_filiacao = autor_texto[1]
    print(autor_nome)
    print(autor_filiacao)
    autor_link = autor.find_elements_by_tag_name('a')[0].get_attribute('href')
    print(autor_link)



# Vai ser usado para pegar o link para a Bio do author ;)
# list_autores[0].find_elements_by_tag_name('a')[0].get_attribute('href')


driver.quit()