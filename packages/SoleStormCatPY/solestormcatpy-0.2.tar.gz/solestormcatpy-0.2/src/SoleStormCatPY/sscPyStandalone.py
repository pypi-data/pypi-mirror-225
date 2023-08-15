"""This is the standalone app for 'SoleStormCatPY'. Here, any user can use 'SoleStormCatPY' with little to no coding (Depends on if the user uses a script to open this script). Here is how you can make your own script to open this app:

import SoleStormCatPY.sscPyStandalone as SSCstand

SSCstand.fullPythonApp()
"""

import tkinter as tk

def fullPythonApp():
	window = tk.Tk()
	
	window.title('Python Operating Script Distribution')
	window.geometry('1024x768')
	
	appName = tk.Label(window, text = 'Welcome to "SoleStormCatPY"! Please choose an app below!')
	appName.pack()
	
	def WebGUI():
		import SoleStormCatPY.WebGUI
		
	WebB = tk.Button(window,text='Web', command=lambda: WebGUI())
	WebB.pack()
	
	def TerminalGUI():
		import SoleStormCatPY.TerminalGUI
	
	TerminalB = tk.Button(window,text='Terminal', command=lambda: TerminalGUI())
	TerminalB.pack()
	
	
	def SystemInfo():
		import SoleStormCatPY.SystemInfo as si
		si.systemPrint()
	
	SystemInfoB = tk.Button(window,text='System Info', command=lambda: SystemInfo())
	SystemInfoB.pack()
	
	
	def ClockTimerGUI():
		import SoleStormCatPY.ClockTimerGUI
		
	ClockTimerB = tk.Button(window,text='ClockTimer', command=lambda: ClockTimerGUI())
	ClockTimerB.pack()
	
	
	window.mainloop()
