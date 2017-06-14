#
# hw0pr1.py
#

# An example function

def plus1( N ):
    """ returns a number one larger than its input """
    return N+1


# An example loop (just with a printed countdown)

import time

def countdown( N ):
    """ counts downward from N to 0 printing only """
    for i in range(N,-1,-1):
        print("i ==", i)
        time.sleep(0.01)

    return    # no return value here!


# ++ Challenges:  create and test as many of these five functions as you can.
#
# The final three will be especially helpful!
def time42( s ):
	""" prints the string s 42 times(on separate lines)"""
	for i in range(42):
		print(s)
	return 

def aline(N):
	""" returns the string "aliii...iiien" with exactly N "i"s"""
	print 'al' + N *'i' + 'en'

def count_digits( s ):
	""" returns the number of digits in the input string s """
	count = 0
	for i in s:
		if i.isdigit():
			count += 1
	return count 
	
def clean_digits( s ):    
	""" returns only the digits in the input string s """
	digit = ''
	for i in s:
		if i.isalpha():
			digit = digit 
		else:
			digit = digit + i
	return digit

def clean_word( s ):
	""" returns an all-lowercase, all-letter version of the input string s"""
	words = ''
	for i in s:
		if i.isalpha():
			words += i
		else:
			words = words
	words = words.lower()
	return words



