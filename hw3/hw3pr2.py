#
# hw3pr2.py
#
# Person or machine?  The rps-string challenge...
#
# This file should include your code for
#   + extract_features( rps ),               returning a dictionary of features from an input rps string
#   + score_features( dict_of_features ),    returning a score (or scores) based on that dictionary
#   + read_data( filename="rps.csv" ),       returning the list of datarows in rps.csv
#
# Be sure to include a short description of your algorithm in the triple-quoted string below.
# Also, be sure to include your final scores for each string in the rps.csv file you include,
#   either by writing a new file out or by pasting your results into the existing file
#   And, include your assessment as to whether each string was human-created or machine-created
#
#

"""
Short description of
      (1) The features I compute for each rps-string are the number of each character.
      (2) To generate a score relate to "humanness" or "machineness," score_features
          computes the percentage of number of each character in each string: percentS,
          percentP and percentR. Then compute how much is each percentage away from
          the probability 1/3, which is when three character has equal weight in the
          string and the furthest percentage away from 1/3 is the actual score. The
          function rescales it by multilying 10. The lower the score is, the more evenly
          distributed of each character in the string and more likely to be machine-generated.
          Likewise, the higher the scores are, the more likely the string will be
          produced by human.
"""


# Here's how to machine-generate an rps string.
# You can create your own human-generated ones!

import random
import csv

def gen_rps_string( num_characters ):
    """ return a uniformly random rps string with num_characters characters """
    result = ''
    for i in range( num_characters ):
        result += random.choice( 'rps' )
    return result

# Here are two example machine-generated strings:
rps_machine1 = gen_rps_string(200)
rps_machine2 = gen_rps_string(200)
# print those, if you like, to see what they are...


from collections import defaultdict

#
# extract_features( rps ):   extracts features from rps into a defaultdict
#
def extract_features( rps ):
    """ extract_features takes in a string rps and creates a default dictionary
        that counts the number of each character in the string.
    """
    d = defaultdict( float )  # other features are reasonable
    number_of_s_es = rps.count('s')  # counts all of the 's's in rps
    number_of_r_es = rps.count('r')  # counts all of the 'r's in rps
    number_of_p_es = rps.count('p')  # counts all of the 'p's in rps
    d['s'] = number_of_s_es
    d['r'] = number_of_r_es
    d['p'] = number_of_p_es
    return d

#
# score_features( dict_of_features ): returns a score based on those features
#
def score_features( dict_of_features ):
    """ score_feature takes in a dictionary of features, and returns a single
        floating-point number that scores how human-made or how machine-made
        those features are.
    """
    d = dict_of_features
    length = d['s']+ d['r']+d['p']
    prob = float(1/3)    # The probability of choosing each character is 1/3
    percentS = float(d['s'])/length
    percentR = float(d['r'])/length
    percentP = float(d['p'])/length

    scoreS = abs(percentS - prob) * 10
    scoreR = abs(percentR - prob) * 10
    scoreP = abs(percentP - prob) * 10
    score = max(scoreS, scoreR, scoreP)
    return score   # return a humanness or machineness score

#
# read_data( filename="rps.csv" ):   gets all of the data from "rps.csv"
#
def read_data( filename="rps.csv" ):
    """ read_data extracts all of its data in the file and returns a list of
        all of the rps strings in that csv file
    """
    try:
        csvfile = open( filename, newline='' )  # open for reading
        csvrows = csv.reader( csvfile )              # creates a csvrows object

        all_rows = []                               # we need to read the csv file
        for row in csvrows:                         # into our own Python data structure
            all_rows.append( row )                  # adds only the word to our list

        del csvrows                                  # acknowledge csvrows is gone!
        csvfile.close()                              # and close the file
        all_rows = [x[3] for x in all_rows]
        return all_rows                              # return the list of lists

    except FileNotFoundError as e:
        print("File not found: ", e)
        return []


#
# you'll use these three functions to score each rps string and then
#    determine if it was human-generated or machine-generated
#    (they're half and half with one mystery string)
#
# Be sure to include your scores and your human/machine decision in the rps.csv file!
#    And include the file in your hw3.zip archive (with the other rows that are already there)
#
def main():
    """ compute the score of each rps string and write the scores and
        human/machine decision to the rps.csv file
    """
    allString = read_data( filename="rps.csv" )
    list_of_rows = []
    index = 0
    for string in allString:
        index += 1
        dict_of_features = extract_features(string)
        score = score_features( dict_of_features )

        if score > 0.5:
            decision = 'human'
        else:
            decision = 'machine'
        list_of_rows += [[index, score, decision, string]]
    # print (list_of_rows)
    try:
        csvfile = open( "rps.csv", "w", newline='' )
        filewriter = csv.writer( csvfile, delimiter=",")
        for row in list_of_rows:
            filewriter.writerow( row )
        csvfile.close()

    except:
        print("File", "rps.csv", "could not be opened for writing...")
main()
