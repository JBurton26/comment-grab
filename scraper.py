import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
options = FirefoxOptions()
fp = webdriver.FirefoxProfile()
fp.set_preference("javascript.enabled", True)
options.add_argument("--headless")
# options.add_argument("--enable-javascript")


driver = webdriver.Firefox(firefox_profile=fp, options=options)
driver.get("""https://www.nvidia.com/en-gb/shop/geforce/?page=1&limit=9&locale=en-gb&search=1660""")

page = driver.page_source
soup = BeautifulSoup(page, 'html5lib')
titles = soup.find_all("h2")
prices = soup.find_all("div", "price clearfix")
# print(title)
# print(title[2].get_text())
for i in range(len(titles)):
    print(titles[i].get_text())
    print(prices[i].get_text().strip()[1:])
