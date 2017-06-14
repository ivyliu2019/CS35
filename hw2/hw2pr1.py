#
# starting examples for cs35, week2 "Web as Input"
#

import requests
import string
import json

"""
Examples you might want to run during class:

Web scraping, the basic command (Thanks, Prof. Medero!)

#
# basic use of requests:
#
url = "https://www.cs.hmc.edu/~dodds/demo.html"  # try it + source
result = requests.get(url)
text = result.text   # provides the source as a large string...

#
# try it for another site...
#

#
# let's demo the weather example...
#
url = 'http://api.wunderground.com/api/49e4f67f30adb299/geoloookup/conditions/q/Us/Ca/Claremont.json' # JSON!
       # try it + source
result = requests.get(url)
data = result.json()      # this creates a data structure from the json file!
# What type will it be?
# familiarity with dir and .keys() to access json data...

#
# let's try the Open Google Maps API -- also provides JSON-formatted data
#   See the webpage for the details and allowable use
#
# Try this one by hand - what are its parts?
# http://maps.googleapis.com/maps/api/distancematrix/json?origins=%22Claremont,%20CA%22&destinations=%22Seattle,%20WA%22&mode=%22walking%22
#
# Take a look at the result -- imagine the structure of that data... That's JSON! (Sketch?)
#
"""

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Problem 1 starter code
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#
#
#
def google_distances_api_scrape(filename_to_save="distances.json"):
    """ a short function that shows how
        part of Google Maps' API can be used to
        obtain and save a json file of distances data...
    """
    url="http://maps.googleapis.com/maps/api/distancematrix/json"

    city1="Claremont,CA"
    city2="Seattle,WA"
    my_mode="walking"

    inputs={"origins":city1,"destinations":city2,"mode":my_mode}

    result = requests.get(url,params=inputs)
    data = result.json()
    print("data is", data)

    # save this json data to file
    f = open( filename_to_save, "w" )     # opens the file for writing
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    f.write(string_data)                        # then, writes that string to a file...
    f.close()                                   # and closes the file
    print("\nfile", filename_to_save, "written.")
    # no need to return anything, since we're better off reading it from file!
    return


def google_distances_api_process(filename_to_read = "distances.json"):
    """ a function with examples of how to manipulate json data --
        here the data is from the file scraped and saved by
        google_distances_api_starter()
    """
    f = open( filename_to_read, "r" )
    string_data = f.read()
    data = json.loads( string_data )
    print("data (not spiffified!) is\n\n", data, "\n")

    print("Accessing its components:\n")

    row0 = data['rows'][0]
    print("row0 is", row0, "\n")

    cell0 = row0['elements'][0]
    print("cell0 is", cell0, "\n")

    distance_as_string = cell0['distance']['text']
    print("distance_as_string is", distance_as_string, "\n")

    # here, we may want to continue operating on the whole json dictionary
    # so, we return it:
    return data


#
# multicity_distance_scrape
#
def multicity_distance_scrape( Origins, Dests, filename_to_save="multicity.json" ):
    """ Inputs: Origins is a list of “origin” locations,
                Dests is a list of “destination” locations.
        It uses the Google Maps API to get the distance from each of the “origin”
        locations to each of the “destination” locations and save a json file of
        distances data
    """
    originInput = ''
    destinationInput = ''
    for origin in Origins:
        originInput += origin + '|'
    for destination in Dests:
        destinationInput += destination + '|'
    url="http://maps.googleapis.com/maps/api/distancematrix/json"

    my_mode="walking"

    inputs={"origins":originInput,"destinations":destinationInput,"mode":my_mode}

    result = requests.get(url,params=inputs)
    data = result.json()
    print("data is", data)

    # save this json data to file
    f = open( filename_to_save, "w" )     # opens the file for writing
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    f.write(string_data)                        # then, writes that string to a file...
    f.close()                                   # and closes the file
    print("\nfile", filename_to_save, "written.")
    # no need to return anything, since we're better off reading it from file!
    return

#
# multicity_distance_process
#
def multicity_distance_process(filename_to_read = "multicity.json"):
    """ This function reads in the json data from the file, creates and returns an
        HTML table with the distances between each of the locations.
    """
    f = open( filename_to_read, "r" )
    string_data = f.read()
    data = json.loads( string_data )
    print("data (not spiffified!) is\n\n", data, "\n")

    htmlString = '<table>\n'

    rows = data['rows']
    for row in rows:
        htmlString += '<tr>\n'
        listOfElements = row['elements']
        for element in listOfElements:
            distance = element['distance']
            htmlString += "<td>" + distance + "</td>\n"
        htmlString += "</tr>\n"
    html_string += "</table>\n"

    return html_string
