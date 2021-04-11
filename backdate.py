import json
from csvconverter import convJSONtoCSV
import os
import time
import datetime
DATA_FOLDER = ""

def main():
    names  = os.listdir(DATA_FOLDER)
    for item in names:
        temp_fold = DATA_FOLDER+item
        files = os.listdir(temp_fold)
        foo = 0
        for fil in files:
            if fil[-5:] != ".json":
                continue
            filename = temp_fold+"/"+fil
            csv = filename[:-5] + ".csv"
            jfile = open(filename, "r")
            JSONfile = json.load(jfile)
            jfile.close()
            datenum = time.mktime(datetime.datetime.strptime(JSONfile['created'], '%Y-%m-%d %H:%M:%S').timetuple())
            before = time.mktime(datetime.datetime.strptime("2021-02-19", '%Y-%m-%d').timetuple())
            if datenum > before:
                continue
            foo += 1
            convJSONtoCSV(JSONfile, csv)
        print(item + ": ",foo)
if __name__ == "__main__":
    main()
