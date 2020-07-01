# media-library

An in progress django application for organizing media files, specifically Movies & TV Shows.
Current support for adding ftp servers, need to change to allow for both local files and http links from servers for the in video player, and a way to play video files from other sources including local files.

## Setup the server

- Install all dependencies using Pipenv, and enter the pipenv shell.
    ```
    $ pipenv install
    $ pipenv shell
    ```
- Create a local_settings.py file from the media_library/settings/local_settings.py.sample and place it in the same settings directory. Remember to setup a Django secret key of your choice before running the application, and setup the database if you wish to not use the default sqlite3 database.
    ```
    $ cp media_library/settings/local_settings.py.sample media_library/settings/local_settings.py
    ```
    For example, after adding a secret key and using the default sqlite3 database
    ```
    $ cat media_library/settings/local_settings.py

    SECRET_KEY = 'random_sequence_of_characters'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    # Database
    # https://docs.djangoproject.com/en/2.2/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
    ```
- Setup a TMDB api key. This is necessary for scraping Movie & TV metadata, and you can obtain it from themoviedb.org . Afterwards, remember to export the API key as TMDB_API_KEY in your shell.
    ```
    $ TMDB_API_KEY=whatever_api_key_you_get
    ```
    If you're using bash, and don't want to keep repeating this step, add it to your bashrc as follows,
    ```
    $ echo export TMDB_API_KEY=whatever_api_key_you_get >> ~/.bashrc
    ```
- Make initial migrations for the database and setup it up
    ```
    $ python manage.py makemigrations users movies tvseries pages
    $ python manage.py migrate
    ```
    Also setup the TV and Movie Genres, which have to be added manually (hopefully a temporary fix)
    ```
    $ python manage.py movieGenreAddAll
    $ python manage.py tvGenreAdd
    ```
- Optionally, create a superuser for direct editing of the models using django's admin interface
    ```
    $ python manage.py createsuperuser
    ```
- Once you're done, start the dev server
    ```
    $ python manage.py runserver
    ```

## Adding sources

The website only supports basic FTP servers, however in order for this to work there is a required file structure. (again, hopefully temporary)
- The server contains a 'Movies' and 'TV Shows' folder, where the required Movies and TV Shows will be loaded.
- Movies follow a pattern of FOLDER/'MOVIE (YEAR) EXTRAINFO.mp4'.
- TV series follow a pattern of SHOW/SEASON/'NAME - SSxEE - EPISODENAME.mp4' where SS corresponds to Season Number and EE to Episode number.
- Extension can be any video format.
- Also make sure the FTP server has no login credentials, if you wish to add that then you have to hardcode it to the corresponding addFTP.py file

For example, using linux's ftp on terminal
```
$ ftp 192.168.43.1 2121

Connected to 192.168.43.1.
220 ---------- Welcome to MiXplorer v6.40.3-B19101820 ----------
Name (192.168.43.1:user):
331 USER send password
Password:
230 PASS access granted
Remote system type is UNIX.
Using binary mode to transfer files.

ftp> ls
200 PORT Done
150 LIST ASCII opening...
drwxr-xr-x 1 10189 10189            0 Jun 27 11:16 Movies
drwxr-xr-x 1 10189 10189            0 Jun 27 11:10 TV Shows
226 LIST Done
```
Add it then using the in form in the website page itself, using the appropriate IP address and Port number