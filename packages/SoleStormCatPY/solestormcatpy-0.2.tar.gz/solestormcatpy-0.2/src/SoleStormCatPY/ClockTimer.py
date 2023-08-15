"""THIS APPLICATION HELPS A USER MAKE AN TIMER IN THE TERMINAL. TO RUN (DO NOT CHANGE THE 'minutes' WITHIN 'timer.clockTimer()':
import SoleStormCatPY.ClockTimer as timer

timer.clockTimer(minutes)
"""
"""TO MANUALLY RUN THE TIMER BY THE DEVELOPER, RUN:
import SoleStormCatPY.ClockTimer as timer

seconds = {"HOW MANY SECONDS YOU WANT. IF YOU REQUIRE MINUTES, USE "{minutes} * 60"}
timer.clockTimerManual(seconds)
"""

from threading import Timer
import subprocess
from playsound import playsound

def timeout():
    print("Finished Timer!")
    playsound('ClockTimerAssets//timerUP.wav')

def getNum():
    minutesSTR = input('How Many Minutes do you require?     ')
    minutes = int(minutesSTR)
    return minutes

def clockTimerSETUP(minutes):
    t = Timer(minutes * 60, timeout)
    t.start()
    print('Waiting for timer of ',minutes,' minutes to complete!')
    
    t.join()
    
def clockTimerManual(seconds):
    t = Timer(seconds, timeout)
    t.start()
    print('Waiting for timer of ',seconds,' seconds to complete!')
    
    t.join()
    
def clockTimer():
    minutes = getNum()
    clockTimerSETUP(minutes)
