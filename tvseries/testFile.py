import pprint
import addDirFTP
import tmdbCaller

tvList = addDirFTP.getData('192.168.43.1', 2121)
tvList = tmdbCaller.getMetadataList(tvList)
pprint.pprint(tvList)
