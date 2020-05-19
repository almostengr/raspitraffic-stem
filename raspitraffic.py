#!/usr/bin/python

################################################################################
# Project: Raspi Traffic Control
# Script Usage: raspitraffic.py
# Created: 2017-04-02
# Author: Kenny Robinson, @almostengr, thealmostengineer.com
# Description: Core script which all the functions for controlling the lights
# are contained.
################################################################################

from time import sleep
from random import randint
import RPi.GPIO as GPIO
import lcddriver
import random
import subprocess

# DEBUGGING MODE, DISABLED = 0, ENABLED = 1
DEBUG = 0

# DEFINE THE GPIO NUMBERS AND VARIABLES FOR THE EASTBOUND TRAFFIC
EAST_CR = 23
EAST_CY = 21
EAST_CG = 19

PINOUTLIST = [EAST_CR, EAST_CY, EAST_CG]

# DEFINE ADDITIONAL CONSTANTS
LAMPON = GPIO.LOW
LAMPOFF = GPIO.HIGH
FLASHER_DELAY = .7
TXTTRAFFIC = "/tmp/traffic.txt"
TXTPSEUDO = "/tmp/traffic_pseudo.txt"

display = lcddriver.lcd()
selection = ""
phaseflasher = 0

# SET UP GPIO PINS
def setup():
	GPIO.setmode(GPIO.BOARD)

	# disable GPIO warnings when not debugging
	if DEBUG == 0:
		GPIO.setwarnings(False)

	# loop through each of the pins and define it.
	for i in PINOUTLIST:
	 	debug_message("Setting up and activiating pin " + str(i))
	 	GPIO.setup(i, GPIO.OUT)

	# turn off all the lights
	thesignal(LAMPOFF, LAMPOFF, LAMPOFF)

	lcd_message("Setup Complete")


# LOG ADDITIONAL MESSAGES TO THE SCREEN/LOG FILE WHEN TESTING
def debug_message(message):
	if DEBUG == 1:
		log_message("DEBUG: " + message)


# print message on computer screen
def log_message(message):
	print message


# Displays the message on the LCD screen and computer screen
# Pad the display to make sure that it does have 16 characters
def lcd_message(line1, line2=''):
	if display != "":
		line2=line1 + " " + line2
		line2=line2.ljust(16)

		programstr="PG:" + selection
		programstr=programstr.ljust(16)

		display.lcd_display_string(programstr, 1)
		display.lcd_display_string(line2, 2)

	log_message(line1 + " " + line2)


# SEQUENCE FOR RED LIGHT GREEN LIGHT GAME.
def run_red_light_green_light(yellowon):

	# generate random values for red and green
	red_time = randint(1, 10)
	yellow_time = randint(0,2)
	green_time = randint(1, 3)

	# Turn on the red light and wait
	thesignal(LAMPON, LAMPOFF, LAMPOFF)
	debug_message("Red Time: " + str(red_time))
	lcd_message("Red!", "Dont move!")
	sleep(red_time)

	# Turn on the green light and wait
	thesignal(LAMPOFF, LAMPOFF, LAMPON)
	debug_message("Green Time: " + str(green_time))
	lcd_message("Green!", "Run!")
	sleep(green_time)

	# if playing with yellow light, then turn on the yellow light
	if yellowon == 1:
		thesignal(LAMPOFF, LAMPON, LAMPOFF)
		debug_message("Yellow Time: " + str(yellow_time))
		lcd_message("Yellow!", "Slow!")
		sleep(yellow_time)


# runs the light using normal signal
def run_signal(country):
	phaseflasher = 0

	# generate random values for the lights to stay on
	east_grn_time = random.randint(5, 45)
	east_yel_time = random.randint(2, 5)
	east_red_time = random.randint(5, 45)

	# green light
	thesignal(LAMPOFF, LAMPOFF, LAMPON)
	for ttime in range(east_grn_time, 0, -1):
		lcd_message("Green", "Time: " + str(ttime) + "s")
		sleep(1)

        # flash green if selected
        if country.startswith("russia"):
            for i in range(randint(5,10), 0, -1):
                phaseflasher = run_flasher("green", phaseflasher)

	# yellow light
	thesignal(LAMPOFF, LAMPON, LAMPOFF)
	for ttime in range(east_yel_time, 0, -1):
		lcd_message("Yellow", "Time: " + str(ttime) + "s")
		sleep(1)

	# red light
	thesignal(LAMPON, LAMPOFF, LAMPOFF)
	for ttime in range(east_red_time, 0, -1):
		lcd_message("Red", "Time: " + str(ttime) + "s")
		sleep(1)

	# red-yellow for UK only
	if country.startswith("uk"):
		thesignal(LAMPON, LAMPON, LAMPOFF)
		for ttime in range(east_yel_time, 0, -1):
			lcd_message("Red-Yel", "Time: " + str(ttime) + "s")
			sleep(1)

	# perform flashing if selected
	if country.endswith("flasher"):

		# pick a color to flash
		colorint = randint(0,10)
		if colorint < 5:
			color = "red"
		else:
			color = "yellow"

		# perform the flashing
		flashrangemax = randint(6,50)
		for i in range(1,flashrangemax):
			phaseflasher = run_flasher(color, phaseflasher)


