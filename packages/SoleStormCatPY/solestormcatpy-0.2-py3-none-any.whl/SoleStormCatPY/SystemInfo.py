""" This gets/shows information about the user's system! Here is a way to use it:"
import SoleStormCatPY.SystemInfo as SystemInfo

SystemInfo.systemInfoPrint(deviceOS,userName,pythonVersion)


-This Gets the system info, but does not print it:

import SoleStormCatPY.SystemInfo as SystemInfo
SystemInfo.systemInfoFind()
"""

import os
import platform as pf


def systemInfoFind():
	"GETS THE SYSTEM INFO"
	deviceOS = pf.system()
	userName = os.getlogin()
	if deviceOS == "Windows":
		pythonVersion = os.system('python --version')
	else:
		pythonVersion = os.system('python3 --version')
	return deviceOS, userName, pythonVersion


def systemInfoPrint(deviceOS,userName,pythonVersion):
	"PRINTS THE SYSTEM INFO"
	deviceOS = systemInfoFind()
	userName = systemInfoFind()
	pythonVersion = systemInfoFind()
	
	print('The Current User OS is:  ')
	print(deviceOS)
	print(' ')
	print('The Current User is:   ')
	print(userName)
	print(' ')
	print('The Current Python Version is:   ')
	print(pythonVersion)




