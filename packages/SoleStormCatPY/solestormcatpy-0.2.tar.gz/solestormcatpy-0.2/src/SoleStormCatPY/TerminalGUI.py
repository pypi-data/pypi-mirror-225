"""This brings the user's terminal into your Python script in a GUI, allowing the user to enter whatever command they'll like! You Can Run This:
import SoleStormCatPY.TerminalGUI
"""

"Imports 'tkinter' and 'os'"
import os
import tkinter as tk


def terminalGUI():
	command = inputtxt.get(1.0, "end-1c")
	
	"This shows the command output into the terminal"
	os.system(command)

frame = tk.Tk()
frame.title("Enter A Command")
frame.geometry('500x125')	
inputtxt = tk.Text(frame,
height = 1,
width = 45)

inputtxt.pack()
	
gotoTerminalButton = tk.Button(frame,
text = "Run Command",
command = terminalGUI)
gotoTerminalButton.pack()
	
lbl = tk.Label(frame, text = "Enter a Terminal Command into the Box")
lbl.pack()
frame.mainloop()
