"""Your document will look something similar to this:
import SoleStormCatPY.MathSolver as pyms

num1 = input("What number do you want first in your math problem?  ")
num2 = input("What number do you want second in your math problem?  ")
ty = input("Which type of equation do you want these numbers to be used with?   ")

pyms.numPrint(num1, num2, ty)
"""



def numPrint(num1, num2, ty):
	"""This prints the numbers from your document. make sure your numbers are assigned to the names 'num1' and 'num2'. You must also have the type of math typed in as 'ty', as 'Divide', 'Multiply', 'Add', or 'Subtract'."""
	
	"""This changes the numbers inputted from strings into intergers, so changing the number strings to integers is not required!"""
	num1N = int(num1)
	num2N = int(num2)
	
	"""This doese the type of math that the user wants"""
	if ty == 'Divide':
		"There are two ways of dividing, so both will be shown"
		print('There are two different ways of dividing, so both will be shown below:  ')
		print('The First way (Number 1 divided by Number 2) being: ', num1N / num2N)
		print('The Second way (Number 2 divides by Number 1) being: ', num2N / num1N)
	elif ty == 'Multiply':
		"There is only one way of multiplying (Both ways give the same number), so only one answer will be shown"
		print('Your answer is: ', num1N * num2N)
	elif ty == 'Add':
		"There is only one way of adding (Both ways give the same number), so only one answer will be shown"
		print('Your answer is: ', num1N + num2N)
	elif ty == 'Subtract':
		"There are two ways of subtracting, so both will be shown"
		print('There are two different ways of subtracting, so both ways will be shown below:  ')
		print('The First way (Number 1 - Number 2) is: ', num1N - num2N)
		print('The Second way (Number 2 - Number 1) is: ', num2N - num1N)
		
		
