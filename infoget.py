import json
import requests
import requests.auth
import time
import datetime
import os
import logging
from extracter import json_extract, json_get_obj

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
        print("Auths File Found")
        logging.info("Auths File Found")
        f = open(authfile, 'r')
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

def getOAuthToken(creds):
    try:
        client_auth = requests.auth.HTTPBasicAuth(creds['id'], creds['secret_key'])
        post_data = {"grant_type": "password", "username": creds['username'], "password": creds['psk']}
        headers = {"User-Agent": creds['userAgent']}
        res = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
        print("Response Status Code: ", res.status_code) # requests has in built logging set up
        return res
    except Exception as e:
        print(e)
        logging.error(e)
        return None

def getComments(creds, token, input):
    headers = {"Authorization": ("bearer "+token.json()['access_token']), "User-Agent": creds['userAgent']}
    response = requests.get("https://oauth.reddit.com/r/TinyHouses/top/?t=year&limit=10", headers=headers)
    resJSON = response.json()
    raw_fold = saveloc + "TinyHouses" + str(datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')) +"/"
    processed_fold = processed + "TinyHouses" + str(datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'))+"/"
    if not os.path.exists(saveloc):
        os.mkdir(saveloc)
    elif not os.path.exists(processed):
        os.mkdir(processed)
    os.mkdir(raw_fold)
    os.mkdir(processed_fold)
    raw_file = raw_fold + "posts.json"
    f = open(raw_file, 'w')
    json.dump(resJSON, f, indent = 4, sort_keys = True)
    f.close()
    logging.info("Raw post information saved. (Raw Reponse JSON.)")
    #print(resJSON)


    for post in resJSON['data']['children']:
        #print(json.dumps(post, indent = 4, sort_keys = True))
        link = "https://oauth.reddit.com" + post['data']['permalink'] + "/?limit=300"
        response = requests.get(link, headers=headers)
        #print(json.dumps(response.json(), indent = 4, sort_keys = True))
        try:
            raw_file = raw_fold + "/" + post['data']['id'] +"_raw_comments.json"
            f = open(raw_file, 'w')
            json.dump(response.json(), f, indent = 4, sort_keys = True)
            f.close()
            logging.info("File Saved: " + raw_file)
        except Exception as e:
            logging.error(e)

        ids = json_extract(response.json(), 'id')
        ids.pop(0)
        ids.pop(0)

        ids = [ x for x in ids if x != "_"]


        post_id = post['data']['id']
        com_new = []
        for x in ids:
            try:
                obj = json_get_obj(response.json(), x)
                com = {
                    "user": obj[0]['author'],
                    "score": obj[0]['score'],
                    "body": obj[0]['body'],
                    "parent": obj[0]['parent_id'],
                    "id": "t1_" + obj[0]['id'],
                    "created":datetime.datetime.fromtimestamp(obj[0]['created']).strftime('%Y-%m-%d %H:%M:%S')
                }
                com_new.append(com)
            except Exception as e:
                print(e)
        corrected_com = com_new[::-1]

        comments = {
            "user":post['data']['author'],
            "created": datetime.datetime.fromtimestamp(post['data']["created"]).strftime('%Y-%m-%d %H:%M:%S'),
            "permalink": "www.reddit.com" + post['data']['permalink'],
            "score": post['data']['score'],
            "name": post['data']['name'],
            "title": post['data']['title'],
            "upvote_ratio": post['data']['upvote_ratio'],
            "images":post['data']['url'],
            "xcomments":corrected_com
        }

        #print(json.dumps(comments, indent = 4, sort_keys = True))
        processed_file = processed_fold + post['data']['name'] + ".json"
        f = open(processed_file, 'w')
        json.dump(comments, f, indent = 4, sort_keys = True)
        f.close()



if __name__ == "__main__":
    credentials = getAuths()
    token = getOAuthToken(credentials)
    if token.status_code == 200:
        getComments(credentials, token, None)
    else:
        print("An Error Occurred during token request, response error:", token.status_code)
