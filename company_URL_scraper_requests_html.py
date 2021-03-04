#! /home/eimansun/anaconda3/bin/python

from requests_html import HTMLSession
import csv
import time
import datetime

#Setup
date_stamp = datetime.datetime.now().strftime('%y%m%d')
url_initial = 'https://rekvizitai.vz.lt/en/companies/'
session = HTMLSession()
fieldnames = ["comapny_url"]

if "data" not in os.listdir():
    os.mkdir("data")
    print("Data folder has been created.")
else:
    print("Data already exists.")

#Create empty csv file:
data_file = f'/data/companies_url_{date_stamp}.csv'
with open(data_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    print(f'{data_file} has been created.')


def loadPage(url):
    """Returns response object from URL"""
    # session = HTMLSession() needs to be declared outside the function
    global session
    try:
        response = session.get(url)
        response.html.render(sleep=5)
    except:
        print(f"Failed to load URL: {url}")
    return response


def getCategories(response):
    """Retrieve all categories"""
    select = response.html.find("select#catUrlKey", first=True)
    options = select.find("option")
    categories = []
    for cat in options:
        if cat.attrs["value"] != "":
            categories.append(cat.attrs["value"])
    return categories

def getMetrics(response):
    """Parse search results and page numbers for the category"""
    # Parse search results.
    breadcrumb = response.html.find("div.breadcrumb", first=True)
    result = breadcrumb.find(".floatRight strong", first=True).text
    # Parse page numbers.
    pager = response.html.find("div.pager", first=True)
    pages_total = pager.find("a")[-2].attrs["href"].split("/")[-2]
    print(f"Search resuls: {result}. Pages: {pages_total}")
    return (int(result), int(pages_total))

def getCatSearchResults(url, categories):
    """Get search results for each category"""
    search_results = {}
    for cat in categories:
        url_cat = url + cat
        response = loadPage(url_cat)
        breadcrumb = response.html.find("div.breadcrumb", first=True)
        result = breadcrumb.find(".floatRight strong", first=True).text
        search_results[cat] = int(result)
        print(f"Found {result} search results for {cat} category.")
        print(search_results)
    return search_results

def parseCompanyLinks(response):
    """Parse all company links in page"""
    links = response.html.find("a.firmTitle")
    with open(data_file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        count = 0
        for link in links:
            writer.writerow({fieldnames[0]: link.attrs["href"]})
            count += 1
        return count


# Load all categories
r = loadPage(url_initial)
print(r.html)
categories = getCategories(r)

#search_results = getCatSearchResults(url_initial, cat)

# Go through each category
cat_count = len(categories)
rem_cat_count = cat_count
for cat in categories:
    url_cat = url_initial + cat
    response = loadPage(url_cat)
    search_results, pages = getMetrics(response)
    remaining_results = search_results
    page = 1
    # Navigate through each page of the category
    while (page <= pages) or results == 0:
        url_count = parseCompanyLinks(response)
        remaining_results -= url_count
        print(f"Succesfully parsed: {url_count} company links for {cat} category.")
        print(f"Remaining search results: {remaining_results}/{search_results}")
        print(f"Pages left: {pages-page}/{pages}")
        print(f"Categories left: {rem_cat_count}/{cat_count}")
        url_cat_page = f"{url_cat}/{page}/"
        response = loadPage(url_cat_page)
        page += 1
    rem_cat_count -= 1
    print(f"Finished parsing {cat} category.\nPages left: {pages}\nSearch results left: {search_results}")
