"""This document opens a web browser. Here is an example code!:
import SoleStormCatPY.WebGUI as webgui
"""

"This imports certain requirements. This Requires 'tkinter' (The Tkinter for Python 3.X)"
import tkinter as tk





def webGUI():
	"This imports the 'webbrowser' module"
	import webbrowser
	
	website = inputtxt.get(1.0, "end-1c")
	
	"This if-elif statement shows how the website should load. I have specified special websites (shown below as if and elif), and all the user needs to enter is the name"
	if website == 'Python':
		print('Sending you to Python!')
		webbrowser.open('https://python.org')
	elif website == 'GitHub':
		print('Sending you to GitHub!')
		webbrowser.open('https://github.com')
	elif website == 'Google':
		print('Sending you to Google!')
		webbrowser.open('https://google.com')
	elif website == 'Bing':
		print('Sending you to Bing!')
		webbrowser.open('https://bing.com')
	elif website == 'Facebook':
		print('Sending you to Facebook!')
		webbrowser.open('https://facebook.com')
	elif website == 'Twitter':
		print('Sending you to Twitter!')
		webbrowser.open('https://twitter.com')
	elif website == 'ChunkBase':
		print('Sending you to ChunkBase!')
		webbrowser.open('https://chunkbase.com')
	elif website == 'Minecraft':
		print('Sending you to Minecraft!')
		webbrowser.open('https://minecraft.net')
	elif website == 'Roblox':
		print('Sending you to Roblox!')
		webbrowser.open('https://roblox.com')
	elif website == 'Microsoft 365':
		print('Sending you to Microsoft 365!')
		webbrowser.open('https://microsoft365.com')
	elif website == 'YouTube':
		print('Sending you to YouTube!')
		webbrowser.open('https://youtube.com')
	elif website == 'Quit':
		quit()
	elif website == 'Steam':
		print('Sending you to Steam!')
		webbrowser.open('https://store.steampowered.com')
	elif website == 'Walmart':
		print('Sending you to Walmart!')
		webbrowser.open('https://walmart.com')
	elif website == 'Amazon':
		print('Sending you to Amazon!')
		webbrowser.open('https://amazon.com')
	else:
		"This runs if the user's website is not in the list."
		print('Sending you to: ', website, '!')
		webbrowser.open(website)


frame = tk.Tk()
frame.title("Enter A Website URL")
frame.geometry('500x125')	
inputtxt = tk.Text(frame,
height = 1,
width = 45)

inputtxt.pack()
	
gotoWebButton = tk.Button(frame,
text = "Go To URL",
command = webGUI)
gotoWebButton.pack()
	
lbl = tk.Label(frame, text = "Enter a URL into the text box. Ensure that your URL contains 'http://'")
lbl.pack()
frame.mainloop()
