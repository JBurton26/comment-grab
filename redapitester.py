import json
import requests
import requests.auth
import time
import datetime
import os

def getAuths(file_name):
    try:
        print("File Found")
        f = open(filename, 'r')
        credentials = json.load(f)
        f.close()
        return credentials
    except Exception as e:
        f = open(filename, 'w')
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
        print("Filepath: "+os.getcwd()+"/auth.json")
        return None

def getOAuthToken(creds):
    try:
        client_auth = requests.auth.HTTPBasicAuth(creds['id'], creds['secret_key'])
        post_data = {"grant_type": "password", "username": creds['username'], "password": creds['psk']}
        headers = {"User-Agent": creds['userAgent']}
        res = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
        return res
    except Exception as e:
        print(e)
        return None

def getComments(creds, token):
    headers = {"Authorization": ("bearer "+token.json()['access_token']), "User-Agent": creds['userAgent']}
    response = requests.get("https://oauth.reddit.com/r/TinyHouses/top/?t=all&limit=3", headers=headers)
    #print(response.json())
    resJSON = response.json()
    """
    for item in resJSON['data']['children']:
        print(item['data']['permalink'])
        #print("")
    """
    link = "https://oauth.reddit.com" + resJSON['data']['children'][0]['data']['permalink']
    response = requests.get(link, headers=headers)
    #print(json.dumps(response.json()[1], indent=4))
    #print(json.dumps(response.json()[0], indent=4))

    y = len(response.json()[1]['data']['children'])
    #print("replies: " + str(response.json()[1]['data']['children'][y-1]) + "\n")
    for i in range(len(response.json()[1]['data']['children'])):
        #None
        #for key in response.json()[1]['data']['children'][i]['data']:
        #    print(key + ": " + str(response.json()[1]['data']['children'][i]['data'][key]) + "\n")
        if response.json()[1]['data']['children'][i]['kind'] != 'more':

            comment = {
                "user": response.json()[1]['data']['children'][i]['data']['author'],
                "score": response.json()[1]['data']['children'][i]['data']['score'],
                "body": response.json()[1]['data']['children'][i]['data']['body'],
                "timestamp": datetime.datetime.fromtimestamp(response.json()[1]['data']['children'][i]['data']['created']).strftime('%Y-%m-%d %H:%M:%S'),
                "postID": response.json()[1]['data']['children'][i]['data']['id']#,
                #"before": response.json()[1]['data']['children'][i]['before'],
                #"after": response.json()[1]['data']['children'][i]['after']
            }
            print(json.dumps(comment, indent=4))


if __name__ == "__main__":
    filename = "./auth.json"
    credentials = getAuths(filename)
    token = getOAuthToken(credentials)
    if token.status_code == 200:
        getComments(credentials, token)
    else:
        print("An Error Occurred during token request, response error:", token.status_code)
