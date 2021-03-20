from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import sqlite3
import os
from sqlite3 import Error


fold = os.getcwd()+"/data"
db = os.getcwd()+"/data/cheapbase.sqlite3"
searchtext = os.getcwd()+"/data/gpus.txt"


def init_db():
    conn = sqlite3.connect(db)
    query = """CREATE TABLE nvidia_gpu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                cooling TEXT NOT NULL,
                clock TEXT NOT NULL,
                mem INTEGER NOT NULL);"""
    query2 = """
                CREATE TABLE nvidia_gpu_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gpu_id INTEGER NOT NULL REFERENCES nvidia_gpu(id),
                item_cost REAL NOT NULL,
                date TEXT NOT NULL);"""
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.execute(query2)
    conn.commit()
    conn.close()


if os.path.exists(fold):
    if os.path.isfile(db):
        try:
            conn = sqlite3.connect(db)
            print("DB Connected: "+sqlite3.version)
        except Error as e:
            print(e)
    else:
        f = open(db, "w")
        f.close()
        init_db()
        print("DB Connected: "+sqlite3.version)

else:
    try:
        os.mkdir(fold)
        f = open(db, "w")
        f.close()
        init_db()
        print("DB Connected: "+sqlite3.version)
    except OSError as e:
        print(e)


def scrapeNvidia(keyword):
    print("start")
    data = []
    options = Options()
    #options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)  # CHROME FOR RASPBIAN, FIREFOX FOR WINDOWS
    driver.get("""https://www.nvidia.com/en-gb/shop/geforce/?page=1&limit=100&locale=en-gb&search="""+keyword+"""&sorting=fg""")
    time.sleep(3)
    # Code not necessary for running - will possibly be useful for future iterations
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


def storage():
    if (os.path.isfile(searchtext) is False):
        print("File for searching GPUs is missing, one will be created")
        f = open(searchtext, "w")
        f.close()
        print("File created at: " + searchtext)
        print("Please populate this file with the model number(s) of the gpu you weant to analyse on each line")
    else:
        f = open(searchtext, "r")
        gpus = f.readlines()
        if len(gpus) < 1:
            print("GPU Search file at " + searchtext + " is empty, please add some items to look for.")
            return
        conn = sqlite3.connect(db)
        for gpu in gpus:
            DATA_NVIDIA = scrapeNvidia(gpu)
            for index in range(len(DATA_NVIDIA)):
                cursor = conn.cursor()
                state = """SELECT count(*) FROM nvidia_gpu WHERE nvidia_gpu.name = '""" + DATA_NVIDIA[index][0] + """'"""
                cursor.execute(state)
                xint = cursor.fetchone()[0]
                if(xint == 0):
                    query = """INSERT INTO nvidia_gpu (name, cooling, clock, mem) VALUES ((?),(?),(?),(?));"""
                    xvar = (DATA_NVIDIA[index][0], DATA_NVIDIA[index][2][0], DATA_NVIDIA[index][2][1], DATA_NVIDIA[index][2][2][:-3],)
                    conn.execute(query, xvar)
                    conn.commit()
                get_id = """SELECT id FROM nvidia_gpu WHERE nvidia_gpu.name = '""" + DATA_NVIDIA[index][0] + """';"""
                cursor.execute(get_id)
                ccgpu_id = cursor.fetchone()[0]
                query2 = """INSERT INTO nvidia_gpu_prices (gpu_id, item_cost, date) VALUES (?,?,datetime('now'));"""
                xvar2 = (ccgpu_id, DATA_NVIDIA[index][1])
                cursor.execute(query2, xvar2)
                conn.commit()
        conn.close()

if __name__ == "__main__":
    storage()
# scrapeNvidia("3060")
