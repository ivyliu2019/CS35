#
# hw0pr2.py
#
#
# Questions to answer:
# 1. How many .txt files are in the whole set? 9896
# 2. Across all of the files, how many of the phone numbers contain exactly 10 digits? 3988
# 3. Of these exactly-ten-digit phone numbers, how many are in the area code 909 (the 
#	area code will be the first three digits of a ten-digit number). 9
# 4. How many people have the name "GARCIA" in the whole set? 237

import os
import os.path

def count_digits( s ):
	""" returns the number of digits in the input string s """
	count = 0
	for i in s:
		if i.isdigit():
			count += 1
	return count 

def clean_digits( s ):    
	""" returns only the digits in the input string s """
	digit = ""
	for i in s:
		if i.isdigit():
			digit += i
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

# presuming we're in the 00 directory, let's count all the txt files
def count_txtfile():
	""" examples of file reading and exceptions """
	count = 0
	L = os.listdir() 
	for file in L:	
		if file.endswith(".txt"):
				count += 1
	return count

def count_phoneNumbers():
	""" returns the number of the phone numbers contain exactly 10 digits and with area code 909"""
	count = 0
	L = os.listdir() 
	for file in L:
		lines = tuple(open(file, 'r'))
		digits = count_digits(lines[0])
		if digits == 10:
			count += 1
	return count

def count_909():
	"""  returns the number of phone numbers with area code 909"""
	count909 = 0
	L = os.listdir() 
	for file in L:
		lines = tuple(open(file, 'r'))
		digits = count_digits(lines[0])
		if digits == 10:
			cleanNumbers = clean_digits(lines[0])
			if cleanNumbers[:3] == "909":
				count909 += 1
	return count909

def count_GARCIA():
	""" returns the number of GARCIA"""
	count_GARCIA = 0
	L = os.listdir() 
	names = []
	for file in L:
		lines = tuple(open(file, 'r'))
		nameLine = lines[1]
		newLine = clean_word(nameLine)
		if 'garcia' in newLine:
			count_GARCIA += 1
	return count_GARCIA

def main():
	os.chdir( "phone_files" )
	L = os.listdir() 
	numberFiles = 0
	numberTenDigits = 0
	number909 = 0
	numberGarcia = 0
	for subdirectory in L:
		os.chdir(subdirectory)
		count = count_txtfile()
		numberFiles += count
		numberTenDigits += count_phoneNumbers()
		number909 += count_909()
		numberGarcia += count_GARCIA()
		os.chdir( ".." )
	print("Number of txt files:", numberFiles)
	print("Number of 10 digits phone number", numberTenDigits)
	print("Number of the phone numbers with area code 909", number909)
	print("Number of GARCIA", numberGarcia)
main()
