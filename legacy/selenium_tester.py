from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox()
driver.get("https://www.nvidia.com/en-gb/shop/geforce/?page=1&limit=9&locale=en-gb&search=1660")
#assert "Python" in driver.title
elem = driver.find_element_by_class_name("product-details-grid-tile grid-tile-spacing")
print(elem)
driver.close()
