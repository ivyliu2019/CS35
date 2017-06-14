# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# Problem 2a starter code
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import requests
import string
import json


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

    artistid=data['results'][0]['artistId']
    return artistid
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
def most_productive_scrape(artist1, artist2, fname1="artist1.json", fname2="artist2.json"):
    """ most_productive_process takes the names of two artists as input,
        gathers all of the album/work information from iTunes and save the
        results into the filenames fname1 and fname2
    """
    artistid1 = apple_api_id_scraper(artist1)
    artistid2 = apple_api_id_scraper(artist2)
    print (artistid1)
    print (artistid2)

    apple_api_full_scraper(artistid1,fname1)
    apple_api_full_scraper(artistid2,fname2)

    # we'll leave the processing to another function...
    return
#
#
#
def most_productive_process(fname1="artist1.json", fname2="artist2.json"):
    """ most_productive_process reads in those two files and then prints out
        the artists and the number of works they have int he iTunes store.
    """
    data1 = apple_api_full_process(fname1)
    artist1 = data1['results'][0]['artistName']
    num1 = data1['resultCount']
    print("# of results for", artist1, "==", num1)

    data2 = apple_api_full_process(fname2)
    artist2 = data2['results'][0]['artistName']
    num2 = data2['resultCount']
    print("# of results for", artist2, "==", num2)
    # for live investigation, here's the full data structure
    return

#
# main_pr2()  for testing problem 2's functions...
#
def main_pr2():
    """ a top-level function for testing things... """
    most_productive_scrape( "Katy Perry", "Steve Perry" )
    most_productive_scrape( "Taylor Swift", "Kanye West" )
    most_productive_scrape( "Drake", "Ed Sheeran" )
    most_productive_process()  # uses default filenames!
    return

"""
Overview of progress on this problem - test cases you ran

For example: most_productive_scrape( "Taylor Swift", "Kanye West" ); most_productive_process()
"""
main_pr2()


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

# print("\nProblem 2b's starter-code results:\n")
# now = datetime.date.today()
# print("Now, the date is", now)   # counts from 0001-01-01
# print("Now, the ordinal value of the date is", now.toordinal())
# print("now.fromordinal(42) is", now.fromordinal(42))



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
def quakiestDay(threshold):
    """ quakiestDay takes in threshold, prints out the number of
        earthquakes for each of the previous 7 days and returns
        the quakiest day.
    """
    url = "http://earthquake.usgs.gov/fdsnws/event/1/query"
    today = datetime.date.today()
    todays_ordinal = today.toordinal()
    dataLists = []
    for ordinal in range(todays_ordinal,todays_ordinal-7,-1):
        day = datetime.date.fromordinal(ordinal)
        nextDay = datetime.date.fromordinal(ordinal+1)
        print("Currently looking at", str(day))
        parameters={"format":"geojson","limit":"20000","starttime":str(day),
                    "endtime":str(nextDay), "minmagnitude":str(threshold)}
        data = requests.get(url,params=parameters).json()
        dataLists.append(data)

    # find the max quakes day!
    list = [ len(data['features']) for data in dataLists ]
    maximum = max( list )
    i = list.index(maximum)
    quakiestday = datetime.date.fromordinal( todays_ordinal - i )

    print("With the following numbers of quakes (today -> back):", list)
    print("The quakiest day in the past week was", quakiestday)

    return quakiestday
print (quakiestDay(2.42))
