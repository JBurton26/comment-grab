import json
import requests
import requests.auth
import time
import datetime
import os
import logging
from extracter import json_extract

authfile = "./configs/auth.json"
saveloc = "./data/raw/"
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
    response = requests.get("https://oauth.reddit.com/r/TinyHouses/top/?t=all&limit=10", headers=headers)
    resJSON = response.json()
    raw_fold = saveloc + "TinyHouses" + str(datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S'))
    if not os.path.exists(saveloc):
        os.mkdir(saveloc)
    os.mkdir(raw_fold)
    raw_file = raw_fold + "/posts.json"
    f = open(raw_file, 'w')
    json.dump(resJSON, f, indent = 4, sort_keys = True)
    f.close()
    logging.info("Raw post information saved. (Raw Reponse JSON.)")
    #print(resJSON)


    for post in resJSON['data']['children']:
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
        #print(response.status_code)
        """
        comms = []
        y = len(response.json()[1]['data']['children'])
        for i in range(len(response.json()[1]['data']['children'])):
            if response.json()[1]['data']['children'][i]['kind'] != 'more':
                comment = {
                    "user": response.json()[1]['data']['children'][i]['data']['author'],
                    "score": response.json()[1]['data']['children'][i]['data']['score'],
                    "body": response.json()[1]['data']['children'][i]['data']['body'],
                    "timestamp": datetime.datetime.fromtimestamp(response.json()[1]['data']['children'][i]['data']['created']).strftime('%Y-%m-%d %H:%M:%S'),
                    "postID": response.json()[1]['data']['children'][i]['data']['id']
                }

                #print(json.dumps(comment, indent=4))
        print(len(comms))
        """
        #authors = json_extract(response.json(), 'author')
        #print(len(com2))
        #print(com2[2])
        #scores = json_extract(response.json(), 'score')
        #print(len(com3))
        #print(com3[2])
        bodies = json_extract(response.json(), 'body')
        print(len(bodies))
        #print(com4[1])
        """
        for xi in range(len(bodies)):
            #if authors[xi+1] == "[deleted]":
            com = {
                "user": authors[xi+1],
                "score": scores[xi+1],
                "body": bodies[xi]
            }
            #print(json.dumps(com, indent=4))
            """

if __name__ == "__main__":
    credentials = getAuths()
    token = getOAuthToken(credentials)
    if token.status_code == 200:
        getComments(credentials, token, None)
    else:
        print("An Error Occurred during token request, response error:", token.status_code)
