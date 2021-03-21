import infoget as inf
import tkinter as tk
import logging


if __name__ == "__main__":
    logging.basicConfig(filename='logs/runlog.log', encoding='utf-8', level=logging.DEBUG)
    credentials = inf.getAuths()

    token = inf.getOAuthToken(credentials)
    try:
        inf.getComments(credentials, token, None)
    except AttributeError as e:
        print("Attribute Error: ")
    except Exception as e2:
        print("Authentication values invalid or error during request, response error:", token.status_code)
        print(e2)
