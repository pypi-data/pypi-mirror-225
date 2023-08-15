# SoleStormCatPY

SoleStormCatPY is an app developed to help you throughout your day. Here are some of the apps that are jam-packed into this Python Distribution Package!

## ModuleInstaller
This is not an app, but instead, you can run this inside Python to insure that you have everything that is required to run SoleStormCatPY! (Unless you only use the executables, then this dosn't apply to you)
In your terminal, you must open your Python by using `python` on Windows, or `python3` on MacOS and Linux. Then run `import SoleStormCatPY.ModuleInstaller`, and the application will check for the required modules. If they are found on your local device, it'll show a conframation, but if they are not installed, this application will install them for you.

## MathSolver

"MathSolver" seems just like it sounds. A calculator. A boring old calculator. You've seen many apps (the even come built in to your device) that work like this, but "MathSolver" is made to help with your daily math needs. "MathSolver" can do math ranging from Multiplication, Division, Adding, and Subtracting!

### How To Use
To Run "MathSolver" in your script, make sure to specify `num1` (Being the first number), `num2` (being your second number), and `ty` (being the type of math you require), along with the command `{However you specify "MathSolver"}.numPrint(num1, num2, ty)`.

Have Fun Mathing!

## Web

"Web" is not as it might see. It's not a web browser, but a web browser opener! You enter the URL of the website you want (including `http://`), and you'll be sent to the website. And, you also get to put in names for specific websites that lead to them with only the name!

### The Two Types of "Web"

Yes, there are two versions of "Web"! There is "WebGUI" (With GUI), and "WebCMD" (With No GUI, Just Terminal). Here are their differences!

WebGUI:
WebGUI opens in a `tkinter` window, allowing users to enter their URL into a user-friendly box! (Requires the `tkinter` module)

WebCMD:
WebCMD opens in the standard terminal window, this is great for opening a website the developer wants! (THIS WILL NOT WORK WITH `.pyw` FILES!)

### How To Use
To Run "Web" in your script, make sure to specify `website` (being the URL (or name in some cases)), along with the command `{However you specify "WebCMD"}.webCMD(website)` (For WebCMD. Requires `website`), or `import SoleStormCatPY.WebGUI` (For WebGUI. Will NOT use `website`).
Have Fun Webbing!

### Websites With Names:
This meantions the certain websites that you can access by name. The Format for this is (Name of Website with clickable URL), (Name input into App). Both WebCMD and WebGUI support this!

1. [Amazon](https://amazon.com), "Amazon"
1. [Microsoft Bing](https://bing.com), "Bing"
1. [ChunkBase](https://chunkbase.com), "ChunkBase"
1. [Facebook](https://facebook.com), "Facebook"
1. [GitHub](https://github.com), "GitHub"
1. [Google Search](https://google.com), "Google"
1. [Microsoft 365](https://microsoft365.com), "Microsoft 365"
1. [Minecraft](https://minecraft.net), "Minecraft"
1. [Python](https://python.org), "Python"
1. [Twitter](https://twitter.com), "Twitter"
1. [Roblox](https://roblox.com), "Roblox"
1. [Steam](https://store.steampowered.com), "Steam"
1. [Walmart](https://walmart.com), "Walmart"
1. [YouTube](https://youtube.com), "YouTube"

## Terminal
"Terminal" is a way to easily access the user's system default terminal. So, if you want to check for an update for your package, you could easily do that! There are also two versions of "Terminal": "Terminal" and "TerminalGUI". Here is how you can tell which each is!

### Both "Terminal" Types
There are two types of "Terminal" Here they are:
"Terminal":
This is the default terminal runner. Everything is done within the Terminal.

"TerminalGUI":
This asks the user for a command within a `tkinter` GUI. The output will be printed in the real Terminal. (Requires `tkinter` module)

### How To Use
To run "Terminal" in your application, here is a way to use it. As per the example above, updating your package would require the `command` string, which holds your command that you are going to run (example: `command = 'pip install tkinter'`), along with `{However "Terminal" is specified}.terminalrun(command)` (For "Terminal), or run `import SoleStormCatPY.TerminalGUI` (For "TerminalGUI", does NOT require `command`).
Have Fun Running commands via Python!

## System Info
This application prints out the user's infomation onto their terminal screen. Here is a basic output of this application:

`The Current User OS is:
Linux

The Current User is:
SoleStormCatPY_user

The Current Version of Python is:
Python 3.10.6`

### How To Use
Here is how you use "System Info":

`import SoleStormCatPY.SystemInfo as SystemInfo
SystemInfo.systemPrint()`

## ClockTimer
This application acts as a timer. The user can set the time (in minutes (Along with seconds and hours in the GUI)), or the developer can set the timer (in seconds). Everything will be printed out into the terminal (or the GUI), and will set the timer.

### How To Use
There is three different ways to use `ClockTimer`. The First being the process where the user sets the timer, the second being where the developer sets the timer, and the third being the GUI mode.
`import SoleStormCatPY.ClockTimer as PyTimer
PyTimer.clockTimer()`

`import SoleStormCatPY.ClockTimer as PyTimer
seconds = 12
PyTimer.clockTimerManual(seconds)`

`import SoleStormCatPY.ClockTimerGUI`

