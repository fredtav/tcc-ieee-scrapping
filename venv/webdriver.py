from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os
from os import path
from pathlib import Path
import csv
import time
import logging
import sys


class Artigo:
    def __init__(self, seq, lan, abstract, title, pages, key_words):
        self.seq = seq
        self.lan = lan
        self.abstract = abstract
        self.title = title
        self.pages = pages
        self.key_words = key_words


class Autor:
    def __init__(self, article, authorFirstname, authorMiddlename, authorLastname, authorAffiliation, authorCountry):
        self.article = article
        self.authorFirstname = authorFirstname
        self.authorMiddlename = authorMiddlename
        self.authorLastname = authorLastname
        self.authorAffiliation = authorAffiliation
        self.authorCountry = authorCountry
        self.authorBio = ""


def salvar_autores(lista_autores):
    # filename = "C:\\Users\\Fred\\Desktop\\TCC\\arquivo_autores.csv"
    filename = folder_base_path + "/arquivo_autores.csv"
    try:
        with open(filename, mode='a') as arquivo:
            field_names = ['article', 'authorFirstname', 'authorMiddlename', 'authorLastname', 'authorAffiliation',
                           'authorCountry', 'authorBio']
            writer = csv.writer(arquivo, delimiter=';', lineterminator='\n')
            if os.stat(filename).st_size == 0:
                writer.writerow(field_names)
            for aut in lista_autores:
                writer.writerow([aut.article, aut.authorFirstname, aut.authorMiddlename, aut.authorLastname,
                                 aut.authorAffiliation, aut.authorCountry, aut.authorBio])
            arquivo.close()
            logging.info("Arquivo de autores salvo")
    except BaseException as e:
        print(e)
        logging.error(e)


def monta_obj_artigo(seq, link, strPag):
    driver.get(link)
    pagina = strPag.split(":")
    if pagina.__len__() > 1:
        num_pag = pagina[1].split("-")
        if num_pag.__len__() > 1:
            qtd_pag = int(num_pag[1].strip()) - int(num_pag[0].strip()) + 1  # removendo espacos em branco
        else:
            qtd_pag = 1
    else:
        qtd_pag = ""

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
    a = Artigo(seq, 'EN', resumo.text, titulo.text, qtd_pag, chaves)

    new_link = link.replace('keywords#keywords','authors#authors')
    driver.get(new_link)

    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH,
                                                                     '//*[@id="authors"]')))
    try:
        obj_autores = driver.find_elements_by_xpath('//*[@id="authors"]/div/xpl-author-item/div/div/div')
        autores = driver.find_elements_by_xpath('//*[@id="authors"]/div/xpl-author-item/div/div/div/div[1]/a')
        filiacoes = driver.find_elements_by_xpath('//*[@id="authors"]/div/xpl-author-item/div/div/div/div[2]/div')
    except Exception as e:
        print(e)
        autores = driver.find_elements_by_xpath('//*[@id="authors"]/div/xpl-author-item/div/div/div/div[1]/xpl-modal/a')
        filiacoes = driver.find_elements_by_xpath('//*[@id="authors"]/div/xpl-author-item/div/div/div/div[2]/div')

    # monta_obj_autor(seq, autores, filiacoes)
    monta_obj_autor(seq, obj_autores)
    return a


