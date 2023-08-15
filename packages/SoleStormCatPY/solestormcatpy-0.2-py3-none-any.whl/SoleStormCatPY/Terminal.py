"""This brings the user's terminal into your Python script. Run any command you want. In this example, the user will enter their command:

import SoleStormCatPY.Terminal as cmd

command = input('''What command do you want the system to run?
''')

cmd.terminalrun(command)

This example runs your custom commands:

import SoleStormCatPY.terminal as cmd

command = 'pip list'
cmd.terminalrun(command)
"""

"This Imports the 'os' Module, which is used to run system commands!"
import os

"This Runs the command specified!"
def terminalrun(command):
	os.system(command)
