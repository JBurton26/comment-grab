import requests
from bs4 import BeautifulSoup
from selenium import webdriver

#import time
driver = webdriver.Firefox()
driver.get("""https://www.nvidia.com/en-gb/shop/geforce/?page=1&limit=9&locale=en-gb&search=1660""")

page = driver.page_source
soup = BeautifulSoup(page, 'html5lib')
title = soup.find("div")
print(title)
