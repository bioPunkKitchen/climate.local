#!/usr/bin/env python3
from flask import Flask, render_template, request
import datetime
import time
import os
import json
import handledata as handle

app = Flask(__name__)
hd = handle.handle_data()


def timestamp():
	time = datetime.datetime.now().strftime('%Y-%m-%d_%a_%H:%M:%S.%f')
	return time
	

def read_state():
	"""
	"""
	std_state = {
		'timestamp_measurement' : 'none',
		'temp_measured' : 'none',
		'state_onoff' : 'off',
		'state_light' : 'off',
		'state_cooling' : 'off',
		'state_heating' : 'off',
		'alert_msg' : '-'
	}
	try:
		with open('./data/state.json', 'r') as infile:
			state = json.load(infile)
	except IOError: 
		print(timestamp(), "\tIOError opening state.json for reading, using std_state instead")
		return std_state
	except json.decoder.JSONDecodeError as e:
		print(timestamp(), "\tJSONDecodeError reading state.json: ", e, " using std_state instead")
		return std_state
	return state
	

def read_conf():
	"""
	"""	
	std_config = {
		'timestamp_request' : 'none',
		'temp_desired' : '20.0',
		'light_on_time' : '07:00',
		'light_off_time' : '19:30',
	}
	try:
		with open('./data/config.json', 'r') as infile:
			config = json.load(infile)
	except IOError: 
		print(timestamp(), "\tIOError opening config.json for reading, using std_config instead")
		return std_config
	except json.decoder.JSONDecodeError as e:
		print(timestamp(), "\tJSONDecodeError reading config.json: ", e, " using std_config instead")
		return std_config
	return config
	
	
	
	
def write_conf(config):
	"""
	"""
	try:
		with open('./data/config.json', 'w') as outfile:
			print(timestamp(), "\tConfig written: ", config)
			json.dump(config, outfile)
	except IOError: 
		print(timestamp(), "\tIOError opening config.json for writing")
	return
	
	

@app.route('/')
def home():
	if os.path.exists('./data/firstrun'):
		os.remove('./data/firstrun')
		print(timestamp(), "\tFirst call detected, ./data/firstrun removed")
		return render_template('info.html')
	else:
		state = read_state()
		config = read_conf()
		if state['alert_msg'] != '-':
			return(state['alert_msg'])
		else:
			config['timestamp_request'] = timestamp()
			print(timestamp(), "\tServer writes config @1")
			write_conf(config)
			# generate individual and cachebusting filename (http://tinyw.in/8x8T):
			files = {
				'plot_png' : str('data_log.png?' + str(datetime.datetime.now().strftime("%f"))),
				'data_log' : str('data.log?' + str(datetime.datetime.now().strftime("%f")))
			}
			ret = {**state, **config, **files}
			return render_template('main.html', **ret)


@app.route('/input')
def input():
	state = read_state()
	config = read_conf()
	config['timestamp_request'] = timestamp()
	print(timestamp(), "\tServer writes config @2")
	write_conf(config)
	ret = {**state, **config}
	return render_template('input.html', **ret)


@app.route('/clear')
def clear():
	state = read_state()
	config = read_conf()
	hd.clean_file()
	config['timestamp_request'] = timestamp()
	print(timestamp(), "\tServer writes config @3")
	write_conf(config)
	# generate individual and cachebusting filename (http://tinyw.in/8x8T):
	files = {
		'plot_png' : str('data_log.png?' + str(datetime.datetime.now().strftime("%f"))),
		'data_log' : str('data.log?' + str(datetime.datetime.now().strftime("%f")))
	}
	ret = {**state, **config, **files}
	return render_template('main.html', **ret)


@app.route('/submit', methods=['POST'])
def submit():
	state = read_state()
	config = read_conf()
	if 'set_temp_desired' in request.form:
		if str(request.form['set_temp_desired']).replace('.','',1).isdigit(): # check string for int and float
			config['temp_desired'] = request.form['set_temp_desired']
		else:
			config['temp_desired'] = 20.0
	if 'set_light_on' in request.form:
		config['light_on_time'] = request.form['set_light_on']
	if 'set_light_off' in request.form:
		config['light_off_time'] = request.form['set_light_off']
	config['timestamp_request'] = timestamp()
	print(timestamp(), "\tServer writes config @4")
	write_conf(config)
	# generate individual and cachebusting filename (http://tinyw.in/8x8T):
	files = {
		'plot_png' : str('data_log.png?' + str(datetime.datetime.now().strftime("%f"))),
		'data_log' : str('data.log?' + str(datetime.datetime.now().strftime("%f")))
	}
	ret = {**state, **config, **files}
	return render_template('main.html', **ret)


if __name__ == '__main__':
	# ToDo:
	# https://vsupalov.com/flask-web-server-in-production/
	# https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
	try:
		with open('./data/state.json', 'r') as infile:
			state = json.load(infile)
		app.run( host= '0.0.0.0', port=8080, debug = False)
	except FileNotFoundError:
		print(timestamp(), "\t./data/state.json not found - climate_chamber.py has to be started first!")
	except ValueError:
		print(timestamp(), "\tFile ./data/state.json is empty or has wrong content - climate_chamber.py has to be started first!")
	except IOError: 
		print(timestamp(), "\tIOError opening state.json")
	except json.decoder.JSONDecodeError as e:
		print(timestamp(), "\tJSONDecodeError reading state.json: ", e)

