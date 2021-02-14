from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.common.exceptions import NoSuchElementException
import time
import os
import platform
import sqlite3
import data_man as dm
# Declaration of filepaths
FOLDER = os.getcwd()+"/data"
DATA_FILE_CSV = os.getcwd()+"/data/tinyhousementions.csv"
DATA_FILE_DB = os.getcwd()+"/data/tinyhousementions.sqlite3"
OS_TYPE = platform.system()

def test_reddit():
    print("Testing Connection")
    print("System Type: " + OS_TYPE)
    # For currently unknown reasons, Raspian doesnt like GeckoDriver thus chrome has been used.
    if(OS_TYPE == 'Windows'):
        options = FFOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    elif(OS_TYPE == 'Linux'):
        options = ChOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    else:
        print(OS_TYPE + " is not supported at this time")
        print("Ending Program")
        return
    driver.get("""https://www.reddit.com/r/TinyHouses/""")
    try:
        for x in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
    except Exception:
        print("Problem Encountered")
    page = driver.page_source
    soup = BeautifulSoup(page, 'html5lib')
    titles = soup.find_all('div',{'class':'_1oQyIsiPHYt6nx7VOmd1sz'})
    for title in titles:
        notad = title.find('span',{'class':'_2oEYZXchPfHwcf9mTMGMg8'})
        if(notad is None):
            try:
                item = title.find('h3', {'class': '_eYtD2XCVieq6emjKBH3m'}).getText().strip()
                print(item)
            except Exception:
                continue
dm.file_all(FOLDER, DATA_FILE_DB, DATA_FILE_CSV)
test_reddit()

#<span class="_2oEYZXchPfHwcf9mTMGMg8">promoted</span>
