#
# hw1pr3.py
# simply run on the terminal with "python3 hw1pr3.py"
# 

import csv

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
            filewriter.writerow( row )
        csvfile.close()

    except:
        print("File", filename, "could not be opened for writing...")

def generateSubDict( filename ):
    """ generateSubDict takes as
         + input:  csv_file_name, the name of a csv file
        and returns
         + output: a dictionary (or defaultdict){string key : string value} 
         pairs that are the annotations or substitutions 
    """
    loR = readcsv(filename)
    dict = {}
    for row in loR:
        dict[row[0]] = row[1]
    return dict

def clean_word( s ):
    """ returns an all-letter version of the input string s"""
    words = ''
    for i in s:
        if i.isalpha():
            words += i
        else:
            words = words
    return words
#
# annotate_text
#
#   Shows off how to style portions of an input text
#
#
def annotate_text( text, subs ):
    """ input text: any (possible large) string of text;
        input subs, a dictionary or defaultdict of {string key : string value} 
        pairs that are the annotations or substitutions;
        annotate_text should output a string of styled HTML that can be 
        displayed in a webpage.
    """
    new_html_string = ''
    for word in text.split(): #word by word#
        cleanedWd = clean_word(word)
        if cleanedWd in subs:
            # we use Python's cool "text-formatting" ability...
            new_word = '<span style="color:rgb{0};" title="{1}">{2}</span> '.format("(0,0,150)",subs[cleanedWd],word)
        elif word == '\n':  # handle new lines...
            new_word = "<br>"
        else:
            new_word = word + ' '

        # add the new character, new_c
        new_html_string += new_word 

    # finished!
    return new_html_string


# Larger example for testing...


#
# Here are the text and dictionary of substitutions used in hamlet_substitution.html
#
# Note that we don't give away the template engine here (there'd be nothing left!) 
#
# Inspired by
# http://nfs.sparknotes.com/hamlet/page_50.html
#

HAMLET_A1S4 = """
The king doth wake tonight and takes his rouse, 
Keeps wassail and the swaggering upspring reels, 
And, as he drains his draughts of Rhenish down, 
The kettle-drum and trumpet thus bray out 
The triumph of his pledge. 
"""

#
# this would be read in from a csv file and constructed
#
# Again, we don't give that function (it's the hw!)
HAMLET_SUBS = { "doth":"does", "rouse":"partying", 
                "wassail":"drinks",
                "reels":"dances", "rhenish":"wine", 
                "bray":"blare", "pledge":"participation"}

text = """
Senator johnson was caught stealing a smartphone on election 
night. witnesses say that he allegedly took the smartphone 
from a kindly old lady while she was washing her electric car. 
republican and democrat congressional leaders have vowed to 
hold hearings. Senator johnson could not be reached for comment.
"""

SUB = [['witnesses', 'these dudes I know'], ['rebuild', 'avenge'], 
        ['space', 'spaaace'], ['electric','atomic'], ['car','cat'],
        ['election','eating contest'], ['smartphone', 'pokedex'] ]

def main():
    write_to_csv( SUB, 'substitution.csv' )
    subs = generateSubDict( 'substitution.csv' )
    print(annotate_text(text,subs))

main()
