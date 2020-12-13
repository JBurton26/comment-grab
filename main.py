#import scraper
import sqlite3
import os
import json
from flask import Flask, render_template, request, make_response
import matplotlib as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigCan
import io
import pandas as pd
import datetime
app = Flask(__name__)


searchtext = os.getcwd()+"/data/gpus.txt"


def getGPUs(number):
	dict = []
	conn=sqlite3.connect('data/cheapbase.sqlite3')
	cursor=conn.cursor()
	term = "%" + number + "%"
	cursor.execute("""SELECT * FROM nvidia_gpu WHERE name LIKE ?;""", (term,))
	rows = cursor.fetchall()
	conn.close()
	for x in rows:
		data = {
			'id' : x[0],
			'name' : x[1],
			'cooling': x[2],
			'clock': x[3],
			'mem': x[4]
		}
		dict.append(data)
	return dict


def getModels(type):
	types = []
	if(os.path.isfile(searchtext) is False):
		print("No")
	else:
		f = open(searchtext, "r")
		f_total = f.readlines()
		f.close()
		for line in f_total:
			words = line.split()
			if words[0] == type:
				types.append(line)
	return types


def getSpecCosts(id):

	conn=sqlite3.connect('data/cheapbase.sqlite3')
	cursor=conn.cursor()
	cursor.execute("""SELECT * FROM nvidia_gpu WHERE id = ?;""", (id,))
	x = cursor.fetchone()
	cursor.execute("""SELECT * FROM nvidia_gpu_prices WHERE gpu_id = ? ORDER BY date ASC LIMIT 20;""", (id,))
	rows = cursor.fetchall()
	prices = []
	for row in rows:
		dpri = {
			'cost': row[2],
			'date': row[3]
		}
		prices.append(dpri)
	data = {
		'id' : x[0],
		'name' : x[1],
		'cooling': x[2],
		'clock': x[3],
		'mem': x[4],
		'prices': prices
	}
	conn.close()
	return data

@app.route('/')
@app.route('/type')
def home():
	return render_template('home.html'), 200


@app.route('/type/<type>/')
def typebygr(type):
	models = getModels(type)
	return render_template('gtxrtx.html', models = models), 200


@app.route('/type/<type>/<model>')
def typebyno(type, model):
	gpus = getGPUs(model)
	return render_template('number.html', gpus=gpus, model=model), 200

@app.route('/type/<type>/<model>/<id>')
def modelStat(type, model, id):
	data = getSpecCosts(id)
	return render_template('spec.html', gpu=data), 200


##### TODO Figure out how to plot entire sections ####
"""
@app.route('/graph/model/<model>')
def graphCostTimeModel(model):
	return "HELLO"
"""
@app.route('/graph/<id>')
def graphCostTimeID(id):
	data = getSpecCosts(id)
	prices = []
	dates = []
	for item in data['prices']:
		prices.append(item['cost'])
		dates.append(item['date'])
	ys = prices
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	axis.set_title("Cost Over Time")
	axis.set_xlabel("Dates")
	axis.set_ylabel("Cost")
	axis.grid(True)
	xs = dates
	axis.plot(xs,ys)
	axis.set_xticklabels(xs, rotation='vertical')
	fig.tight_layout()
	canvas=FigCan(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=False)
