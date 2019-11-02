import ftplib
import re
import sys

vRegex = re.compile(r'\.(mkv|m4a|mp4)$')


def getTvList(connection, folder):
    connection.cwd(folder)
    f1List = connection.mlsd()
    showList = []         # Format --> [show, [ [s1, [e1, e2, ..]], [s2, [e1, e2, ..]], ..] ]
    for show in f1List:
        entry = []
        if show[1]['type'] == 'dir':
            seasonList = []
            connection.cwd(show[0])
            f2List = connection.mlsd()
            seasonList = []
            for season in f2List:
                if season[1]['type'] == 'dir':
                    episodeList = []
                    connection.cwd(season[0])
                    f3List = connection.mlsd()
                    for episode in f3List:
                        if vRegex.search(episode[0]):
                            episodeList.append(episode[0])
                    #Episodelist made
                    seasonList.append([season[0], episodeList])
                    connection.cwd('..')
            #SeasonList made
            entry = [show[0], seasonList]
            connection.cwd('..')
        showList.append(entry)
    connection.cwd('..')
    return showList


def getData(ipaddress, port):
    with ftplib.FTP() as ftp:
        ftp.connect(ipaddress, port)
        ftp.login()
        tvList = getTvList(ftp, 'TV Shows')
        return tvList
