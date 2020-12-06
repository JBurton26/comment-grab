from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
import time, sqlite3
from os import path


def scrapeNvidia(keyword):
    final_titles = []
    final_costs = []
    options = FirefoxOptions()
    fp = webdriver.FirefoxProfile()
    fp.set_preference("javascript.enabled", True)
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_profile=fp, options=options)
    driver.get("""https://www.nvidia.com/en-gb/shop/geforce/?page=1&limit=100&locale=en-gb&search="""+keyword+"""&sorting=fg""")
    time.sleep(3)
    """
    for x in range(1):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            btn = driver.find_element_by_css_selector("input.buy-link.load-more-btn")
            btn.click()
            time.sleep(2)
            print("Loading More")
        except NoSuchElementException:
            print("All Loaded")
            break
    time.sleep(1)
    """
    page = driver.page_source
    soup = BeautifulSoup(page, 'html5lib')
    titles = soup.find_all("h2")
    prices = soup.find_all("div", "price clearfix")
    # TODO Fix Indexing on certain searches
    print("Num Titles: "+str(len(titles)))
    print("Num Prices: "+str(len(prices)))
    banned_words = ['SSD', '"', 'i5', 'i7', 'i9', 'RYZEN']
    for i in range(len(titles)):
        temp_title = titles[i].getText().strip()
        temp_cost = prices[i].getText().strip()
        temp_pass = False
        for word in banned_words:
            if word in temp_title:
                temp_pass = True
                break
        if(temp_pass):
            continue
        print(temp_title)
        final_titles.append(temp_title)
        print(temp_cost)
        final_costs.append(temp_cost)
    driver.quit()
    print("Num Titles: "+str(len(final_titles)))
    print("Num Prices: "+str(len(final_costs)))
    return final_titles, final_costs


scrapeNvidia("1660")
