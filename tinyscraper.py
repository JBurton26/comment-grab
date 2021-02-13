from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.common.exceptions import NoSuchElementException
import time
import os
import platform
# Declaration of filepaths
FOLDER = os.getcwd()+"/data"
DATA_FILE = os.getcwd()+"/data/tinyhousementions.csv"
OS_TYPE = platform.system()

# Checks the files exist, creates them if necessary
if os.path.exists(FOLDER):
    if os.path.isfile(DATA_FILE):
        try:
            print("Data File Found at: " + DATA_FILE)
        except Error as e:
            print(e)
    else:
        f = open(DATA_FILE, "w")
        f.close()
        print("Data File Created at: " + DATA_FILE)

else:
    try:
        os.mkdir(FOLDER)
        f = open(DATA_FILE, "w")
        f.close()
        print("Data File and Folder Created.")
    except OSError as e:
        print(e)

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
    page = driver.page_source
    soup = BeautifulSoup(page, 'html5lib')
    titles = soup.find_all('div',{'class':'_1oQyIsiPHYt6nx7VOmd1sz'})
    for title in titles:
        notad = title.find('span',{'class':'_2oEYZXchPfHwcf9mTMGMg8'})
        if(notad is None):
            item = title.find('h3', {'class': '_eYtD2XCVieq6emjKBH3m'}).getText().strip()
            print(item)
test_reddit()

#<span class="_2oEYZXchPfHwcf9mTMGMg8">promoted</span>
