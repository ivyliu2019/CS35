#
# hw0pr3.py
#
#
"""
Run in terminal: python3 hw0pr3.py
Questions to answer:
1. Comparing 2009's and 2013's addresses, which used the word "country" more often? 2013.txt
2. Comparing all of the addresses, which used the word "war" most often? 1821.txt
3. Which of the addresses contains the largest number of four-letter words?
   (Here, we imagine removing all of the punctuation from each word, so that
	"don't" and "wars?" are both four-letter words.) 1841.txt
My questions:
1. Comparing all of the addresses, which used the word "citizen" most often? 1841.txt
2. What's the total number of punctuations in all files? 151491
3. What's the total number of digits in all files? 370
"""

import os
import os.path

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

def countWords(filename, checkWord):
	""" return the number of checkword in the file filename"""
	f = open(filename, 'r').read()
	content = f.split()
	wordList = []
	for word in content:
		cleanWord = clean_word(word)
		wordList += [cleanWord]
	count = 0
	for word in wordList:
		if word == checkWord:
			count += 1
	return count

def compareWords(filename1, filename2, checkWord):
	""" return the file that has more checkWord """
	num1 = countWords(filename1, checkWord)
	num2 = countWords(filename2, checkWord)
	if num1 == num2:
		return 'same'
	if num1 > num2:
		return filename1
	else:
		return filename2

def countFourLetterWords(filename):
	""" return the number of four-letter words in a file"""
	f = open(filename, 'r').read()
	content = f.split()
	wordList = []
	for word in content:
		cleanWord = clean_word(word)
		wordList += [cleanWord]
	count = 0
	for word in wordList:
		if len(word) == 4:
			count += 1
	return count

def count_digits(s):
	""" returns the number of digits in the input string s """
	count = 0
	for i in s:
		if i.isdigit():
			count += 1
	return count 

def count_punctuations( s ):
	""" returns the number of punctuations of the input string s"""
	count = 0
	for i in s:
		if (i.isalpha() or i.isdigit()) == False:
			count += 1
	return count

def main():
	os.chdir( "addresses" )
	country = compareWords("2009.txt", "2013.txt", "country")
	print ("The address that uses the word 'country' most often", country)
	L = os.listdir()
	dict1 = {}
	dict2 = {}
	dict3 = {}
	numDigit = 0
	numPunctuations = 0
	for file in L:
		numWar = countWords(file, "war")
		numCitizen = countWords(file, "citizen")
		numFourLetter = countFourLetterWords(file)
		dict1[file] = numWar
		dict2[file] = numFourLetter
		dict3[file] = numCitizen
		lines = tuple(open(file, 'r'))
		for line in lines:
			digits = count_digits(line)
			punctuations = count_punctuations(line)
			numDigit += digits
			numPunctuations += punctuations
	maxKey1 = max(dict1, key=dict1.get)
	maxKey2 = max(dict2, key=dict2.get)
	maxKey3 = max(dict3, key=dict3.get)
	print ("The address that uses the word 'war' most often", maxKey1)
	print ("The address that uses the four-letter words most often", maxKey2)
	print ("The address that uses the word ‘citizen’ most often", maxKey3)
	print ("The total number of digits for all files is", numDigit )
	print ("The total number of punctuations for all files is", numPunctuations)

main()
