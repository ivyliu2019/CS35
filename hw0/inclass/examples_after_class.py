#
# cs35 examples in-class  1/23/17
#

"""
DEMO 1:

moving around directories and accessing their contents

the os and os.path libraries are documented here:
  https://docs.python.org/3/library/os.html
  https://docs.python.org/3/library/os.path.html
"""

import os
import os.path

def directory_examples():
    """ examples for directory navigation and contents... """
    # get current working directory
    original_dir = os.getcwd()
    print("original_dir is", original_dir)

    # change the current working directory
    os.chdir("..")  # up one directory
    print("now, I'm in", os.getcwd())

    # change back!
    os.chdir( original_dir )  # back to original
    print("and now, I'm in", os.getcwd())

    # get a listing of all of the contents of the directory
    DirContents = os.listdir( )
    print("DirContents:", DirContents)

    # +++ Challenge: go into the hp directory and list its contents:

    # SOLUTION TO CHALLENGE
    os.chdir( "hp" )
    DirContents = os.listdir( )
    print("DirContents:", DirContents)




"""
DEMO 2:

Opening files and reading their contents

Documentation:
  https://docs.python.org/3.3/tutorial/inputoutput.html#reading-and-writing-files
  [Extra] file encodings:  https://docs.python.org/3/library/codecs.html
"""

# here's the first file challenge:
def file_examples_CONCATENATE_SOLUTION():
    """ examples of file reading and exceptions """

    L = os.listdir()  # LIST of FILES!!!!
    print("Current list of files is", L)

    # here is our final string...
    final_result = ""

    for filename in L:
        try:
            f = f(filename,"r", encoding="latin1") # latin1 is a very safe encoding
            data = f.read()   # read all of the file's data
            f.close()         # close the file
        except PermissionError:  # example of "exceptions": atypical errors
            print("file", filename, "couldn't be opened: permission error")
            data = ""
        except UnicodeDecodeError:
            print("file", filename, "couldn't be opened: encoding error")
            data = "" # no data
        except FileNotFoundError:  # try it with and without this block...
            print("file", filename, "couldn't be opened: not found!")
            print("Check if you're running this in the correct directory... .")
            data = ""

        final_result += data

    # We return the data we obtained in trying to open the file
    #print("File data:", data)
    return final_result    # remember print and return are different!



# here's the second file challenge (a variant, at least)
def file_examples_INDIVIDUAL_FILES_SOLUTION():
    """ examples of file reading and exceptions """

    L = os.listdir()  # LIST of FILES!!!!
    print("Current list of files is", L)

    # here is a LIST of final strings
    List_of_datas = []  # always trying to use the word datas!

    for filename in L:
        try:
            f = open(filename,"r", encoding="latin1") # latin1 is a very safe encoding
            data = f.read()   # read all of the file's data
            f.close()         # close the file
        except PermissionError:  # example of "exceptions": atypical errors
            print("file", filename, "couldn't be opened: permission error")
            data = ""
        except UnicodeDecodeError:
            print("file", filename, "couldn't be opened: encoding error")
            data = "" # no data
        except FileNotFoundError:  # try it with and without this block...
            print("file", filename, "couldn't be opened: not found!")
            print("Check if you're running this in the correct directory... .")
            data = ""

        List_of_datas.append(  data   )  # add each one to the list


    return List_of_datas    # don't print this - it's huge!



""" 
DEMO 3:

Text analysis of data obtained from a file...

Here we introduce the _much_ nicer alternative to dictionaries, called
    default dictionaries, or defaultdict, with documentation here:
    https://docs.python.org/3/library/collections.html#collections.defaultdict 

In addition, we introduce some useful parts of the string library:
    https://docs.python.org/3.1/library/string.html
    Methods such as s.lower(), s.upper(), s.split(), ... are wonderful!
"""

from collections import defaultdict      # be sure to import it!


# We will write a function that counts all of the 'A's and 'a's in the input 
def count_a( data ):
    """ this function returns a default dictionary that contains
        the key 'a': its value is equal to the number of 'a's in the input, data
        NOTE: everything is lower-cased, so this really counts 'A's and 'a's
    """
    counts = defaultdict(int)
    data = data.lower()       # lower case all of the data
    for c in data:            # loop over each character in the data
        if c == 'a':
            counts['a'] += 1

    return counts


# SOLUTION TO THE COUNT-ALL-CHARS challenge
# We will write a function that counts all of the chars in the input 
def count_all_chars( data ):
    """ 
    count all characters! Less, not more!!
    """
    counts = defaultdict(int) # our friend
    data = data.lower()       # lower case all of the data
    for c in data:            # loop over each character in the data
        counts[c] += 1

    return counts




# IN-CLASS FUNCTION...
def clean( wd ):
    """  should return the string wd with no non-letter characters... 
    """
    # NOT IMPLEMENTED HERE - UP TO YOU!
    return wd



# SOLUTION TO THE COUNT-ALL-WORDS challenge
# We will write a function that counts all of the words in the input 
def count_all_words( data ):
    """ 
    count all characters! Less, not more!!
    """
    counts = defaultdict(int) # our friend
    data = data.lower()       # lower case all of the data
    List_of_words = data.split()
    for wd in List_of_words:            # loop over each character in the data
        wd = clean(wd)         # do this! (our function is empty...)
        counts[wd] += 1

    return counts





# Here is a function to read the file and call things
# 
def main():
    """ This "main" function will show off the prior ones...
    """
    # This is an example of a function that you should create so that 
    # the graders can test your solutions...
    # Note that it uses other function calls that return values - this one
    # simply prints the results:

    # first, we change into the hp directory
    os.chdir( "hp" )
    List_of_datas = file_examples_INDIVIDUAL_FILES_SOLUTION()
    all_text_in_all_files = file_examples_CONCATENATE_SOLUTION()
    # we could run loops of counting over List_of_datas,
    # but we leave that to you...!

    # Instead we run over all_text_in_all_files
    all_chars = count_all_chars( all_text_in_all_files )
    all_words = count_all_words( all_text_in_all_files )
    print("The number of a's in all the text:", all_chars['a'])
    print("The number of z's in all the text:", all_chars['z'])
    print("The number of words a/A in all the text:", all_words['a'])
    print("The number of words z/Z in all the text:", all_words['Z'])

    # for consistency, we return to the top-level directory
    os.chdir( ".." )

    # and return for fun 
    return 42


"""
Example triple-quoted string with solutions

Note: these are not the desired solutions, but they're a reasonable 
example!

We counted the number of letters 'a' and 'z' and the
  number of words 'a' and 'z' across our corpus of three foundational
  English-language works. Here were the results:

Current list of files is ['hp1.txt', 'hp4.txt', 'samiam.txt']
The number of a's in all the text: 95043
The number of z's in all the text: 1165
The number of words a/A in all the text: 5304
The number of words z/Z in all the text: 0
"""




