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
title = soup.find("h2")
print(title.get_text())
