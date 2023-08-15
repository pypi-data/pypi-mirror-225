"""THIS IS THE GUI COUNTERPART OF 'ClockTimer'! HERE IS HOW TO USE:
import SoleStormCatPY.ClockTimerGUI
"""
import tkinter
from threading import Timer
from playsound import playsound

def timeout():
    frameEND = tkinter.Tk()
    frameEND.title('Timer, ENDED!')
    frameEND.geometry('500x500')
    
    lblEND = tkinter.Label(frameEND,
    text = "Your Timer Has Ended!")
    lblEND.pack()
    
    playsound('ClockTimerAssets//timerUP.wav')
    frameEND.mainloop()
    
def clockTimerGUI():
    timeSTR = inputtxt.get(1.0, 'end-1c')
    time = int(timeSTR)
    
    t = Timer(time, timeout)
    t.start()
    
    frameTime = tkinter.Tk()
    frameTime.title('Timer, Started')
    frameTime.geometry('500x500')
    
    lblTime = tkinter.Label(frameTime,
    text = "Your Timer Of:")
    lblTime.pack()
    
    lbltimeS = tkinter.Label(frameTime,
    text = timeSTR)
    lbltimeS.pack()
    
    lbltime1 = tkinter.Label(frameTime,
    text = "Seconds has started!")
    lbltime1.pack()
    
    frameTime.mainloop()
    
    t.join()
def clockTimerGUImin():
    timeSTR = inputtxt.get(1.0, "end-1c")
    time = int(timeSTR)
        
    t = Timer(time * 60, timeout)
    t.start()
    
    frameTime = tkinter.Tk()
    frameTime.title('Timer, Started')
    frameTime.geometry('500x500')
    
    lblTime = tkinter.Label(frameTime,
    text = "Your Timer Of:")
    lblTime.pack()
    
    lbltimeS = tkinter.Label(frameTime,
    text = timeSTR)
    lbltimeS.pack()
    
    lbltime1 = tkinter.Label(frameTime,
    text = "Minutes Has Started!")
    lbltime1.pack()
    
    frameTime.mainloop()
    
    t.join()
    
def clockTimerGUIhour():
    timeSTR = inputtxt.get(1.0, "end-1c")
    time = int(timeSTR)
    
    t = Timer(time * 3600, timeout)
    t.start()
    
    frameTime = tkinter.Tk()
    frameTime.title('Timer, Started')
    frameTime.geometry('500x500')
    
    lblTime = tkinter.Label(frameTime,
    text = "Your Timer Of:")
    lblTime.pack()
    
    lbltimeS = tkinter.Label(frameTime,
    text = timeSTR)
    lbltimeS.pack()
    
    lbltime1 = tkinter.Label(frameTime,
    text = "Hours Has Started!")
    lbltime1.pack()
    
    lbltimeD = tkinter.Label(frameTime,
    text = "DISCLAIMER: THIS WILL TAKE A WHILE!")
    lbltimeD.pack()
    
    frameTime.mainloop()
    t.join()

frame = tkinter.Tk()
frame.title('Timer')
frame.geometry('550x150')

inputtxt = tkinter.Text(frame,
height = 1,
width = 45)
inputtxt.pack()

startTimerButtonS = tkinter.Button(frame,
text = "Start Timer (Seconds)",
command = clockTimerGUI)
startTimerButtonS.pack()

startTimerButtonM = tkinter.Button(frame,
text = "Start Timer (Minutes)",
command = clockTimerGUImin)
startTimerButtonM.pack()

startTimerButtonH = tkinter.Button(frame,
text = "Start Timer (Hours)",
command = clockTimerGUIhour)
startTimerButtonH.pack()

lbl = tkinter.Label(frame,
text = "Enter your time in the box, then click the 'Start Timer' button that best fits you.")
lbl.pack()
frame.mainloop()
