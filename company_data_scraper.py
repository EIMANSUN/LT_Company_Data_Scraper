import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import random
import re
import csv

# Setup
file_name = 'data/company_data.csv'

# Column names for csv file. Also, related to data_filter in
# scrapeCompanyData() funtion (Maybe its a good idea to make data_filter global
# or at least as an argument for the function)
fieldnames = ['Company Name', 'Registration code', 'VAT',
            'Manager', 'Address', 'Website', 'Work hours',
            'SS insurer code', 'Transport', 'Authorized capital',
            'Company age', 'Employees', 'Average salary',
            'Social insurance taxes', 'Sales revenue From',
            'Sales revenue To', 'Rating', 'No. Rated', 'Category',
            'Other Categories', 'Facebook']

user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0')
test_url = 'https://rekvizitai.vz.lt/en/company/uab_royal_accounting/'

# Drop duplicate links from companies_url_scraper data
df = pd.read_csv('data/initial_test_companies_url.csv', header=None)
df.columns = ['URL', 'Category']
df.drop_duplicates(subset='URL', keep=False, inplace=True)
url_df = df.reset_index(drop=True)
print(df.head())


def loadUserAgents(filename):
    '''Loads User-Agents from csv file'''
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        user_agents_list = []
        for row in reader:
            user_agents_list.append(row[0])
        # Select random user-agent from the list
        user_agent = random.choice(user_agents_list)
        return user_agent

def loadPage(url, delay, user_agent):
    """Loads and returns html contents of the page"""
    headers = {'User-Agent': user_agent}
    r = requests.get(test_url, headers=headers)
    time.sleep(delay)
    soup = BeautifulSoup(r.content, 'lxml')

    # Checking for capcha
    capcha = soup.find('div',{'class':'content unusualTraffic'})
    if capcha:
        time.sleep(delay)
        user_agent = loadUserAgents('data/user_agents.csv')
        print('Capcha detecting! Switching User-Agent and retrying...')
        loadPage(url, delay, user_agent)
    else:
        return soup

def scrapeCompanyData(soup):
    """Scrape company data table"""

    # Empty data row to store scraped data. Note! column names are in fieldnames
    # list. If the page has missing data, column will be blank.
    data_row = {}

    # Part I Adds Company Name to the data row
    data_row['Company Name'] = soup.select('.fn')[0].get_text()

    # Part II Get main category and subcategories
    try:
        category = soup.find('div', {'class':'floatLeft about'}).find_all('a')
    except AttributeError:
        category = soup.find('div', {'class':'about floatLeft'}).find_all('a')
    else:
        data_row['Category'] = category[0]['title']
        # Run this part only if there is more than 1 category.
        other_categories = [i['title'] for i in category if len(category)>1]
        data_row['Other Categories'] = other_categories

    # Part III scrape table data
    # Find the first table and get all table rows
    table_rows = soup.find('table').find_all('tr')

    # Header names in data_filter list is used to filter table headers which
    # dont require special operations to scrape the data. Other headers require
    # additional formating before writing to data_row
    data_filter = ['Registration code', 'VAT', 'Manager', 'Address',
                  'Website', 'Work hours', 'SS insurer code',
                  'Average salary', 'Social insurance taxes',
                  'Transport', 'Authorized capital', 'Company age', 'Facebook']
    # Scrape table data
    for i, row in enumerate(table_rows):
        header_name = table_rows[i].find_all('td')[1].get_text()
        table_data = table_rows[i].find_all('td')[2].get_text().strip()
        if header_name in data_filter:
            data_row[header_name] = table_data
        elif header_name == 'Employees':
            data_row[header_name] = table_data.split(' ')[0]
        elif header_name == 'Sales revenue':
            result = re.search(r'\d+\s*\d*\s*[-]\s*\d*\s*\d*', table_data)
            data_row[header_name + ' From'] = result[0].replace(' ', '').split('-')[0]
            data_row[header_name + ' To'] = result[0].replace(' ', '').split('-')[1]
        elif header_name == 'Rating':
            try:
                rating = table_rows[i].find_all('td')[2].select('span')[0].get_text()
                no_rated = table_rows[i].find_all('td')[2].select('span')[2].get_text()
                data_row[header_name] = rating
                data_row['No. Rated'] = no_rated
            except IndexError:
                continue
    return data_row

def writeHeaders(file_name, fieldnames):
    """Writes headers to csv file"""
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def writeDataRow(file_name, data_row, fieldnames):
    """Appends rows to csv file"""
    with open(file_name, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data_row)

n_url = len(url_df)
print(f"Begin scraping {n_url} links...")
writeHeaders(file_name, fieldnames)

for url in url_df.iloc[:,0]:
    start = time.perf_counter()
    soup = loadPage(url, 3, user_agent)
    data_row = scrapeCompanyData(soup)
    writeDataRow(file_name, data_row, fieldnames)
    finish = time.perf_counter()
    n_url -= 1
    print(f'Succesfully scraped URL: {url}.')
    print(f"Scraping took: {finish-start}. URL's remaining: {n_url}")
