#! /home/eimansun/anaconda3/bin/python

from selenium import webdriver
#Imports for waits
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# For selecting items in form
from selenium.webdriver.support.ui import Select

import csv
import time


#Setup
PATH = '/home/eimansun/Projects/WebDev/Web_Scraping/Selenium/geckodriver'
driver = webdriver.Firefox(executable_path=PATH)
timeout = 60

#Create empty csv file:
file_name = 'companies_url.csv'
with open(file_name, 'w') as f:
    print(f'{file_name} has been created.')



driver.get('https://rekvizitai.vz.lt/en/company-search/')


# Return a list of categories
def getCategories(save=True):
    cat = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "cat")))
    categories = cat.find_elements_by_tag_name("option")
    catList = []
    for i in categories:
        catList.append(i.text)
    return catList


#Select Category
def selectCategory(catList, index=0):
    target = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "cat")))
    #Scroll into view
    driver.execute_script("arguments[0].scrollIntoView();", target)
    # Create a selector object
    select = Select(driver.find_element_by_id("cat"))
    # Select category by index
    select.select_by_visible_text(catList[index])


def searchButton():
    search_button = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.ID, "ok")))
    driver.execute_script("arguments[0].scrollIntoView();", search_button)
    search_button.click()

def companyUrlAppender(category):
    companyLinks = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located(
        (By.XPATH, "//a[@href and @class='firmTitle']")))



    with open(file_name, "a", newline='') as csv_file:
        urlwriter = csv.writer(csv_file)
        count = 0
        for link in companyLinks:
            print(link.get_attribute("href"))
            urlwriter.writerow([link.get_attribute("href"), category])
            count += 1
        print(f"{count} URL's have been appended to {file_name}")
        time.sleep(1)


categories = getCategories(save=False)

#searchFrom = categories.index('Homeowners associations')
searchFrom = 0

t0_tot = time.time()
# Should be in for loop
for cat in categories[searchFrom:]:
    t0 = time.time()
    driver.get('https://rekvizitai.vz.lt/en/company-search/')
    selectCategory(categories, categories.index(cat))
    searchButton()

    while True:
        try:
            nextButton = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(
                (By.XPATH, "//a[@title='Next page' and @class='prevnext']")))
            companyUrlAppender(cat)

        except:
            print('Next page has not been found continuing to next category')
            break
        nextButton = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(
            (By.XPATH, "//a[@title='Next page' and @class='prevnext']")))
        nextButton.click()
        time.sleep(1)


    t1 = time.time()
    dt = t1 - t0
    print(f'{cat} took {dt}sec. to complete')



t1_tot = time.time()
dt_tot = t1_tot - t0_tot
print(f'URL parsing took {dt_tot}sec. to complete')
time.sleep(5)
driver.quit()
