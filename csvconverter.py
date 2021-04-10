import json
import csv
import logging
import pandas as pd
def convJSONtoCSV(obj, processed_CSV):
    df = pd.json_normalize(obj, 'xcomments', ['user', 'created', 'permalink', 'score', 'name', 'title', 'bodytext', 'upvote_ratio', 'images'],
        record_prefix='comment.')
    df.to_csv(processed_CSV,index=False)
if __name__ == "__main__":
    None
