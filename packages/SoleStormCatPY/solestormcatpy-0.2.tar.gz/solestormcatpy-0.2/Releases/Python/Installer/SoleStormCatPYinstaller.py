"""THIS INSTALLS 'SoleStormCatPY' VIA 'Python'. If you do not have Python, you may install it at python.org!"""

import os

ask = input('Do you want to install SoleStormCatPY onto your system? ("yes" or "no")     ')

if ask == 'yes':
	print('Downloading SoleStormCatPY from PyPi via pip, along with other required modules!')
	os.system('pip install SoleStormCatPY')
	os.system('pip install tkinter')
	os.system('pip install threading')
	os.system('pip install subprocess')
	os.system('pip install playsound')
	input('The modules of "SoleStormCatPY", "tkinter", "threading", "subprocess", and "playsound" were installed (if not already). Press Enter to exit!')
elif ask == 'no':
	input('No Changes Were Made To Your System. If you would like to install SoleStormCatPY, you may use this file, or run "pip install SoleStormCatPY" in your terminal!')
