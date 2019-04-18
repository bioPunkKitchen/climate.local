#!/usr/bin/env python3
import hardware_control
import handledata
import ds1820_raspi_readout
import datetime
import time
import json
from shutil import copyfile as cpf


def timestamp():
	"""
	"""	
	time = datetime.datetime.now().strftime('%Y-%m-%d_%a_%H:%M:%S.%f')
	return time
	
	
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
	

def state_write(state):
	"""
	"""	
	try:
		with open('./data/state.json', 'w') as outfile:
			print(timestamp(), "\tClimate_chamber.py writes state.json ")
			json.dump(state, outfile)
	except IOError: 
		print(timestamp(), "\tIOError opening state.json for writing")
	return
	

if __name__ == '__main__':
	"""
	"""
	ds1820 = ds1820_raspi_readout.ds1820()
	datahandler = handledata.handle_data()
	hc = hardware_control.hardware_control()
	hc.hw_setup()


	# configuration and status
	state = {
		'timestamp_measurement' : 'none',
		'temp_measured' : 'none',
		'state_onoff' : 'off',
		'state_light' : 'off',
		'state_cooling' : 'off',
		'state_heating' : 'off',
		'alert_msg' : '-'
	}

	# internal parameters: DON'T TOUCH THEM!!!
	# Manipualtion of internal parameters can lead to malfunction, damage, fire, etc.
	int_par = {
		'last_update' : 'none',
		'temp_hysteresis' : 1.0,
		'temp_min' : 5,
		'temp_max' : 40,
		'intervall_measure' : 10,		#in sec: 10s
		'intervalls_log' : 6,			#6*10s=1min
		'intervalls_dump' : 360,		#6h*60min=360 (4x/day)
		'intervalls_max_work' :  270,	#270*10s=45min.
		'intervalls_work' : 0
	}

	state['timestamp_measurement'] = timestamp()
	state['temp_measured'] = str(ds1820.read())
	state_write(state)
		 
	datahandler.insert_data(state['timestamp_measurement'], state['temp_measured'], state['state_onoff'], state['state_light'], state['state_cooling'], state['state_heating'])
	datahandler.append_data_to_file()
	datahandler.update_graph('./static/data_log.png')
	int_par['last_update'] = state['timestamp_measurement'] # timestamp of update to data.log

	try:
		# Control loop
		while True:
			for i in range(int_par['intervalls_dump']):
				for j in range(int_par['intervalls_log']):
					# Read config, read temp, set timestamp
					config = read_conf()
					state['temp_measured'] = str(ds1820.read())
					state['timestamp_measurement'] = timestamp()
					timestamp_measurement_H_M = datetime.datetime.strptime(state['timestamp_measurement'], '%Y-%m-%d_%a_%H:%M:%S.%f').strftime("%H:%M")

					# Temp.-control: check dangerous conditions
					if float(state['temp_measured']) > 42:
						state['state_onoff'] = 'off'
						hc.control_pin(hc.onoff_pin, hc.is_off)
						hc.control_pin(hc.temp_en_pin, hc.is_off)
						print(timestamp(), "\tTemperature is above 42°C!!! Heating switched off, waiting for 15min. to cool down.")
						state['alert_msg'] = "<H2>DANGER: Temperature is above 42°C!!!<br>Heating switched off, waiting for 15min. to cool down.<br></H2>" + str(timestamp())
						state_write(state)
						time.sleep(900) # 15 min. off
						state['alert_msg'] = '-'
						state_write(state)				
					elif int_par['intervalls_work'] > int_par['intervalls_max_work']:
						state['state_onoff'] = 'off'
						hc.control_pin(hc.onoff_pin, hc.is_off)
						hc.control_pin(hc.temp_en_pin, hc.is_off)
						print(timestamp(), "\tFridge has constantly been working for too long, needs to be switched off for 15min.")
						state['alert_msg'] = "<H2>ALERT: The fridge has constantly been working for too long,<br>it needs to be switched off for 15min.<br></H2>" + str(timestamp())
						state_write(state)
						time.sleep(900) # 15 min. off
						int_par['intervalls_work'] = 0
						state['alert_msg'] = '-'
						state_write(state)
					state['state_onoff'] = 'on'
					hc.control_pin(hc.onoff_pin, hc.is_on)
					# Temp.-control: check temp. limits
					if float(config['temp_desired']) < float(int_par['temp_min']):
						config['temp_desired'] = str(int_par['temp_min'])
					elif float(config['temp_desired']) > float(int_par['temp_max']):
						config['temp_desired'] = str(int_par['temp_max'])
					# Temp.-control: control temp.
					if (float(state['temp_measured']) - float(int_par['temp_hysteresis'])) > float(config['temp_desired']):
						state['state_cooling'] = 'on'
						int_par['intervalls_work'] = int_par['intervalls_work'] + 1
						state['state_heating'] = 'off'
						hc.control_pin(hc.temp_en_pin, hc.is_on)
						hc.control_pin(hc.cooling_heating_pin, hc.is_off)
					elif (float(state['temp_measured']) + float(int_par['temp_hysteresis'])) < float(config['temp_desired']):
						state['state_cooling'] = 'off'
						int_par['intervalls_work'] = 0
						state['state_heating'] = 'on'
						hc.control_pin(hc.temp_en_pin, hc.is_on)
						hc.control_pin(hc.cooling_heating_pin, hc.is_on)
					else: # temp_measured within desired temp.-range
						state['state_cooling'] = 'off'
						int_par['intervalls_work'] = 0
						state['state_heating'] = 'off'
						hc.control_pin(hc.temp_en_pin, hc.is_off)

					# Light control:
					if timestamp_measurement_H_M > config['light_on_time']:
						if timestamp_measurement_H_M > config['light_off_time']:
							state['state_light'] = 'off'
							hc.control_pin(hc.light_pin, hc.is_off)
						else:
							state['state_light'] = 'on'
							hc.control_pin(hc.light_pin, hc.is_on)
					else:
						state['state_light'] = 'off'
						hc.control_pin(hc.light_pin, hc.is_off)

					# Update/Output control:
					if int_par['last_update'] < config['timestamp_request']:
						int_par['last_update'] = config['timestamp_request']
						print(timestamp(), "\tUpdate requested and data updated at: ", int_par['last_update'])
						datahandler.append_data_to_file()
						datahandler.update_graph('./static/data_log.png')
						cpf('./data/data.log', './static/data.log')
						state_write(state)
					# Measurement intervall
					time.sleep(int_par['intervall_measure'])
					
				datahandler.insert_data(state['timestamp_measurement'], state['temp_measured'], state['state_onoff'], state['state_light'], state['state_cooling'], state['state_heating']) # data logging intervall

			datahandler.append_data_to_file()
			datahandler.update_graph('./static/data_log.png')
			print(timestamp(), "\tMeasurement data automatically dumped to file")
			state_write(state)
		
	except KeyboardInterrupt:  # if 'Ctrl+C' is pressed
		print(timestamp(), "\tProgram aborted by user keyboard interrupt")
		datahandler.append_data_to_file()
		state_write(state)
		hc.cleanup()
