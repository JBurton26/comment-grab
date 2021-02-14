import os
import sqlite3


def init_db(DB):
    try:
        csvop = open(DB, "x")
        conn = sqlite3.connect(DB)
        table_query1 = """CREATE TABLE posts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            encr_name TEXT NOT NULL,
                            post_url TEXT NOT NULL,
                            post_title TEXT NOT NULL,
                            post_content TEXT,
                            image_url TEXT);
                            """
        print("DB File Created")
    except Exception:
        print("DB File Already Exists")


def init_csv(CSV):
    try:
        csvop = open(CSV, "x")
        print("CSV File Created")
    except Exception:
        print("CSV File Already Exists")


def file_all(FOLDER, DB, CSV):
    if os.path.exists(FOLDER):
        #init_db(DB)
        init_csv(CSV)
    else:
        try:
            os.mkdir(FOLDER)
            #init_db(DB)
            init_csv(CSV)
            print("Data Files and Folder Created.")
        except OSError as e:
            print(e)
