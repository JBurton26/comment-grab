from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
# Declaration of filepaths
FOLDER = os.getcwd()+"/data"
DATA_FILE = os.getcwd()+"/data/tinyhousementions.csv"
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
