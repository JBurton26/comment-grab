#import scraper
import sqlite3
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
	return "<p>Hello World</p>"
