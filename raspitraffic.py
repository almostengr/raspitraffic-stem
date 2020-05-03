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
TXTDISPLAY = "/tmp/traffic_display.txt"
TXTPSEUDO = "/tmp/traffic_pseudo.txt"

# display = lcddriver.lcd()
display = ""
displayState = "off"
displayStateOld = "off"
selection = ""
phaseflasher = 0
phasenum = 0
run_signal_flasher = "red"

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
	eblight(LAMPOFF, LAMPOFF, LAMPOFF)

	lcd_message("Done performing setup", "")


# LOG ADDITIONAL MESSAGES TO THE SCREEN/LOG FILE WHEN TESTING
def debug_message(message):
	if DEBUG == 1:
		log_message("DEBUG: " + message)


# print message on computer screen
def log_message(message):
	print message


# Displays the message on the LCD screen and computer screen
def lcd_message(line1, line2=''):
	if displayState == "on":
		display.lcd_clear()
		display.lcd_display_string(line1, 1)
		display.lcd_display_string(line2, 2)

	log_message(line1)
	log_message(line2)


# SEQUENCE FOR RED LIGHT GREEN LIGHT GAME.
def run_red_light_green_light(yellowon):

	# generate random values for red and green
	red_time = randint(1, 10)
	green_time = randint(1, 3)
	yellow_time = randint(0,2)

	# Turn on the red light and wait
	eblight(LAMPON, LAMPOFF, LAMPOFF)
	debug_message("Red Time: " + str(red_time))
	lcd_message("Red Light!", "Dont move!")
	sleep(red_time)

	# Turn on the green light and wait
	eblight(LAMPOFF, LAMPOFF, LAMPON)
	debug_message("Green Time: " + str(green_time))
	lcd_message("Green Light!", "Run!")
	sleep(green_time)

	if yellowon == 1:
	# if playing with yellow light, then turn on the yellow light
		eblight(LAMPOFF, LAMPON, LAMPOFF)
		debug_message("Yellow Time: " + str(yellow_time))
		lcd_message("Yellow Light!", "Slow!")
		sleep(yellow_time)


# runs the light using normal signal
def run_signal(country):
	phaseflasher = 0

	# generate random values for the lights to stay on
	east_grn_time = random.randint(5, 45)
	east_yel_time = random.randint(2, 5)
	east_red_time = random.randint(5, 45)

	# green light
	eblight(LAMPOFF, LAMPOFF, LAMPON)
	for ttime in range(east_grn_time, 0, -1):
		lcd_message("Green", "Time Remain: " + str(ttime) + "s")
		sleep(1)

        # flash green if selected
        if country.startswith("russia"):
            for i in range(randint(5,10), 0, -1):
                phaseflasher = run_flasher("green", phaseflasher)

	# yellow light
	eblight(LAMPOFF, LAMPON, LAMPOFF)
	for ttime in range(east_yel_time, 0, -1):
		lcd_message("Yellow", "Time Remain: " + str(ttime) + "s")
		sleep(1)

	# red light
	eblight(LAMPON, LAMPOFF, LAMPOFF)
	for ttime in range(east_red_time, 0, -1):
		lcd_message("Red", "Time Remain: " + str(ttime) + "s")
		sleep(1)

	# red-yellow for UK only
	if country.startswith("uk"):
		eblight(LAMPON, LAMPON, LAMPOFF)
		for ttime in range(east_yel_time, 0, -1):
			lcd_message("Red-Yellow", "Time Remain: " + str(ttime) + "s")
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
		flashrangemax = randint(6,30)
		for i in range(1,flashrangemax):
			phaseflasher = run_flasher(color, phaseflasher)


# randomly change the color to a different light(s)
def party_mode(phase, delay):
	if phase == 1:
		eblight(LAMPON, LAMPOFF, LAMPOFF)
	elif phase == 2:
		eblight(LAMPOFF, LAMPON, LAMPOFF)
	elif phase == 3:
		eblight(LAMPOFF, LAMPOFF, LAMPON)
	elif phase == 4:
		eblight(LAMPON, LAMPON, LAMPOFF)
	elif phase == 5:
		eblight(LAMPOFF, LAMPON, LAMPON)
	elif phase == 6:
		eblight(LAMPON, LAMPOFF, LAMPON)
	elif phase == 7:
		eblight(LAMPON, LAMPON, LAMPON)
	elif phase == 8:
		eblight(LAMPOFF, LAMPOFF, LAMPOFF)

	# delay between changing lights again
	sleep(delay)

	# reduce change of same phase being displayed twice in a row
	nextphase = randint(1,8)
	if nextphase == phase:
		nextphase = randint(1,3)

	return nextphase


# flash the lights with the color provided
def run_flasher(color, phase):

	if color == "red":
		if phase == 1:
			eblight(LAMPOFF, LAMPOFF, LAMPOFF)
			lcd_message("Flashing Red Off", "")
			phase = 2
		else:
			eblight(LAMPON, LAMPOFF, LAMPOFF)
			lcd_message("Flashing Red", "")
			phase = 1

	elif color == "yellow":
		if phase == 3:
			eblight(LAMPOFF, LAMPOFF, LAMPOFF)
			lcd_message("Flashing Yellow Off", "")
			phase = 4
		else:
			eblight(LAMPOFF, LAMPON, LAMPOFF)
			lcd_message("Flashing Yellow", "")
			phase = 3

	elif color == "green":
		if phase == 7:
			eblight(LAMPOFF, LAMPOFF, LAMPOFF)
			lcd_message("Flashing Green Off", "")
			phase = 8
		else:
			eblight(LAMPOFF, LAMPOFF, LAMPON)
			lcd_message("Flashing Green", "")
			phase = 7

	elif color == "all":
		if phase == 9:
			eblight(LAMPON, LAMPON, LAMPON)
			lcd_message("Flashing All", "")
			phase = 10
		else:
			eblight(LAMPOFF, LAMPOFF, LAMPOFF)
			lcd_message("Flashing All Off", "")
			phase = 9

	sleep(FLASHER_DELAY)
	return phase


