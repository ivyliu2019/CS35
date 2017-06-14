# coding: utf-8

"""
#
# Using the Web's Wisdom to answer the question
#
#     Which college will win the football game?
#
#
"""
    # 2016:
    # team_1 = 'USC'
    # team_2 = 'Texas'
    #
    # 2017:
    # team_1 = 'LSU'
    # team_2 = 'Alabama'

#
# Here is our "web scavenging" approach:
# 1. first we grab the pages that define the teamthe of each college's colors
# 2. then, use bs4 to parse those pages and return a list of colors
# 3. then, grab the page that defines the popularity of team colors
# 4. finally, use bs4 to compute a score for each team based on its colors
#

import requests
from bs4 import BeautifulSoup
import random

#
# get_color_page()
#
def get_color_page():
    """ This function requests the most-popular-colors page
        and parses it with Beautiful Soup, returning the resulting
        Beautiful Soup object, soup
    """
    color_popularity_url = "https://www.thetoptens.com/female-least-favorite-colors/"
    response = requests.get(color_popularity_url)   # request the page

    if response.status_code == 404:                 # page not found
        print("There was a problem with getting the page:")
        print(color_popularity_url)

    data_from_url = response.text                   # the HTML text from the page
    soup = BeautifulSoup(data_from_url,"lxml")      # parsed with Beautiful Soup
    return soup


#
# find_color_score( color, soup )
#
def find_color_score( color_name, soup ):
    """ find_color_score takes in color_name (a string represnting a color)
        and soup, a Beautiful Soup object returned from a successful run of
        get_color_page

        find_color_score returns our predictive model's number of points in
        a potential match up involving a team with that color

        if the color is not on the list, we will assign a random number in the
        range of 10.
    """
    ListOfDivs = soup.findAll('div', {'class':"i"})   # the class name happens to be 'i' here...

    for div in ListOfDivs:
        # print(div.em, div.b)                    # checking the subtags named em and b
        this_divs_color = div.b.text.lower()      # getting the text from them (lowercase)
        this_divs_ranking_as_str = div.em.text    # this is the _string_ of the ranking

        this_divs_ranking = random.randint(0,9)
        try:
            this_divs_ranking = int(div.em.text)  # try to convert it to an integer
        except:                                   # if it fails
            pass                                  # do nothing and leave it at 21

        if color_name == this_divs_color:         # check if we need to return this one
            return this_divs_ranking
    # if we ran through the whole for loop without finding a match, the ranking is 21
    return random.randint(0,9)     

#
# get_university_colors_page()
#
def get_university_colors_page():
    """ get_university_colors_page takes in a string of the name of university
        it tried to request the appropriate page and parse it with Beautiful
        Soup and it should return that soup object
    """
    university_color_url = "http://fanindex.usatoday.com/2014/09/15/the-10-best-team-colors-in-college-football/"
    response = requests.get(university_color_url)         # request the page

    if response.status_code == 404:                 # page not found
        print("There was a problem with getting the page")
        print(university_color_url)

    data_from_url = response.text                   # the HTML text from the page
    soup = BeautifulSoup(data_from_url,"lxml")      # parsed with Beautiful Soup
    print (data_from_url.encode('ascii', 'ignore').decode('ascii', 'ignore'))
    return soup

#
# extract_universty_colors( soup, school )
#
def extract_universty_colors(soup, school):
    """ extract_university_colors takes in a beautiful soup object, soup
        and uses Beautiful Soup to extract a list of all of color of each school
        it return that list of colors
    """
    AllDivs = soup.findAll('h2')
    list_of_school_colors = {}
    Words = []
    for item in AllDivs:
        Words += [item.text.split()]
        numList = ['1.','2.', '3.', '4.', '5.','6.', '7.', '8.', '9.','10.' ]
    actualList = [x[1:] for x in Words if x[0] in numList]
    for university in actualList:
        hex_index = university.index('and')
        if len(university) >= 6:
            school = university[:hex_index-2]
            color = university[ hex_index-2: ]
            list_of_school_colors[' '.join(school)] = ' '.join(color)
        else:
            school = university[:hex_index-1]
            color = university[ hex_index-1: ]
            list_of_school_colors[' '.join(school)] = ' '.join(color)
    return list_of_school_colors[' '.join(school)]

#
# put it all together!
#
def main():
    """
    # Here is an example of using the Web's Wisdom to answer the question
    #
    #     Which college will win the football game?
    #
    #
    """
    # 2016:
    # team_1 = 'USC'
    # team_2 = 'Texas'

    # 2017:
    team_1 = 'LSU'
    team_2 = 'Alabama'

    #
    # Here is our "web scavenging" approach:
    #
    # 1. first we grab the pages that define the team of each college's colors
    # 2. then, use bs4 to parse those pages and return a list of colors
    # 3. then, grab the page that defines the popularity of colors
    # 4. finally, use bs4 to compute a score for each team based on its colors
    #

    # we get the team colors page
    # and we return a BeautifulSoup "soup" object for each!
    soup = get_university_colors_page()

    # We have a function that actually grabs the colors from the page...
    team_colors_1 = extract_universty_colors( soup, team_1 )
    team_colors_2 = extract_universty_colors( soup, team_2 )
    print("Team 1 (" + team_1 + ") colors:", team_colors_1)
    print("Team 2 (" + team_2 + ") colors:", team_colors_2)

    print("Done scraping the team colors.\n")

    # Next, we grab the color-popularity page (and parse it into
    # a BeautifulSoup object...
    #
    color_popularity_soup = get_color_page()
    print("\nDone scraping the color-popularity page.\n")

    # Finally, we convert the team colors into total scores
    # which will reveal our predicted result
    # Admittedly, our "points" are simply the ranking of how popular a color is.

    # let's use a list comprehension as a reminder of how those work...
    team_1_scores = [ find_color_score(clr, color_popularity_soup) for clr in team_colors_1 ]
    team_2_scores = [ find_color_score(clr, color_popularity_soup) for clr in team_colors_2 ]
    print("Team 1's (" + team_1 + ") scores:", team_1_scores)
    print("Team 2's (" + team_2 + ") scores:", team_2_scores)
    print()
    print("Team 1's (" + team_1 + ") predicted final score:", sum(team_1_scores))
    print("Team 2's (" + team_2 + ") predicted score:", sum(team_2_scores))

    # that's it!
    return
main()
