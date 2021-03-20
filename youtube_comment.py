from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.common.exceptions import NoSuchElementException
import platform
import os
from datetime import date

savefile = os.getcwd()+"/data/"
OS_TYPE = platform.system()

def test_youtube():
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
    driver.get("""https://www.youtube.com/watch?v=iQ35RkR5Pak""")
    """
    while(True):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        except Exception:
            break
        """
    page = driver.page_source
    today = date.today()
    d = today.strftime("%b-%d-%Y")
    htmlfile = savefile + d + ".html"
    f = open(htmlfile, "w", encoding="utf-8")
    f.write(page)
    f.close()

if __name__ == "__main__":
    test_youtube()
    print("Finished")
