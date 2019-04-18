#!/usr/bin/env python3
import RPi.GPIO as GPIO
import datetime
import time
import os
"""
                                                     / o---Cooling
                                  / o---x   |-----o-/
                           |---o-/          |          o---Heating (relais light on)
                           |        o-------|    Relais4
                           |  Relais3
                           |
           / o---x OFF     |
230V ---o-/                |      / o---x
             o--- ON ------|---o-/
                                    o---Light (25A light relais)
         Relais1              Relais2
"""

class hardware_control:
	# Relais control:
	onoff_pin = 6# Relais1, black
	light_pin = 13 # Relais2, white
	temp_en_pin = 19 # Relais3, blue
	cooling_heating_pin = 26 # Relais4, red
	is_on = GPIO.HIGH
	is_off = GPIO.LOW


	def __init__(self):
		pass


	def hw_setup(self):
		GPIO.setmode(GPIO.BCM) # alternative: GPIO.BOARD
		GPIO.setup(hardware_control.onoff_pin, GPIO.OUT)
		GPIO.output(hardware_control.onoff_pin, hardware_control.is_off)
		GPIO.setup(hardware_control.light_pin, GPIO.OUT)
		GPIO.output(hardware_control.light_pin, hardware_control.is_off)
		GPIO.setup(hardware_control.temp_en_pin, GPIO.OUT)
		GPIO.output(hardware_control.temp_en_pin, hardware_control.is_off)
		GPIO.setup(hardware_control.cooling_heating_pin, GPIO.OUT)
		GPIO.output(hardware_control.cooling_heating_pin, hardware_control.is_off)
		return


	def control_pin(self, pin, state):
		GPIO.output(pin, state)
		return


	def cleanup(self):
		"""
		hc = hardware_control.hardware_control()
		...
		try:
		...
		except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		print("Program aborted by user keyboard interrupt")
		hc.cleanup()
		"""
		print("Cleaning up RasPi GPIO.")
		GPIO.cleanup()  # Release resource
		print("Cleaning up RasPi GPIO finished. Bye.")
		return
