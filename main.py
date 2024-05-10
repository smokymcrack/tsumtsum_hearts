from BlueStacks import *
from pyautogui_debug import *
from AppOpener import open
import pyautogui, os, subprocess, pathlib
import time
import schedule
import logging
import psutil

state = 0
schedule_delay = 62; #delay for the scheduler in minutes
click_delay = 2 # delay after clicking in seconds
def __main__():
	global state, no_hearts_flag,exit_flag
	try:
		t = time.localtime()
		current_time = time.strftime("%H:%M:%S", t)
		print("START TIME: " + str(current_time))
		print("START STATE MACHINE \n")
		state = 0 
		no_hearts_flag = 0
		exit_flag = 0
		state_machine()
		print("EXIT STATE MACHINE\n")
	except Exception as e:
		print(f"An error occurred: {str(e)}")
	return


def open_tsumtsum_app():
	os.startfile("C:\\Users\\Mao\\Documents\\Projects\\tsumtsum\\TsumTsum.lnk")
	time.sleep(12)
	pyautogui.press('F11')
	pyautogui.press('tab')
	pyautogui.press('tab')
	pyautogui.press('enter')
	delay_cntr = 0
	while (delay_cntr < 4):
		pyautogui.press('esc')
		time.sleep(2)
		delay_cntr += 1

	pyautogui.press('F11')
	time.sleep(5)
	while(not(Find_Image("TAP_TO_START"))):
		if (Find_Image("BLUESTACKS_ICON")):
			click()
			click()
			pyautogui.press('F11')
		time.sleep(3)
	click()
	time.sleep(15)
	return

def close_tsumtsum_app():
	close_process_by_name('HD-Player.exe')		#BlueStacks 5 App name
	
def close_process_by_name(process_name):
    os.system(f"taskkill /f /im \"{process_name}\"")


def task():
	try: 
		state_machine()
	except Exception as e:
		print(f"An error occurred: {str(e)}")


state = 0
no_hearts_flag = 0
exit_flag = 0
def state_machine():
	global state, no_hearts_flag, exit_flag

	state = 0
	no_hearts_flag = 0

	while(exit_flag == 0):
		time.sleep(2)
		if(state == 0):
			__init__()
		elif(state == 1):
			state_1()
		elif(state == 5):
			state_5()
		elif(state == 6):
			state_6()
	return


def state_1():
	global state,no_hearts_flag
	print ("----------------------------")
	print("STATE 1 - SEND HEARTS STATE")
	print ("----------------------------\n")
	if(send_hearts()):
		click()
		if(Find_Image('OK')):
			click()
			click()
			no_hearts_flag = 0
	else:
		if(Find_Image("ROW_OF_HEARTS")):
			if(not(Find_Image("EARN_COINS"))):

				height = 1920
				width = 1080
				pyautogui.moveTo(height / 2, width / 2)
				pyautogui.scroll(-50)
				time.sleep(2)
				pyautogui.press('F11')
				pyautogui.press('F11')
				time.sleep(2)
			else:
				state = 6
		else:
			state = 5	#go to error state
	return


def state_5():
	global state,no_hearts_flag
	print ("-----------------------")
	print("STATE 5 - ERROR STATE")
	print ("-----------------------\n")
	if(Find_Image("CLOSE")):
		click()
	elif(Find_Image("CANCEL")):
		click()
	elif(Find_Image("BACK")):
		click()
	elif(Find_Image("ROW_OF_HEARTS")):
		reset_screen()
		state = 1
	else:
		if (no_hearts_flag < 4):
			no_hearts_flag += 1
		else:
			no_hearts_flag = 0
			state = 6
	return

def state_6():
	global state,no_hearts_flag, exit_flag
	print ("-----------------------")
	print("STATE 6 - RESTART STATE")
	print ("-----------------------\n")

	if(Find_Image("ROW_OF_HEARTS")):		#exit if we see a row of hearts, but no hearts
		exit_flag = 1
		close_tsumtsum_app()
	else:
		state = 0

	return
	


def Find_Image(img,val = 0.9,low_limit = 0.601): #original low_limit 0.701
	print("Locating " + img)
	path = path = os.path.dirname(os.path.abspath(__file__)) + "\\Images\\"
	#val = 0.9
	#low_limit = 0.7
	while val > low_limit:
		print("confidence: " + str(val))
		try:
			x,y = pyautogui.locateCenterOnScreen(path + img +'.png', confidence = val,grayscale =False)
			pyautogui.moveTo(x,y)
			print("x: " + str(x))
			print("y: " + str(y) + "\n")
			return True
		except TypeError:
			print("Cannot find " + img + "\n")
		val -= 0.1
		round(val,2)
	return False


def __init__():
	global state,no_hearts_flag
	print ("----------------")
	print("INITIALIZING....")
	print ("----------------\n")
	if(not(Find_Image("ROW_OF_HEARTS"))):
		close_tsumtsum_app()
		open_tsumtsum_app()
	state = 5

	print ("------------------------")
	print("INITIALIZATION COMPLETE!")
	print ("------------------------\n")
	return

#Function to reset the screen to initial heart-sending screen
def reset_screen():
	pyautogui.press('F11')
	pyautogui.press('F11')
	time.sleep(2)
	if Find_Image('PLAY'):
		click()
		if Find_Image('BACK'):
			click()
			if Find_Image('EARN_COINS'):
				pyautogui.scroll(200)
				time.sleep(2)
	return
	  

	  
#Function to check whether the HEART icon is on the screen
def send_hearts():
	if(Find_Image('HEART')):
		return True
	return False


#Function to simulate click with a 2s delay afterwards
def click():
	pyautogui.click()
	time.sleep(click_delay)
	return

def full_screen():
	pyautogui.press('f11')


__main__()
schedule.every(schedule_delay).minutes.do(__main__)
#__main__()

while True:
	schedule.run_pending()
	time.sleep(1)