# CALCULATE THE AMOUNT OF YELLOW LIGHT TIME
def calc_yellow_time(grade):
	speed = randint(25,80)
	yel_time = 1 + ((1.47 * speed) / (2 * (10 + (0 / 100) * 32.2)))
	return yel_time


# CONTROLS THE LAMPS ON THE EASTBOUND LIGHT.
def eblight(cirred, ciryel, cirgrn):
	GPIO.output(EAST_CR, cirred)
	GPIO.output(EAST_CY, ciryel)
	GPIO.output(EAST_CG, cirgrn)

	# print the status of each light
	# 1 = off, 0 = on
	debug_message("R: " + str(cirred) + " Y: " + str(ciryel) + " G: " + str(cirgrn))


# TURNS ON THE LIGHTS BASED ON THE ARGUMENT PROVIDED
def all_on(phase):

	# turn on all the lights
	if phase == "all":
		eblight(LAMPON, LAMPON, LAMPON)
		lcd_message("ALL LIGHTS ON", "")

	# turn on the red light
	elif phase == "red":
		eblight(LAMPON, LAMPOFF, LAMPOFF)
		lcd_message("ALL REDS ON", "")

	# turn on the red and yellow lights
	elif phase == "redyellow":
		eblight(LAMPON, LAMPON, LAMPOFF)
		lcd_message("ALL REDS AND", "YELLOW ON")

	# turn on the yellow light
	elif phase == "yellow":
		eblight(LAMPOFF, LAMPON, LAMPOFF)
		lcd_message("ALL YELLOWS ON", "")

	# turn of the yellow and green light
	elif phase == "yellowgreen":
		eblight(LAMPOFF, LAMPON, LAMPON)
		lcd_message("ALL YELLOW AND", "GREEN ON")

	# turn on the green light
	elif phase == "green":
		eblight(LAMPOFF, LAMPOFF, LAMPON)
		lcd_message("ALL GREENS ON", "")

	# turn on the green and red light
	elif phase == "greenred":
		eblight(LAMPON, LAMPOFF, LAMPON)
		lcd_message("ALL GREEN AND", "YELLOWS ON")

	# turn off all the lights
	elif phase == "off":
		eblight(LAMPOFF, LAMPOFF, LAMPOFF)
		lcd_message("ALL LIGHTS OFF", "")

	# do nothing
	else:
		log_message("Doing nothing")

	sleep(3)


# TURNS OFF ALL OF THE LIGHTS
def all_off():
	lcd_message("ALL LIGHTS OFF", "")
	eblight(LAMPOFF, LAMPOFF, LAMPOFF)
	sleep(3)


# process the pseudocode that has been entered
def process_pseudocode(command):
	returncode = 1

	# turn on the red light
	if command.startswith("red"):
		eblight(LAMPON, LAMPOFF, LAMPOFF)
		returnCode = 0

	# turn on the yellow light
	elif command.startswith("yellow"):
		eblight(LAMPOFF, LAMPON, LAMPOFF)
		returnCode = 0

	# turn on the green light
	elif command.startswith("green"):
		eblight(LAMPOFF, LAMPOFF, LAMPON)
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

	elif command.startswith("off"):
	# turn off all of the lights
		eblight(LAMPOFF, LAMPOFF, LAMPOFF)
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
			fileTraffic.close()

		try:
		# read the text display file
			fileDisplay = open(TXTDISPLAY, "r")
			displayState = fileDisplay.readline()
			fileDisplay.close()

		except IOError:
		# if the file doesn't exist, then create it and give public permissions
			fileDisplay = open(TXTDISPLAY, "w")
			subprocess.call(['chmod', '0777', TXTDISPLAY])
			fileDisplay.close()

		try:
		# read the psuedo code file
			filePseudo = open(TXTPSEUDO, "r")
			filePseudo.close()

		except IOError:
		# if the file doesn't exist, then create it and give public permissions
			filePseudo = open(TXTPSEUDO, "w")
			subprocess.call(['chmod', '0777', TXTPSEUDO])
			filePseudo.close()

		# controls whether to display output on the LCD
		if displayState == "on":
			display = lcddriver.lcd()
		else:
			display = ""

		if "traffic" in selection:
		# run the US traffic program
			run_signal(selection)

		elif selection == "all_on":
		# all lights on
			all_on("all")

		elif selection == "redon":
		# red on
			all_on("red")

		elif selection == "redyellowon":
		# red and yellow on
			all_on("redyellow")

		elif selection == "yellowon":
		# yellow on
			all_on("yellow")

		elif selection == "yellowgreenon":
		# yellow and green on
			all_on("yellowgreen")

		elif selection == "greenon":
		# green on
			all_on("green")

		elif selection == "greenredon":
		# green and red on
			all_on("greenred")

		elif selection == "all_off":
		# all lights off
			all_off()

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
					all_off()
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
			eblight(LAMPOFF, LAMPOFF, LAMPOFF)
			sleep(5)

		elif selection == "restart":
		# restart the Raspberry Pi
			subprocess.call(["sudo", "reboot"])

		elif selection == "shutdown":
		# shutdown the Raspberry Pi
			subprocess.call(["sudo", "shutdown", "-h", "now"])

		else:
		# If nothing selected or bad value, default to all on
			run_signal("ustrafficflasher")

except BaseException as e:
# perform action if exception occurs
	log_message("Exiting with exception")
	log_message(e)
	all_off()
	# GPIO.clean()
