import requests
import re
import os

URL = 'https://api.themoviedb.org/3/search/movie'
API_KEY = os.environ['TMDB_API_KEY']
BACKDROP_BASE = 'http://image.tmdb.org/t/p/'

# Movie filename follows format
# FOLDER/'MOVIENAME (YEAR) EXTRA INFO.EXT'
vRegex = re.compile(r'''
    .*/         # Folder in which file is placed
    (.*)\s      # Name of movie
    \((\d{4})\) # (YEAR)
    .*          # Any extra characters in name
    \.\w{3}$    # File extension
''', re.VERBOSE)


def getMetadata(query, year='', json_flag=True):
    parameters = {'api_key': API_KEY,
                  'query': query, 'language': 'en-US', 'page': 1}
    if year != '':
        parameters['year'] = year
    response = requests.get(URL, params=parameters)
    if json_flag:
        return response.json()['results'][0]
    else:
        return response.text


def getMetadataList(movieList):
    metadataList = []
    for movie in movieList:
        metadataEntry = {}
        parsed = vRegex.search(movie)

        movieJson = getMetadata(parsed.group(1), year=parsed.group(2))

        metadataEntry['Url'] = movie
        metadataEntry['Name'] = parsed.group(1)
        metadataEntry['Year'] = parsed.group(2)
        metadataEntry['MediaID'] = 'MV' + \
            str(movieJson['id']).rjust(8 - len(str(movieJson['id'])), '0')
        metadataEntry['Poster'] = BACKDROP_BASE + \
            'w500' + movieJson['poster_path']
        metadataEntry['Description'] = movieJson['overview']
        metadataEntry['Rating'] = movieJson['vote_average']
        metadataEntry['Genres'] = movieJson['genre_ids']
        metadataList.append(metadataEntry)
    return metadataList


# {'adult': False,
#  'backdrop_path': '/9pkZesKMnblFfKxEhQx45YQ2kIe.jpg',
#  'genre_ids': [27, 53],
#  'id': 381288,
#  'original_language': 'en',
#  'original_title': 'Split',
#  'overview': 'Though Kevin has evidenced 23 personalities to his trusted '
#              'psychiatrist, Dr. Fletcher, there remains one still submerged '
#              'who is set to materialize and dominate all the others. Compelled '
#              'to abduct three teenage girls led by the willful, observant '
#              'Casey, Kevin reaches a war for survival among all of those '
#              'contained within him — as well as everyone around him — as the '
#              'walls between his compartments shatter apart.',
#  'popularity': 37.719,
#  'poster_path': '/rXMWOZiCt6eMX22jWuTOSdQ98bY.jpg',
#  'release_date': '2016-09-26',
#  'title': 'Split',
#  'video': False,
#  'vote_average': 7.3,
#  'vote_count': 11016}
