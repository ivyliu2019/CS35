#
# hw0pr3.py
#
""" simply run in terminal: python3 hw0pr5.py
"""
import os
import os.path
import csv

def clean_digits( s ):    
	""" returns only the digits in the input string s """
	digit = ""
	for i in s:
		if i.isdigit():
			digit += i
	return digit

def getContactList(digitLine, nameLine):
	""" returns lists of First names and Last names"""
	contactInfo = []
	if ',' in nameLine:
		lastName = nameLine.split(',')[0]
		firstName = nameLine.split(',')[1]
	else:
		firstName = nameLine.split(' ')[0]
		lastName = nameLine.split(' ')[1]
	contactInfo = [lastName, firstName, clean_digits(digitLine)]
	return contactInfo

def main():
	os.chdir( "phone_files" )
	L = os.listdir() 
	data = []
	for subdirectory in L:
		os.chdir(subdirectory)
		L1 = os.listdir() 
		for file in L1:
			lines = tuple(open(file, 'r'))
			digitLine = lines[0]
			nameLine = lines[1]
			data += [getContactList(digitLine, nameLine)]
		os.chdir( ".." )
	with open('number.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		for line in data:
			writer.writerow(line)
main()