def monta_obj_autor(seq, obj_autores):

    lista_autores = []
    lista_link_autores = []
    for aut in obj_autores:
        country = ""
        try:
            autor = aut.find_element_by_xpath("div[1]/a")
        except Exception as e:
            print(e)
            autor = aut.find_element_by_xpath("div[1]/xpl-modal/a")
        nome_autor = autor.text.split(' ')
        primeiro_nome = nome_autor[0]
        ultimo_nome = nome_autor[nome_autor.__len__() - 1]
        nome_meio = ""
        ran = int(nome_autor.__len__() - 2)
        for j in range(0, ran):
            nome_meio = nome_meio + nome_autor[j+1] + " "
        nome_meio = nome_meio.strip()
        try:
            filiacoes = aut.find_element_by_xpath("div[2]/div")
            filiacao = filiacoes.text
            texto = filiacao.split(',')
            if texto.__len__() > 1:
                country = texto[texto.__len__() - 1].strip()  ## pode ser que mude
                filiacao = filiacao.replace(", " + str(country), "")
            else:
                filiacao = texto[0]
        except Exception as e:
            print(e)
            filiacao = ""
        link_autor = autor.get_attribute('href')
        lista_link_autores.append(link_autor)
        aut = Autor(seq, primeiro_nome, nome_meio, ultimo_nome, filiacao, country)
        lista_autores.append(aut)

    for i in range(lista_link_autores.__len__()):
        try:
            driver.get(lista_link_autores[i])
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,
                                                                             '//*[@id="authorProfile"]/div[3]/div[1]/div/div[2]/div[1]')))
            # driver.find_element_by_xpath('//*[@id="authorProfile"]/div[3]/div[1]/div/div[2]/div[2]/span[2]/a').click()
            bio = driver.find_element_by_xpath('//*[@id="authorProfile"]/div[3]/div[1]/div/div[2]/div[2]/span[1]')
            print(bio.text)
            lista_autores[i].authorBio = bio.text
        except Exception as e:
            print(e)

    salvar_autores(lista_autores)


def salvar_artigos(lista_artigos):
    filename = folder_base_path + "/arquivo_artigos.csv"
    global quantidade_artigos
    quantidade_artigos = quantidade_artigos + lista_artigos.__len__()
    try:
        with open(filename, 'w') as f:
            writer = csv.writer(f, delimiter=';', lineterminator='\n')
            writer.writerow(['seq','lan','title','pages','keyWords','abstract'])
            for art in lista_artigos:
                key_w = art.key_words.replace("\n", "")
                abst = art.abstract.replace("Abstract:\n", "")
                writer.writerow([art.seq, art.lan, art.title, art.pages, key_w.encode("utf-8"), abst.encode("utf-8")])
            f.close()
            logging.info("Arquivo de artigos salvo")
    except BaseException as e:
        print(e)
        logging.error(e)


def pegar_links_artigos(link_simposio):
    quant = driver.find_element_by_xpath('//*[@id="publicationIssueMainContent"]/div[1]/xpl-issue-search-dashboard/div/div[2]/div[1]/div/div/span[1]/span[2]')
    print(quant.text)

    total_artigos = int(quant.text) // 25
    if int(quant.text) % 25 > 0:
        total_artigos = total_artigos + 1

    print(total_artigos)

    # pegar links da primeira pagina
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


logging.basicConfig(format='%(asctime)s %(message)s', filename='scrapper.log', level=logging.INFO)
logging.info('Início da execução')

start_time = time.time()
chrome_options = Options()

# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")

# Caminho relativo, preciso revisar
basepath = path.dirname(__file__)
parent_dir = path.abspath(path.join(basepath, os.pardir))
filepath = path.abspath(path.join(parent_dir, "chromedriver.exe"))
print(filepath)
driver = webdriver.Chrome(executable_path=filepath, options=chrome_options)

folder_base_path = path.dirname(__file__) + "/arquivos"
Path(folder_base_path).mkdir(parents=True, exist_ok=True)

if sys.argv.__len__() > 1:
    artigo_url = str(sys.argv[1])
else:
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


    """Entrando no evento"""
    artigo_url = str(lista_artigos[0])
try:
    driver.get(artigo_url)
except Exception as e:
    logging.error(e)
    exit(1)
WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="publicationIssueMainContent"]/div[1]/xpl-issue-search-dashboard/div/div[2]/div[1]/div/div/span[1]/span[2]')))

quantidade_artigos = 0
pegar_links_artigos(artigo_url)

driver.quit()
print("--- %s seconds ---" % (time.time() - start_time))
print("para %s " % quantidade_artigos)
logging.info('Fim da execução')
exit()
