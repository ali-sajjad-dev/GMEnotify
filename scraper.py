import requests
import json
from random import randrange
from fake_useragent import UserAgent
from lxml.html import fromstring
from bs4 import BeautifulSoup

user_agent = UserAgent()
URL = "https://www.gamestop.com/consoles-hardware/playstation-5/consoles/products/sony-playstation-5-console/11108140.html?condition=New"

headers = {
    'User-Agent' : user_agent.random
}

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = []
    for i in parser.xpath('//tbody/tr')[:1000]:
        if i.xpath('.//td[7][contains(text(),"yes")]') and i.xpath('.//td[4][contains(text(),"United States")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.append(proxy)
    return proxies

def parse_HTML(response):
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="add-to-cart")
    value = str(results["data-gtmdata"])
    value_JSON = json.loads(value)
    return value_JSON['productInfo']['availability']

def request_GME(proxies):
    random = randrange(len(proxies))
    proxy = proxies[random]
    try:
        response = requests.get(URL, headers=headers, proxies={'http': 'http://' + proxy, 'https': 'https://' + proxy}, timeout=10)
        if response.status_code == 200:
            availability = parse_HTML(response)
            return availability
    except:
        print('Connection Error with request')
        headers['User-Agent'] = user_agent.random
        return request_GME(proxies)
