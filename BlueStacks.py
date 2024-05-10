from constants import *
import pyautogui, os, subprocess, pathlib

def Find_Image(img,val = 0.9,low_limit = 0.701):
	print("Locating " + img)
	#path = "C:\\Users\\georg\\Documents\\PythonScripts\\AutoClickerProject\\Idle_Heroes\\Images\\"
	path = path = os.path.dirname(os.path.abspath(__file__)) + "\\Images\\"
	#val = 0.9
	#low_limit = 0.7
	while val > low_limit:
		print("confidence: " + str(val))
		try:
			x,y = pyautogui.locateCenterOnScreen(path + img +'.png', confidence = val,grayscale =False)
			pyautogui.moveTo(x,y)
			print("x: " + str(x))
			print("y: " + str(y))
			return True
		except TypeError:
			print("Cannot find " + img)
		val -= 0.1
		round(val,2)
	return False