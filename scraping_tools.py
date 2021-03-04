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


def extract(url, proxy):
    '''Extracts valid proxies'''
    headers = {'User-Agent': random.choice(user_agents)}
    proxies={'https': proxy}
    try:
        print('Trying proxy: {}'.format(proxy))
        r = requests.get(url, proxies=proxies,
        headers = headers, timeout=5)
        print(r.status_code)
        return r
    except:
        print('{} is not valid proxy.'.format(proxy))
        return False


def dataPartition(data, step, start=0, end=None):
    """Partition dataset into speperate parts"""
    # If data partition end is not assigned then use total size as the length
    if end == None:
        end=len(data)

    finish = step
    partition_num = 1
    data_partitions = []
    print(f"Partitioning: {end} data records into {end/step}")
    while True:
        if finish < end:
            batch = data[start:finish]
            data_partitions.append(batch)
            print(f"URL batch No.{partition_num}")
            start = finish
            finish += step
            partition_num += 1
        else:
            batch = data[start:end ]
            data_partitions.append(batch)
            print(f"Final URL batch No.{partition_num}")
            break
    return data_partitions

def main():

    test_url = ["https://rekvizitai.vz.lt/en/companies/accounting_services/1/",
                "https://rekvizitai.vz.lt/en/companies/accounting_services/2/",
                "https://rekvizitai.vz.lt/en/companies/accounting_services/3/",
                "https://rekvizitai.vz.lt/en/companies/accounting_services/4/",
                "https://rekvizitai.vz.lt/en/companies/accounting_services/5/",
                "https://rekvizitai.vz.lt/en/companies/accounting_services/6/",
                "https://rekvizitai.vz.lt/en/companies/accounting_services/7/",
                "https://rekvizitai.vz.lt/en/companies/accounting_services/8/",
                "https://rekvizitai.vz.lt/en/companies/accounting_services/9/"]


    dataPartition(test_url, 3)

    # proxy_list = getProxies()


#     for proxy in proxy_list:
#         extract(proxy)
#
# #check them all with futures super quick
# with concurrent.futures.ThreadPoolExecutor() as executor:
#

if __name__ == '__main__':
    main()
