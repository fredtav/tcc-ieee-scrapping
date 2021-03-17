import os
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from pathlib import Path
from bs4 import BeautifulSoup
import logging

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    logging.error(e)

logging.basicConfig(format='%(asctime)s %(message)s', filename='scrapper.log', level=logging.DEBUG)
logging.info('Teste')


"""
Pegando a lista de eventos de simpósio
"""
#html = simple_get("https://ieeexplore.ieee.org/xpl/conhome/1000131/all-proceedings")
html = simple_get("https://ieeexplore.ieee.org/xpl/conhome/8094486/proceeding")

res = BeautifulSoup(html,"html.parser")

#divs = res.findAll('div', class_="issue-list-container col")
divs = res.findAll("a")
for div in divs:
    tituloconf = div.findAll('a')
    print("\nExtracting metadata for the proceedings of: "+tituloconf)