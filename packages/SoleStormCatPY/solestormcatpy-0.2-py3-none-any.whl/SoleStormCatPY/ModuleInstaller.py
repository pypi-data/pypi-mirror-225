"""This checks to see if the modules required for SoleStormCatPY is installed. If not installed, the modules will be installed via 'pip' to run this installer:

import SoleStormCatPY.ModuleInstaller
"""
"Module os is required to use 'pip' to download modules"
import os

"This Checks for 'tkinter'"
try:
	import tkinter
	print('tkinter is installed!')
except ModuleNotFoundError:
	print('Module tkinter not found, installing!')
	os.system('pip install tkinter')


"This Checks for 'subprocess'"
try:
	import subprocess
	print('subprocess is installed!')
except ModuleNotFoundError:
	print("Module subprocess was not found, installing!")
	os.system('pip install subprocess')
	
"This Checks for 'threading'"
try:
	import threading
	print('threading is installed!')
except ModuleNotFoundError:
	print("Module threading was not found, installing!")
	os.system('pip install threading')
	
"This Checks for 'playsound'"
try:
	import playsound
	print('playsound is installed!')
except ModuleNotFoundError:
	print("Module 'playsound' was not found, installing!")
	os.system('pip install playsound')
