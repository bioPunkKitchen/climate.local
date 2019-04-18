#!/usr/bin/env python3
import datetime
import time
import os
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np


class handle_data:
	data_file = "./data/data.log"
	data_list = []


	def __init__(self):
		pass
		

	def insert_data(self, timestamp, temp, state_onoff, state_light, state_cooling, state_heating):
		"""
		Insert data to log file and add timestamp.
		"""
		if state_onoff == 'on':
			state_onoff = 1
		else:
			state_onoff = 0

		if state_light == 'on':
			state_light = 1
		else:
			state_light = 0

		if state_cooling == 'on':
			state_cooling = 1
		else:
			state_cooling = 0

		if state_heating == 'on':
			state_heating = 1
		else:
			state_heating = 0

		data_string = str(timestamp) + ";" + str(temp) + ";" + str(state_onoff) + ";" + str(state_light) + ";" + str(state_cooling) + ";" + str(state_heating) + "\n"
		self.data_list.append(data_string)
		#print(datetime.datetime.now().strftime('%Y-%m-%d_%a_%H:%M:%S.%f'), "\tInserted data: data_list.append len=", len(self.data_list))
		return


	def append_data_to_file(self):
		"""
		Append data to log file.
		"""
		try:
			with open(self.data_file, "a") as outfile:
				for entry in self.data_list:
					outfile.write(str(entry))
		except IOError: 
			print(datetime.datetime.now().strftime('%Y-%m-%d_%a_%H:%M:%S.%f'), "\tIOError opening data.log for appending data")
		self.data_list.clear()
		return


	def clean_file(self):
		"""
		Clean log file in order to reset measurement.
		"""
		try:
			with open(self.data_file, "w") as outfile:
				outfile.write("Timestamp; Temp; State_onoff; State_light; State_cooling; State_heating\n")
		except IOError: 
			print(datetime.datetime.now().strftime('%Y-%m-%d_%a_%H:%M:%S.%f'), "\tIOError opening data.log for writing")
		return


	def update_graph(self, path):
		"""
		Generate or update graph from data file.
		"""
		lines = sum(1 for _ in open(self.data_file))
		if lines > 1:
			data=np.genfromtxt(self.data_file, delimiter=';', skip_header=1, names=['Time', 'Temp', 'Onoff', 'Light', 'Cooling', 'Heating'], dtype=([('Time', '<U30'), ('Temp', '<f8'), ('Onoff', '<f8'), ('Light', '<f8'), ('Cooling', '<f8'), ('Heating', '<f8')]))
			fig, ax1 = plt.subplots()
			if data['Temp'].shape:
				if data['Temp'].shape[0] > 120:
					ax1.plot(data['Temp'][((data['Temp'].shape[0])-120):(data['Temp'].shape[0])], color = 'r', label = 'Temp.')
				else:
					ax1.plot(data['Temp'], color = 'r', label = 'Temp.')
			else:
				ax1.plot(data['Temp'], color = 'r', label = 'Temp.')
			
			ax1.set_xlim([0,120])
			ax1.set_xticks([0,30,60,90,120])
			ax1.set_ylabel('Temp (°C)', color='r')
			ax1.tick_params('y', colors='r')
			yt=range(-1,41,1)
			ax1.set_yticks(yt, minor=True)
			ax1.set_xlabel('last two hours (scale:min.)')
			"""	
			ax2 = ax1.twinx()
			ax2.plot(data['Light'], color = 'g', label = 'Light', marker = 'o')
			ax2.plot(data['Onoff'], color = 'y', label = 'Onoff', marker = '*')
			ax2.plot(data['Heating'], color = 'r', label = 'Heating')
			ax2.plot(data['Cooling'], color = 'b', label = 'Cooling')
			ax2.set_ylabel('Light (on=1/off=0)', color='b')
			ax2.tick_params('y', colors='b')
			ax2.set_yticks([0,1], minor=False)
			"""
			fig.tight_layout()
			#plt.legend(['Temp. inside'], loc='upper left')
			plt.savefig(path, bbox_inches='tight')
			plt.close(fig)
			print(datetime.datetime.now().strftime('%Y-%m-%d_%a_%H:%M:%S.%f'), "\tGraph generated/updated.")
		else:
			#os.remove(path)
			#os.mknod(path)
			#os.chmod(path, 0o644)
			try:
				with open(path, "w") as outfile:
					outfile.write("")
			except IOError: 
				print(datetime.datetime.now().strftime('%Y-%m-%d_%a_%H:%M:%S.%f'), "\tIOError: Could not generate empty graph file.")
			print(datetime.datetime.now().strftime('%Y-%m-%d_%a_%H:%M:%S.%f'), "\tNo data, graph is empty.")
		return


# Test:
if __name__ == '__main__':
	hd = handle_data()
	#hd.clean_file()
	hd.update_graph('./static/data_log.png')
