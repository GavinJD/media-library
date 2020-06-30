import requests
import re
import os

URL = 'https://api.themoviedb.org/3/search/tv'
API_KEY = os.environ['TMDB_API_KEY']
BACKDROP_BASE = 'http://image.tmdb.org/t/p/'

yRegex = re.compile(r'(\d{4}).*')


def getMetadata(query, json_flag=True):
    parameters = {'api_key': API_KEY,
                  'query': query, 'language': 'en-US', 'page': 1}
    response = requests.get(URL, params=parameters)
    if json_flag:
        return response.json()['results'][0]
    else:
        return response.text


def getMetadataList(tvList):
    # Format --> [show, metadata, [ [s1, [e1, e2, ..]], [s2, [e1, e2, ..]], ..] ]
    for show in tvList:
        show_name = show[0]
        showJson = getMetadata(show_name)
        metadataEntry = {}
        metadataEntry['Name'] = show_name
        metadataEntry['Year'] = yRegex.search(
            showJson['first_air_date']).group(1)
        metadataEntry['MediaID'] = 'TV' + \
            str(showJson['id']).rjust(8 - len(str(showJson['id'])), '0')
        metadataEntry['Poster'] = BACKDROP_BASE + \
            'w500' + showJson['poster_path']
        metadataEntry['Description'] = showJson['overview']
        metadataEntry['Rating'] = showJson['vote_average']
        metadataEntry['Genres'] = showJson['genre_ids']
        show.insert(1, metadataEntry)
    return tvList

#  "original_name": "Avatar: The Last Airbender",
#  "genre_ids": [
#    28,
#    12,
#    16,
#    14
#  ],
#  "name": "Avatar: The Last Airbender",
#  "popularity": 29.94,
#  "origin_country": [
#    "US"
#  ],
#  "vote_count": 555,
#  "first_air_date": "2005-02-21",
#  "backdrop_path": "/732azfQ0xUAJNQ48pPfVtCCLVlZ.jpg",
#  "original_language": "en",
#  "id": 246,
#  "vote_average": 8.3,
#  "overview": "In a war-torn world of elemental magic, a young boy reawakens to undertake a dangerous mystic quest to fulfill his destiny as the Avatar, and bring peace to the world.",
#  "poster_path": "/sB8V0pQtJZ17v8FLXMOcYz6045c.jpg"
