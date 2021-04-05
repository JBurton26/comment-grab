import json
import requests
import requests.auth
import time
import datetime
import os
import logging
from extracter import json_extract, json_get_obj
from csvconverter import convJSONtoCSV


authfile = "./configs/auth.json"
saveloc = "./data/raw/"
processed = "./data/processed/"
configfile = "./configs/config.json"
try:
    f = open(configfile, 'r')
    settings = json.load(f)
    f.close()
except Exception as e:
    f = open(configfile, 'w')
    settings = {
      "logloc": "./logs/runlog.log"
    }
    json.dump(settings, f, indent = 4, sort_keys = True)
    f.close()
logging.basicConfig(filename=settings['logloc'], encoding='utf-8', level=logging.DEBUG)
logging.info("\n\nSession Start: " + str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

def getAuths():
    try:
        f = open(authfile, 'r')
        print("Auths File Found")
        logging.info("Auths File Found")
        credentials = json.load(f)
        f.close()
        return credentials
    except Exception as e:
        f = open(authfile, 'w')
        credentials = {
          "username":"",
          "psk":"",
          "userAgent": "",
          "id":"",
          "secret_key":""
        }
        json.dump(credentials, f, indent = 4, sort_keys = True)
        f.close()
        print("auth.json file missing, one has been created for you.\nPlease populate this file with the appropriate values.")
        print("Filepath: "+os.getcwd()+"\configs\\auth.json")
        logging.info("auths.json file not found, new created at: " + os.getcwd() + "/auth.json")
        return None

def getOAuthToken():
    try:
        creds = getAuths()
        if creds == None:
            raise Exception("auths.json empty")
        for k, v in creds.items():
            if len(v) == 0:
                raise Exception("No value for 1 or more values in auth.json")
        client_auth = requests.auth.HTTPBasicAuth(creds['id'], creds['secret_key'])
        post_data = {"grant_type": "password", "username": creds['username'], "password": creds['psk']}
        headers = {"User-Agent": creds['userAgent']}
        token = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
        print("Response Status Code: ", token.status_code) # requests has in built logging set up
        return creds, token
    except Exception as e:
        print(e)
        logging.error("Exception occurred", exc_info=True)
        return creds, None

def getComments(inp):
    try:
        creds, token = getOAuthToken()
        if creds == None:
            raise ValueError("Credentials file has no values")
        elif token == None:
            raise ValueError("Credentials file has no values1")
        elif token.status_code != 200:
            raise Exception("Authentication values were not correct or were empty.")
        headers = {"Authorization": ("bearer "+token.json()['access_token']), "User-Agent": creds['userAgent']}
        req = "https://oauth.reddit.com/r/" + inp['subreddit'] + "/" + inp['sorting'] + "/?t=year&limit=" + str(inp['limit'])
        response = requests.get(req, headers=headers)
        resJSON = response.json()
        raw_fold = saveloc + inp['subreddit'] + str(datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')) +"/"
        processed_fold = processed + inp['subreddit'] + str(datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'))+"/"
        if not os.path.exists(saveloc):
            os.mkdir(saveloc)
        if not os.path.exists(processed):
            os.mkdir(processed)
        os.mkdir(raw_fold)
        os.mkdir(processed_fold)
        raw_file = raw_fold + "posts.json"
        f = open(raw_file, 'w')
        json.dump(resJSON, f, indent = 4, sort_keys = True)
        f.close()
        logging.info("Raw post information saved. (Raw Reponse JSON.)")
        for post in resJSON['data']['children']:
            link = "https://oauth.reddit.com" + post['data']['permalink'] + "/?limit=300"
            response = requests.get(link, headers=headers)
            raw_file = raw_fold + "/" + post['data']['id'] +"_raw_comments.json"
            f = open(raw_file, 'w')
            respii = {
                #"comments":response.json()
            }
            json.dump(response.json(), f, indent = 4, sort_keys = True)
            f.close()

            logging.info("File Saved: " + raw_file)
            ids = json_extract(response.json(), 'id')
            post_id = post['data']['id']
            ids.remove(post_id)
            ids = [ x for x in ids if (x != "_" and x.islower())]

            comments = {
                "user":post['data']['author'],
                "created": datetime.datetime.fromtimestamp(post['data']["created"]).strftime('%Y-%m-%d %H:%M:%S'),
                "permalink": "www.reddit.com" + post['data']['permalink'],
                "score": post['data']['score'],
                "name": post_id,
                "title": post['data']['title'],
                "upvote_ratio": post['data']['upvote_ratio'],
                "images":post['data']['url'],
                "xcomments":[]
            }
            if len(ids) != 0:
                com_new = []
                for x in ids:
                    obj = json_get_obj(response.json(), x)
                    if 'author' not in obj[0].keys():
                        continue
                    com = {
                        "user": obj[0]['author'],
                        "score": obj[0]['score'],
                        "body": obj[0]['body'],
                        "parentComment": obj[0]['parent_id'],
                        "id": "t1_" + obj[0]['id'],
                        "created":datetime.datetime.fromtimestamp(obj[0]['created']).strftime('%Y-%m-%d %H:%M:%S')
                    }
                    com_new.append(com)
                corrected_com = com_new[::-1]
                comments['xcomments'] = corrected_com
            processed_file = processed_fold + post_id
            processed_JSON = processed_file + ".json"
            processed_CSV = processed_file + ".csv"
            f = open(processed_JSON, 'w')
            json.dump(comments, f, indent = 4, sort_keys = True)
            f.close()
            logging.info("Processed JSON information saved: " + post_id)
            #print("Processed JSON information saved: " + post_id)
            convJSONtoCSV(comments, processed_CSV)
            logging.info("Processed CSV information saved: " + post_id)
            #print("Processed CSV information saved: " + post_id)
        print("Finished Collecting")
        return 0
    except KeyError as e:
        #print(json.dumps(obj, indent = 4))
        print(post_id)
        print(x)
        print(ids)
    except Exception as e2:
        print(e2)
        logging.error("Exception occurred", exc_info=True)
        return e2


if __name__ == "__main__":
    subreddits = [ "TinyHouses","tinyhouse", "tinyhomes"] #
    inp = {
        "sorting":"top",
        "limit": 100
    }
    for subreddit in subreddits:
        inp['subreddit'] = subreddit
        b = getComments(inp)
        if b != 0:
            print(b)