#
# a main function for problem 1 (the multicity distance problem)
#
def main_pr1():
    """ a top-level function for testing things! """
    # these were the cities from class:
    # Origins = ['Pittsburgh,PA','Boston,MA','Seattle,WA']  # starts
    # Dests = ['Claremont,CA','Atlanta,GA']         # goals
    #
    # Origins are rows...
    # Dests are columns...
    pass







# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Problem 2a starter code
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#
#
#

def apple_api_id_scraper(artist_name, filename_to_save="appledata_id.json"):
    """
    """
    ### Use the search url to get an artist's itunes ID
    search_url = "https://itunes.apple.com/search"
    parameters = {"term":artist_name, "entity":"musicArtist","media":"music","limit":200}
    result = requests.get(search_url, params=parameters)
    data = result.json()

    # save to a file to examine it...
    f = open( filename_to_save, "w" )     # opens the file for writing
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    f.write(string_data)                        # then, writes that string to a file...
    f.close()                                   # and closes the file
    print("\nfile", filename_to_save, "written.")

    # we'll return a useful value: the artist id...
    #
    # Note: it's helpful to find the iTunes artistid and return it here
    # (this hasn't been done yet... try it!)

    return 136975   # This is the Beatles...


#
#
#
def apple_api_full_scraper(artistid=136975, filename_to_save="appledata_full.json"):
    """
    Takes an artistid and grabs a full set of that artist's albums.
    "The Beatles"  has an id of 136975
    """
    lookup_url = "https://itunes.apple.com/lookup"
    parameters = {"entity":"album","id":artistid}
    result = requests.get(lookup_url, params=parameters)
    data = result.json()

    # save to a file to examine it...
    f = open( filename_to_save, "w" )     # opens the file for writing
    string_data = json.dumps( data, indent=2 )  # this writes it to a string
    f.write(string_data)                        # then, writes that string to a file...
    f.close()                                   # and closes the file
    print("\nfile", filename_to_save, "written.")

    # we'll leave the processing to another function...
    return



#
#
#
def apple_api_full_process(filename_to_read="appledata_full.json"):
    """ example of extracting one (small) piece of information from
        the appledata json file...
    """
    f = open( filename_to_read, "r" )
    string_data = f.read()
    data = json.loads( string_data )
    #print("data (not spiffified!) is\n\n", data, "\n")

    # for live investigation, here's the full data structure
    return data



#
#
#
#def most_productive_scrape(artist1, artist2, fname1="artist1.json", fname2="artist2.json"):



#
#
#
#def most_productive_process(fname1="artist1.json", fname2="artist2.json"):



#
# main_pr2()  for testing problem 2's functions...
#
def main_pr2():
    """ a top-level function for testing things... """
    most_productive_scrape( "Katy Perry", "Steve Perry" )
    most_productive_process()  # uses default filenames!
    return

"""
Overview of progress on this problem - test cases you ran

For example: most_productive_scrape( "Taylor Swift", "Kanye West" ); most_productive_process()
"""



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Problem 2b starter code
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import datetime

#
# earthquake examples...
#
""" unlike the previous problems, this starter code really
    just shows snippets -- you might try at the command-prompt
    or by editing commenting in/out the lines of this function...
"""
## Playground! Use this space to explore and play around with the USGS API
#

print("\nProblem 2b's starter-code results:\n")
now = datetime.date.today()
print("Now, the date is", now)   # counts from 0001-01-01
print("Now, the ordinal value of the date is", now.toordinal())
print("now.fromordinal(42) is", now.fromordinal(42))



#
# Or, you might copy individual lines to the Python command prompt...
#
"""
# reference:
url = "http://earthquake.usgs.gov/fdsnws/event/1/query"
parameters={"format":"geojson","limit":"20000","starttime":"2017-02-05","endtime":"2017-02-06"}
result = requests.get(url,params=parameters)
data = result.json()
print("data")

# save to a file to examine it...
filename_to_save = "quake.json"
f = open( filename_to_save, "w" )     # opens the file for writing
string_data = json.dumps( data, indent=2 )  # this writes it to a string
f.write(string_data)                        # then, writes that string to a file...
f.close()                                   # and closes the file
print("\nfile", filename_to_save, "written.")

#timestamp = ... from the quake data
#print(dir(datetime))
#  The timestamps in the quake data are in one-thousandths of a day!
#dt = datetime.datetime.utcfromtimestamp(timestamp/1000) #, datetime.timezone.utc)
#print(dt)

# dates!
now = datetime.date.today()
print("Now, the date is", now)   # counts from 0001-01-01
print("Now, the ordinal value of the date is", now.toordinal())
print("now.fromordinal(42) is", now.fromordinal(42))
"""




# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Problem 3 -- please take a look at problem3_example.py for an example!
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#
# This problem is very scalable -- start with a small prediction task
#   (serious or not...) that involves analyzing at least two sites...
#
# Feel free to find your own json-based APIs -- or use raw webpages
#   and BeautifulSoup! (This is what the example does...)
#
