#
# starter file for hw1pr2, cs35 spring 2017...
# 
from collections import defaultdict
import csv
import os
import os.path

#
# readcsv is a starting point - it returns the rows from a standard csv file...
#
def readcsv( csv_file_name ):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
    """
    try:
        csvfile = open( csv_file_name, newline='' )  # open for reading
        csvrows = csv.reader( csvfile )              # creates a csvrows object

        all_rows = []                               # we need to read the csv file
        for row in csvrows:                         # into our own Python data structure
            all_rows.append( row )                  # adds only the word to our list

        del csvrows                                  # acknowledge csvrows is gone!
        csvfile.close()                              # and close the file
        return all_rows                              # return the list of lists

    except FileNotFoundError as e:
        print("File not found: ", e)
        return []

#
# write_to_csv shows how to write that format from a list of rows...
#  + try   write_to_csv( [['a', 1 ], ['b', 2]], "smallfile.csv" )
#
def write_to_csv( list_of_rows, filename ):
    """ readcsv takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a list of lists, each inner list is one row of the csv
           all data items are strings; empty cells are empty strings
    """
    try:
        csvfile = open( filename, "w", newline='' )
        filewriter = csv.writer( csvfile, delimiter=",")
        for row in list_of_rows:
            filewriter.writerow( row)
        csvfile.close()

    except:
        print("File", filename, "could not be opened for writing...")


#
# csv_to_html_table_starter
#
#   Shows off how to create an html-formatted string
#   Some newlines are added for human-readability...
#
def csv_to_html_table_starter( csvfilename ):
    """ csv_to_html_table_starter
           + an example of a function that returns an html-formatted string
        Run with 
           + result = csv_to_html_table_starter( "example_chars.csv" )
        Then run 
           + print(result)
        to see the string in a form easy to copy-and-paste...
    """
    LoR = readcsv( csvfilename ) # List of rows
    html_string = '<table>\n'    # start with the table tag
    for row in LoR:
        html_string += '<tr>\n'
        for item in row:
            html_string += '<td>\n' + str(item) + '</td>\n'
        html_string += '</tr>\n'
    html_string += '</table>\n'
    return html_string

#
# Weighted counting of first letters
#
def Wcount():
    """ returns a dictionary of weighted first-letter counts from the file
        wds.csv
    """
    LoR = readcsv('wds.csv') # List of rows
    counts = defaultdict(int)
    for row in LoR:
        firstLetter = str(row[0])[0]
        word = str(row[0])
        num = float(row[1])
        counts[firstLetter.lower()] += num
    return counts

#
# Weighted counting of last letters
#
def WcountLast():
    """ returns a dictionary of weighted last-letter counts from the file
        wds.csv
    """
    LoR = readcsv("wds.csv") # List of rows
    counts = defaultdict(int)
    for row in LoR:
        word = str(row[0])
        num = float(row[1])
        index = len(word) - 1
        lastLetter = str(row[0])[index]
        counts[lastLetter.lower()] += num
    return counts

#
# Weighted counting of the occurence of each letter
#
def ZCount():
    """ returns a dictionary of most-frequently-found position of 'z' 
        from the file wds.csv
    """
    LoR = readcsv('wds.csv') # List of rows
    counts = defaultdict(int)
    for row in LoR:
        word = str(row[0])
        num = float(row[1])
        for index in range(len(word)):
            if  word[index] == 'z' or 'Z':
                counts[index] += num
    return counts

def main():
    firstLetterDict = Wcount()
    lastLetterDict = WcountLast()
    ZCountDict = ZCount()
    
    List = [ x for x in firstLetterDict.items() ]
    List += [ x for x in lastLetterDict.items() ]
    List += [ x for x in ZCountDict.items() ]

    write_to_csv( List, 'frequencies.csv' )
    # Command to print a string of three different tables of dict
    #write_to_csv( firstLetterDict.items(), 'frequencies.csv' )
    #write_to_csv( lastLetterDict.items(), 'frequencies.csv' )
    #write_to_csv( ZCountDict.items(), 'frequencies.csv' )
    #print(csv_to_html_table_starter( 'frequencies.csv' ))
 
    return
main()
