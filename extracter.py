import json
# Code adapted from From: https://hackersandslackers.com/extract-data-from-complex-json-python/ on 22/03/2021.
def json_extract(obj, search):
    arr = []
    def extract(obj, arr, search):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "all_awardings":
                    continue
                elif isinstance(v, (dict, list)):
                    if k == "all_awardings" or k == "gallery_data" or k == "media_metadata":
                        continue
                    extract(v, arr, search)
                elif k == search:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, search)
        return arr

    values = extract(obj, arr, search)
    return values

def json_get_obj(obj, id):
    val = []
    def getObj(obj, val, id):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    getObj(value, val, id)
                elif value == id:
                    val.append(obj)
                    #print(obj)
        elif isinstance(obj, list):
            for item in obj:
                getObj(item, val, id)
        return val
    ret = getObj(obj, val, id)
    return ret

if __name__ == "__main__":
    ##########
    #testing##
    ##########
    f = open("./data/test.json", "r")
    tests = json.load(f)
    f.close()
    print(json.dumps(tests, indent = 4))
    testObj = json_get_obj(tests, "test1")
    print(testObj[0])
