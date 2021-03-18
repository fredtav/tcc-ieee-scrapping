from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import os
from os import path
import csv


def salvar_autor():
    with open('Autores.csv', mode='w') as arquivo:
        field_names = ['article','authorFirstname','authorMiddlename','authorLastname','authorAffiliation','authorAffiliationEn','authorCountry','authorEmail','orcid','authorBio','authorBioEn']
        writer = csv.writer()


def salvar_artigo():
    with open('Artigos.csv', mode='w') as arquivo:
        field_names = ['seq', 'language', 'sectionAbbrev', 'title',
                       'abstract', 'keywords', 'orcid', 'pages', 'fileLabel', 'fileLink']
        writer = csv.writer()

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
    for art in artigos:
        # artigo = art.find_element_by_xpath('/div/xpl-issue-results-items/div[1]/div[1]/div[2]/h2/a')
        print(art.get_attribute('href'))
        # print(artigo.text)


    # for para pegar links a partir da segunda pagina
    for i in range(total_artigos - 1):
        pag = i + 2
        url = link_simposio + "?pageNumber=" + str(pag)
        print(url)
        driver.get(url)
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="publicationIssueMainContent"]/div[1]/xpl-issue-search-dashboard/div/div[2]/div[1]/div/div/span[1]/span[2]')))
        artigos = driver.find_elements_by_xpath('//div/xpl-issue-results-items/div[1]/div[2]/ul/li[2]/xpl-view-html/div/a')
        for art in artigos:
            # artigo = art.find_element_by_xpath('/div/xpl-issue-results-items/div[1]/div[1]/div[2]/h2/a')
            print(art.get_attribute('href'))


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