# randomly change the color to a different light(s)
def party_mode(phase, delay):
	display.lcd_clear()

	if phase == 1:
		thesignal(LAMPON, LAMPOFF, LAMPOFF)
	elif phase == 2:
		thesignal(LAMPOFF, LAMPON, LAMPOFF)
	elif phase == 3:
		thesignal(LAMPOFF, LAMPOFF, LAMPON)
	elif phase == 4:
		thesignal(LAMPON, LAMPON, LAMPOFF)
	elif phase == 5:
		thesignal(LAMPOFF, LAMPON, LAMPON)
	elif phase == 6:
		thesignal(LAMPON, LAMPOFF, LAMPON)
	elif phase == 7:
		thesignal(LAMPON, LAMPON, LAMPON)
	elif phase == 8:
		thesignal(LAMPOFF, LAMPOFF, LAMPOFF)

	# delay between changing lights again
	sleep(delay)

	# reduce change of same phase being displayed twice in a row
	nextphase = randint(1,7)
	if nextphase == phase:
		nextphase = 8

	return nextphase


# flash the lights with the color provided
def run_flasher(color, phase):

	if color == "red":
		lcd_message("Flash Red", "")
		if phase == 1:
			thesignal(LAMPOFF, LAMPOFF, LAMPOFF)
			phase = 2
		else:
			thesignal(LAMPON, LAMPOFF, LAMPOFF)
			phase = 1

	elif color == "yellow":
		if phase == 3:
			lcd_message("Flash Yellow", "")
			thesignal(LAMPOFF, LAMPOFF, LAMPOFF)
			phase = 4
		else:
			thesignal(LAMPOFF, LAMPON, LAMPOFF)
			phase = 3

	elif color == "green":
		lcd_message("Flash Green", "")
		if phase == 7:
			thesignal(LAMPOFF, LAMPOFF, LAMPOFF)
			phase = 8
		else:
			thesignal(LAMPOFF, LAMPOFF, LAMPON)
			phase = 7

	elif color == "all":
		lcd_message("Flash All", "")
		if phase == 9:
			thesignal(LAMPON, LAMPON, LAMPON)
			phase = 10
		else:
			thesignal(LAMPOFF, LAMPOFF, LAMPOFF)
			phase = 9

	sleep(FLASHER_DELAY)
	return phase


# CALCULATE THE AMOUNT OF YELLOW LIGHT TIME
def calc_yellow_time(grade):
	speed = randint(25,80)
	yel_time = 1 + ((1.47 * speed) / (2 * (10 + (0 / 100) * 32.2)))
	return yel_time


# CONTROLS THE LAMPS ON THE EASTBOUND LIGHT.
def thesignal(cirred, ciryel, cirgrn):
	GPIO.output(EAST_CR, cirred)
	GPIO.output(EAST_CY, ciryel)
	GPIO.output(EAST_CG, cirgrn)

	# print the status of each light
	# 1 = off, 0 = on
	debug_message("R: " + str(cirred) + " Y: " + str(ciryel) + " G: " + str(cirgrn))


# TURNS ON THE LIGHTS BASED ON THE ARGUMENT PROVIDED
def light_and_hold(phase):

	# turn on all the lights
	if phase == "all":
		thesignal(LAMPON, LAMPON, LAMPON)

	# turn on the red light
	elif phase == "red":
		thesignal(LAMPON, LAMPOFF, LAMPOFF)

	# turn on the red and yellow lights
	elif phase == "redyellow":
		thesignal(LAMPON, LAMPON, LAMPOFF)

	# turn on the yellow light
	elif phase == "yellow":
		thesignal(LAMPOFF, LAMPON, LAMPOFF)

	# turn of the yellow and green light
	elif phase == "yellowgreen":
		thesignal(LAMPOFF, LAMPON, LAMPON)

	# turn on the green light
	elif phase == "green":
		thesignal(LAMPOFF, LAMPOFF, LAMPON)

	# turn on the green and red light
	elif phase == "greenred":
		thesignal(LAMPON, LAMPOFF, LAMPON)

	# turn off all the lights
	elif phase == "off":
		thesignal(LAMPOFF, LAMPOFF, LAMPOFF)

	# do nothing
	else:
		log_message("Doing nothing")

	sleep(5)


# process the pseudocode that has been entered
def process_pseudocode(command):
	returncode = 1

	# turn on the red light
	if command.startswith("red"):
		thesignal(LAMPON, LAMPOFF, LAMPOFF)
		returnCode = 0

	# turn on the yellow light
	elif command.startswith("yellow"):
		thesignal(LAMPOFF, LAMPON, LAMPOFF)
		returnCode = 0

	# turn on the green light
	elif command.startswith("green"):
		thesignal(LAMPOFF, LAMPOFF, LAMPON)
		returnCode = 0

	# sleep for the specified duration
	elif command.startswith("wait"):
		waittime = float(command[5:7])
		debug_message("Waiting " + str(waittime))
		sleep(waittime)
		returnCode = 0

	# repeat reading the file
	elif command.startswith("repeat"):
		returnCode = 0

	# turn off all of the lights
	elif command.startswith("off"):
		thesignal(LAMPOFF, LAMPOFF, LAMPOFF)
		returnCode = 0

	# mention that exception occurred and exit
	else:
		log_message("Exception occurred")
		returnCode = 1

	return returnCode


