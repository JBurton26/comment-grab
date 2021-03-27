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
    driver.get("""https://www.reddit.com/r/ScottishPeopleTwitter/comments/m2z0tk/scot_weather_helping_to_keep_the_infection_rate/""")
    try:
        #for x in range(1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        btn = driver.find_element_by_css_selector("button.j9NixHqtN2j8SKHcdJ0om._2iuoyPiKHN3kfOoeIQalDT._10BQ7pjWbeYP63SAPNS8Ts.HNozj_dKjQZ59ZsfEegz8._2nelDm85zKKmuD94NequP0")
        btn.click()
    except Exception:
        print("Problem Encountered")
    page = driver.page_source
    #soup = BeautifulSoup(page, 'html5lib')
    #titles = soup.find_all('div',{'class':'_3sf33-9rVAO_v4y0pIW_CH'})
    #print(len(titles))
    #for title in titles:
    """ # FOR FINDING ALL OF THE POSTS WITHIN A SUBREDDIT
        notad = title.find('span',{'class':'_2oEYZXchPfHwcf9mTMGMg8'})
        if(notad is None):
            try:
                item = title.find('h3', {'class': '_eYtD2XCVieq6emjKBH3m'}).getText().strip()
                print(item)
            except Exception:
                continue
    """

        #it = title.value_of_css_property("padding-left")
        #print(it)
    #print(titles[0])
    try:
        elements = driver.find_elements_by_class_name("_3sf33-9rVAO_v4y0pIW_CH")
        for element in elements:
            print(element.text)
            level = element.find_element_by_class_name('_1RIl585IYPW6cmNXwgRz0J').text      #text#.split('\n')
            user = element.find_element_by_class_name('f3THgbzMYccGW8vbqZBUH._23wugcdiaj44hdfugIAlnX').text
            comment = element.find_element_by_class_name('_1qeIAgB0cPwnLhDF9XSiJM').text
            score = element.find_element_by_class_name('_1rZYMD_4xY3gRcSS3p8ODO._25IkBM0rRUqWX5ZojEMAFQ._3ChHiOyYyUkpZ_Nm3ZyM2M').text
            print('\n\n#######################################################\n\n') ##element.value_of_css_property("padding-left") + " : " +
            print('Level: ', level)
            print('User: ', user)
            print('Comment: ', comment)
            print('Score: ', score)
    except Exception as e:
        print(e)
"""
def px16():


def px37():


def px58():
"""


if __name__ == "__main__":
    dm.file_all(FOLDER, DATA_FILE_DB, DATA_FILE_CSV)
    test_reddit()
    print("finished")


# div id for comments = t1_gqmrnw7
#<span class="_2oEYZXchPfHwcf9mTMGMg8">promoted</span>
