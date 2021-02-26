# LT_Company_Data_Scraper
Lithuanian company ethical web scraper for educational and data analysis purposes.


So far the project consists of two parts geting the company links and scraping them.

## Part I Using selenium to get company links
### (This part will be rewritten in beutifulsoup since it is possible to navigate the pages without a webdriver)
1. Get categories for the company and save them to a file categories.txt . from https://rekvizitai.vz.lt/en/company-search/
2. Load categories.txt and loop through items in the txt.
3. Select category and load the page.
5. Start a while loop with condition that next link is available to click
6. Copy download the source and scrape all the company links.
7. Append new links with categories to a csv.
8. Click next page



## Part II Scraping company information (using scrapy or beutifulsoup)
