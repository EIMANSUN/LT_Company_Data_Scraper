#! /home/eimansun/anaconda3/bin/python

from bs4 import BeautifulSoup
from requests_html import HTMLSession

import csv
import time
import datetime

# Date stamp for file_name
date_stamp = datetime.datetime.now().strftime('%y%m%d')

#Setup
url_initial = 'https://rekvizitai.vz.lt/en/companies/'

session = HTMLSession()



#Create empty csv file:
file_name = f'companies_url_{date_stamp}.csv'
with open(file_name, 'w') as f:
    print(f'{file_name} has been created.')

def loadPage(url, user_agent, delay=3):

    r = session.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup
    time.sleep(delay)


def getCategories(soup):
    """Retrieve all categories"""
    selection = soup.find('select', {'id':'catUrlKey'})
    options = selection.find_all('option')
    categories = []
    for cat in options:
        if cat["value"] != "":
            categories.append(cat["value"])
    return categories

def getCatSearchResults(categories, url, user_agent):
    """Get search results for each category"""
    search_results = {}
    for cat in categories:
        url_cat = url + cat + '/'
        print(url_cat)
        html = loadPage(url, user_agent)
        with open("Debug.html", 'w') as f:
                f.write(str(html))
        breadcrumb = html.find("div", {"class":"breadcrumb"})
        floatRight = breadcrumb.find("div", {"class":"floatRight"})
        results = floatRight.find("strong").get_text()
        search_results[cat] = int(results)
        print(f"Found: {results} search results for category: {cat}")

    return search_results
html = loadPage(url_initial, user_agent, 3)
cat = getCategories(html)

print(f"Categories found: {len(cat)}")
print(getCatSearchResults(cat, url_initial, user_agent))
