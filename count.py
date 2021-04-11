import json
import os
DATA_FOLDER = ""
def main():
    names  = os.listdir(DATA_FOLDER)
    foo = 0
    for item in names:
        temp_fold = DATA_FOLDER+item
        files = os.listdir(temp_fold)
        for fil in files:
            if fil[-5:] != ".json":
                continue
            filename = temp_fold+"/"+fil
            jfile = open(filename, "r")
            JSONfile = json.load(jfile)
            jfile.close()
            foo += len(JSONfile['xcomments'])
    print(foo)



if __name__ == "__main__":
    main()
