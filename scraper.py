from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
import time, sqlite3
from os import path


def scrapeNvidia(keyword):
    data = []
    options = FirefoxOptions()
    fp = webdriver.FirefoxProfile()
    fp.set_preference("javascript.enabled", True)
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_profile=fp, options=options)
    driver.get("""https://www.nvidia.com/en-gb/shop/geforce/?page=1&limit=100&locale=en-gb&search="""+keyword+"""&sorting=fg""")
    time.sleep(3)
    # Code not necessary for running
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
    specs = soup.find_all("div", "specs-container")
    banned_words = ['SSD', '"', 'i5', 'i7', 'i9', 'RYZEN']  # Filters out laptops and other devices.
    for i in range(len(titles)):
        new_data = []
        temp_title = titles[i].getText().strip()
        temp_cost = prices[i].getText().strip()
        temp_specs = []
        temp_specs_set = specs[i].find_all("div", "specs")     # [Cooling, Clock, MEM Size]
        temp_pass = False
        for word in banned_words:
            if word in temp_title:
                temp_pass = True
                break
        if(temp_pass):
            continue
        new_data.append(temp_title)
        new_data.append(temp_cost[1:])
        temp_specs.append(temp_specs_set[0].getText().strip()[16:])
        temp_specs.append(temp_specs_set[1].getText().strip()[19:])
        temp_specs.append(temp_specs_set[2].getText().strip()[17:])
        new_data.append(temp_specs)
        data.append(new_data)
    driver.quit()
    print("Data Collected: " + keyword + ". Num Collected: " + str(len(data)))
    return data


# scrapeNvidia("3060")
