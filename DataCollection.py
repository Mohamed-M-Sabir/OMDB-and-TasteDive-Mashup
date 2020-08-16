import requests_with_caching
import json


def get_movies_from_tastedive(m):
    baseurl = "https://tastedive.com/api/similar"
    parameters = {"q": m, "type": "movies", "limit": 5}
    mo = requests_with_caching.get(baseurl, params=parameters)
    pydata = mo.json()
    print(mo.url)
    return (pydata)


def extract_movie_titles(m):
    lst = []
    for i in m['Similar']['Results']:
        lst.append(i['Name'])
    return lst


def get_related_titles(lstm):
    relatedlst = []
    for movie in lstm:
        lst = extract_movie_titles(get_movies_from_tastedive(movie))
        for i in lst:
            if i not in relatedlst:
                relatedlst.append(i)
    return relatedlst


def get_movie_data(movie):
    baseurl = "http://www.omdbapi.com/"
    parameters = {"t": movie, "r": "json"}
    mo = requests_with_caching.get(baseurl, params=parameters)
    return mo.json()


def get_movie_rating(dic):
    rating = ""
    for i in dic["Ratings"]:
        if i['Source'] == 'Rotten Tomatoes':
            # print(int(i['Value'][:2]))
            rating = i['Value']
    if rating != "":
        ratings = int(rating[:2])
    else:
        ratings = 0
    print(ratings)
    return ratings


def get_sorted_recommendations(lst):
    related = get_related_titles(lst)
    sortedlst = sorted(related, key=lambda movie: (get_movie_rating(get_movie_data(movie)), movie), reverse=True)
    return sortedlst


get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
