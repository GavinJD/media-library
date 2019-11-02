import ftplib
import re
import sys

vRegex = re.compile(r'\.(mkv|m4a|mp4)$')


def getMovieList(connection, folder):
    connection.cwd(folder)
    fileList = connection.mlsd()
    resultList = []
    for f in fileList:
        if f[1]['type'] == 'file' and vRegex.search(f[0]):
            resultList.append(f[0])
        elif f[1]['type'] == 'dir':
            fList = getMovieList(connection, f[0])
            resultList += [(f'{f[0]}/' + x) for x in fList]
    connection.cwd('..')
    return resultList


def getData(ipaddress, port):
    with ftplib.FTP() as ftp:
        ftp.connect(ipaddress, port)
        ftp.login()
        movieList = getMovieList(ftp, 'Movies')
        return movieList