# Update the status so that the message doesnt repeat
def pseudowait():
	log_message("Updating pseudo status")
	fileTraffic2 = open(TXTTRAFFIC, 'w')
	fileTraffic2.write("pseudowait")
	fileTraffic2.close()


# configure everything
setup()

debug_message("Debug mode enabled")

try:
	while True:
		log_message("Reading files")
		debug_message(display)

		try:
		# Read the program file
			fileTraffic = open(TXTTRAFFIC, "r")
			selection = fileTraffic.readline()
			fileTraffic.close()

		except IOError:
		# if the file doesn't exist, then create it and give public permissions
			fileTraffic = open(TXTTRAFFIC, "w")

			# chmod 0777 /tmp/traffic.txt
			subprocess.call(['chmod', '0777', TXTTRAFFIC])
			fileTraffic.write("ustrafficflasher")
			fileTraffic.close()

		try:
		# read the psuedo code file
			filePseudo = open(TXTPSEUDO, "r")
			filePseudo.close()

		except IOError:
		# if the file doesn't exist, then create it and give public permissions
			filePseudo = open(TXTPSEUDO, "w")
			subprocess.call(['chmod', '0777', TXTPSEUDO])
			filePseudo.close()

		debug_message(display)
		log_message("Done reading")

		if "traffic" in selection:
		# run the US traffic program
			run_signal(selection)

		elif selection == "all_on":
		# all lights on
			light_and_hold("all")

		elif selection == "redon":
		# red on
			light_and_hold("red")

		elif selection == "redyellowon":
		# red and yellow on
			light_and_hold("redyellow")

		elif selection == "yellowon":
		# yellow on
			light_and_hold("yellow")

		elif selection == "yellowgreenon":
		# yellow and green on
			light_and_hold("yellowgreen")

		elif selection == "greenon":
		# green on
			light_and_hold("green")

		elif selection == "greenredon":
		# green and red on
			light_and_hold("greenred")

		elif selection == "all_off":
		# all lights off
			light_and_hold("off")

		elif selection == "flashred":
		# flash red
			phaseflasher = run_flasher("red", phaseflasher)

		elif selection == "flashyel":
		# flash yellow
			phaseflasher = run_flasher("yellow", phaseflasher)

		elif selection == "flashgrn":
		# flash green
			phaseflasher = run_flasher("green", phaseflasher)

		elif selection == "redlightgreenlight":
		# red light, green light
			run_red_light_green_light(0)

		elif selection == "redlightgreenlight2":
		# red light, green light, with yellow
			run_red_light_green_light(1)

		elif selection == "partymode4":
		# slower party mode
			phaseflasher = party_mode(phaseflasher, 2)

		elif selection == "partymode":
		# party mode
			phaseflasher = party_mode(phaseflasher, 1)

		elif selection == "partymode2":
		# party mode, but faster
			phaseflasher = party_mode(phaseflasher, 0.5)

		elif selection == "partymode3":
		# party mode, but fastest
			phaseflasher = party_mode(phaseflasher, 0.25)

		elif selection == "pseudocode":
		# Read and attempt to process the sudo code
			lastline = ""
			pseudofile = open(TXTPSEUDO, 'rb')
			for line in pseudofile:
				debug_message("Line reads: " + line)

				# do something with data
				pseudoReturn = process_pseudocode(line)
				lastline = line
				debug_message("pseudoReturn: " + str(pseudoReturn))

				if pseudoReturn == 1:
				# exit if the value returned equals one
					debug_message("Exiting")
					light_and_hold("off")
					pseudowait()
					break
			else:
				if lastline == "repeat":
				# repeat the phase if the last line states repeat
					False
				else:
				# go into waiting state if last line isnt repeat
					pseudowait()

			# close the file when done
			pseudofile.close()

		elif selection == "pseudowait":
		# if there was a failure previously, then dont do anything until updated
			debug_message("Waiting on pseudocode to be updated")
			thesignal(LAMPOFF, LAMPOFF, LAMPOFF)
			sleep(5)

		elif selection == "restart":
		# restart the Raspberry Pi
			subprocess.call(["sudo", "reboot"])

		elif selection == "shutdown":
		# shutdown the Raspberry Pi
			subprocess.call(["sudo", "shutdown", "-h", "now"])

		else:
		# If nothing selected or bad value, default to all on
			log_message("File empty")

except BaseException as e:
# perform action if exception occurs
	log_message("Exiting with exception")
	log_message(e)
	light_and_hold("off")
	display.lcd_clear()
