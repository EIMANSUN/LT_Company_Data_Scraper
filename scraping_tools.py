import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures
import random

def getProxies():
    '''Scrapes the list of free https proxies from free-proxy-list'''
    URL = 'https://free-proxy-list.net/'
    html = requests.get(URL, timeout=3)
    soup = BeautifulSoup(html.content, 'lxml')

    # Find the first tbody tag and retrieve al tr with data td stored in list
    table = soup.find('tbody')
    rows = [row.find_all('td') for row in table.find_all('tr')]

    # Append a proxy adress to the list if anonimity is 'elite proxy'
    proxy_list = []
    for row in rows:
        if row[4].text == 'elite proxy' and row[6].text == 'yes':
            proxy_list.append(row[0].text + ':' + row[1].text)

    return proxy_list

def loadUserAgents(filename):
    '''Loads User-Agents from csv file'''
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        user_agents = []
        for row in reader:
            user_agents.append(row[0])
    return user_agents

user_agents = loadUserAgents('data/user_agents.csv')


def extract(proxy):
    '''Extracts valid proxies'''
    headers = {'User-Agent': random.choice(user_agents)}
    proxies={'https': proxy}
    try:
        print('Trying proxy: {}'.format(proxy))
        r = requests.get('https://rekvizitai.vz.lt/en/companies/', proxies=proxies,
        headers = headers, timeout=3)
        print(r.status_code)
        return proxy
    except:
        print('{} is not valid proxy.'.format(proxy))
        return False



proxy_list = getProxies()

for proxy in proxy_list:
    extract(proxy)

#check them all with futures super quick
# with concurrent.futures.ThreadPoolExecutor() as executor:
#         response = list(executor.map(extract, proxy_list))
#         valid_proxies = list(filter(lambda x: x != False, response))
