#!/usr/bin/env python
## ToDO create a dict with yifyid as key and a list for each key, list to contain all the info needed to generate a magnet link
#
# Created on 10-15-16
# @author: NHolbrook
#     GNU GENERAL PUBLIC LICENSE - Version 3
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#     http://www.gnu.org/licenses/gpl-3.0.txt
#

import json, urllib2, logging, urllib
from time import gmtime, strftime

baseurl = "http://yts.ag/api/v2/"


logging.basicConfig(filename='info.log',level=logging.INFO)
timeStamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())


#make a api call return parsed json
## Requires 2 args, the api url and video quality in a string format (e.g. '1080p or '720p'
### api returns nested json, this nested mess works its way down to the urls for the chosen quality (720p oe 1080p) and adds them to the "array_of_magnet_links"
def json_api_call(url,videoQuality):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')] # yify api needs a browser type
    json_obj = opener.open(url)
    data = json.load(json_obj)
    movies = data['data']['movies']
    array_of_magnet_links = []

    for each in range(len(movies)):
        title = movies[each]['title']
        availableTorrents = movies[each]['torrents']
        for x in range(len(availableTorrents)):
            x = availableTorrents[x]
            quality = x['quality']
            url = x['url']
            hash = x['hash']
            if quality == videoQuality:
                magnet = create_magnet_link(hash,url,title)
                array_of_magnet_links.append(magnet)
    return array_of_magnet_links

#need the hash, url,  title (encoded)
#create magnet links
def create_magnet_link(hash,url,title):
    trackers = ["udp://open.demonii.com:1337","udp://tracker.istole.it:80","http://tracker.yify-torrents.com/announce","udp://tracker.publicbt.com:80", "udp://tracker.openbittorrent.com:80", "udp://tracker.coppersurfer.tk:6969", "udp://exodus.desync.com:6969", "http://exodus.desync.com:6969/announce"]
    tracker = ""
    for each in trackers:
        tracker += each
        tracker +="&tr="
    tracker = tracker[:-4]
    title = urllib.quote_plus(title)
    magnet = "magnet:?xt=urn:btih:" + hash + "&dn=" + title + "&tr=" + tracker
    return magnet
#check existing downloads and remove any duplicates
def dedupeArray(arrayToBeDeduped):
    dedupedArray = []
    referenceArray = []
    #load referenceArray from a txt, each line == item in list
    f = open('previouslyDownloadedMovies.txt','r')
    referenceArray = list(f)

    for each in arrayToBeDeduped:
        if each not in referenceArray:
            dedupedArray.append(each)
    return dedupedArray


#make magnet links from remaining results and add to existing downloads
# magnet:?xt=urn:btih:TORRENT_HASH&dn=Url+Encoded+Movie+Name&tr=http://track.one:1234/announce&tr=udp://track.two:80
if __name__ == '__main__':
    urls_from_yify = json_api_call("https://yts.ag/api/v2/list_movies.json?quality=1080&limit=50", '1080p')

    magnet_links_to_download = dedupeArray(urls_from_yify)

    f = open('movies_to_download_from_YIFY.magnet','a')
    f2 = open('previouslyDownloadedMovies.txt', 'a')
    for each in magnet_links_to_download:
        f.write(each + "\n")
        f2.write(each + "\n")

# listOfUrlsToDownload = dedupeArray(urlsFrom_YIFY)
