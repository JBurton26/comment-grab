from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
import time


def scrapeNvidia(keyword):
    options = FirefoxOptions()
    fp = webdriver.FirefoxProfile()
    fp.set_preference("javascript.enabled", True)
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_profile=fp, options=options)
    driver.get("""https://www.nvidia.com/en-gb/shop/geforce/?page=1&limit=9&locale=en-gb&search="""+keyword+"""&sorting=fg""")
    time.sleep(1)
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            btn = driver.find_element_by_css_selector("input.buy-link.load-more-btn")
            btn.click()
            time.sleep(2)
            print("Loading More")
        except NoSuchElementException:
            print("All Loaded")
            break
    page = driver.page_source
    soup = BeautifulSoup(page, 'html5lib')
    titles = soup.find_all("h2")
    prices = soup.find_all("div", "price clearfix")
    #TODO Fix Indexing on certain searches
    for i in range(len(titles)):
        print(titles[i].get_text())
        print(prices[i].get_text().strip()[1:])
    driver.quit()


scrapeNvidia("30")
