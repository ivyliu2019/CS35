#
# hw3pr3.py
#
# Visualizing your own data with matplotlib...
#
# Here, you should include functions that produce two visualizations of data
#   of your own choice. Also, include a short description of the data and
#   the visualizations you created. Save them as screenshots or as saved-images,
#   named datavis1.png and datavis2.png in your hw3.zip folder.
#
# Gallery of matplotlib examples:   http://matplotlib.org/gallery.html
#
# List of many large-data sources:    https://docs.google.com/document/d/1dr2_Byi4I6KI7CQUTiMjX0FXRo-M9k6kB2OESd7a2ck/edit
#     and, the birthday data in birth.csv is a reasonable fall-back option, if you'd like to use that...
#          you could create a heatmap or traditional graph of birthday frequency variations over the year...
#


"""
Short description of the two data visualizations...
    datavs1() creates a stacked bar plot of the features of rps strings from rps.csv
    datavs2() creates a heatmap of birthday frequencies from births.csv

"""

import matplotlib.pyplot as plt
import numpy as np
import hw3pr2
import csv
from pylab import figure, show
import matplotlib.lines as lines
#
# datavis1()
#
def datavis1():
    """ datavis1 presents data visualization for the features of rps strings"""
    allString = hw3pr2.read_data( filename="rps.csv" )
    N = len(allString)
    numS = []
    numR = []
    numP = []
    index = 0
    for string in allString:
        index += 1
        d = hw3pr2.extract_features(string)
        numS.append( d['s'] )
        numP.append( d['p'] )
        numR.append( d['r'] )

    # plot the bar plot now
    fig = plt.figure()
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35
    p1 = plt.bar(ind, numS, width, color='#d62728')
    p2 = plt.bar(ind, numP, width, color='b', bottom=numS)
    p3 = plt.bar(ind, numR, width, color='y',
                    bottom=[numP[i]+numS[i] for i in range(N)])

    plt.ylabel('number of characters')
    plt.title('FEATURES OF RPS STRINGS')
    xticks = [str(i) for i in range(N)]
    plt.yticks(np.arange(0,250,10))
    plt.legend( (p1[0], p2[0], p3[0]), ('S', 'R', 'P') )
    # save to file
    fig.savefig('datavis1.png', bbox_inches='tight')
    # and show it on the screen
    plt.show()

# run it!
# datavis1()

#
# datavis2()
#
def read_data( filename="births.csv" ):
    """ read_data extracts all of its data in the file and returns a
        list of all of the rps strings in that csv file
    """
    try:
        csvfile = open( filename, newline='' )  # open for reading
        csvrows = csv.reader( csvfile )              # creates a csvrows object

        all_rows = []                               # we need to read the csv file
        for row in csvrows:                         # into our own Python data structure
            all_rows.append( row )                  # adds only the word to our list

        del csvrows                                  # acknowledge csvrows is gone!
        csvfile.close()                              # and close the file
        all_rows = all_rows[1:]
        return all_rows                              # return the list of lists

    except FileNotFoundError as e:
        print("File not found: ", e)
        return []

def datavis2():
    """ datavis2 presents a heatmap of birthda frequencies from the csv file
    """
    # generate data from csv file
    list_of_rows = read_data( filename="births.csv" )
    month = [int(x[0]) for x in list_of_rows]
    day = [int(x[1]) for x in list_of_rows]
    intensity = [int(x[2]) for x in list_of_rows]

    M = np.zeros((max(month) + 1, max(day) + 1))
    M[month, day] = intensity

    fig, ax = plt.subplots()
    plt.title('BIRTHDAY FREQUENCIES')
    plt.ylabel('MONTH')
    plt.xlabel('DAY')
    ax.imshow(M)
    show()

    # save to file
    fig.savefig('datavis2.png', bbox_inches='tight')
    # and show it on the screen
    show()

# run it!
datavis2()
