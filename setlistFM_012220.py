"""
This file calls to the setlistFM API.
-Passes an "Artist Name". 
-Resopnse is a Dictioary.
-The Dictionary contains a key value for "Artist"
- The value associated with the "Artist" Key is a LIST of Dictionaries.
-This Script process the response as follows:
	1. Sort Down to the "Artist" Key
	2. Search the LIST value associate with the "Artist" Key for the Artist "sortName"
	3. This returns a single Dictionary, the first where the seached for "sortName" is found.
	4. Calls the ['mbid'] key value from the single returned Dictionary.
The Music Brainz ID appears to be used as a defacto index within the setlistFM data.

GOAL:

=PRovide for User Input of the Artist Name.
-Pass the artist name and Mbid to an output table.
-Use "Append" functionality to maintain the output table, a master list of Mbids and Artists.
-Script should:
	Query the table of Mbids and Artists to see if values for the currently queried Artist are present.
	Pass values to the table if they are not.
-The Table should accrue values for every query made.

FURTHER GOALS

-Entering an Artist should first Query the Table for Mbid values.
-If present, the script should pull the values, and give the user option to progress and make more granular
queries (setlists...)
- If not then the functions above should execute... Mbid gathered and passed to master table.
"""

import json
import csv
import requests


userArtistIn = input(f"What Artist are you interested in? ")
userArtist = userArtistIn.replace(' ','%20')
headers = {
    'Accept': 'application/json',
    'x-api-key': 'hqklOe2QH1XbmtW6Wbgd1dtm9N7MjFxJ1hnq',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

response = requests.get('https://api.setlist.fm/rest/1.0/search/artists?artistName='+userArtist+'&p=1&sort=sortName', headers=headers)
jsonObject = response.json()
mbidTableVal = []
print(f"AFter declaring the var len(mbidTableVal) = {len(mbidTableVal)}")
with open ('mbidTable.csv','r') as csvInputFile:
    filereader = csv.reader(csvInputFile)
    for line in filereader:
        for cell in line:
            if cell == userArtistIn:
                mbidTableVal.append(line[1])
print(f"After the midTable open and query the mbidTableVal is {mbidTableVal}")
def mbidTableUpdate(mbidOutput):
    with open ('mbidTable.csv','a', newline='') as csvOutputFile:
        filewriter = csv.writer(csvOutputFile)
        filewriter.writerow(mbidOutput)

if len(mbidTableVal)== 0:
    mbidOutput = [userArtistIn, mbidTableVal]
    mbidTableUpdate(mbidOutput)

with open (userArtist+'.json','w') as jsonOutputFileScratch:
    filewriter = json.dump(jsonObject,jsonOutputFileScratch)

"""
Logic Pivot using >>>
if len(mbidTableVal) ....

"""

#print(f"The value of mbidTableVal is: {mbidTableVal}")
#print(f"The vale of len(mbidTableVal) is {len(mbidTableVal)}")
#with open ('PJsetlistQueryOutput1156am.json','r') as jsonInputFile:
#print(f"Confirming the vale of 'jsonObject': {jsonObject}")
mbidValSearchableObj = jsonObject['artist']
#print(mbidValSearchableObj)
mbidValFinder = next((item for item in mbidValSearchableObj if item["sortName"] == userArtistIn),False)
#mbidValFinder = next((item for item in jsonObject if item["sortName"] == "Pearl Jam"), False)
#mbidValFinder = next((item for item in jsonObject if item["sortName"] == "Pearl Jam"),False)
if mbidValFinder == False:
    prepLastFirst = userArtistIn.replace(' ',',')
    splitVar = prepLastFirst.split(",")
    print(f"The value of splitVar is {splitVar}")
    print(f"The value of splitVar[0] is {splitVar[0]}")
    print(f"The value of splitVar[1] is {splitVar[1]}")
    lastFirst = (splitVar[1]+', '+splitVar[0])
    print (f"The value of lastFirst is {lastFirst}")
    mbidValFinder = next((item for item in mbidValSearchableObj if item[ "sortName" ] == lastFirst), False)
print(f"Confirming the post Generator value of 'mbidValFinder' is {mbidValFinder}")
mbid = mbidValFinder['mbid']
print(f"Confirming the value of 'mbid' is: {mbid}")

if len(mbidTableVal)== 0:
    mbidOutput = [userArtistIn, mbid]
    mbidTableUpdate(mbidOutput)


"""
Section for extracting Mbid ... Music Brainz ID.

with open('output1220.json','r') as nextJsonInputFile:
    nextParseFile = json.load(nextJsonInputFile)
print(nextParseFile)
print("The next statement is below this")
#next(item for item in dicts if item["name"] == "Pam")
tryOut = next((item for item in nextParseFile if item["sortName"] == "Pearl Jam"),False)

print(f"The value for 'tryOut'+mbid is: {tryOut['mbid']}")

"""

#curl -X GET —header 'Accept: application/json' —header 'x-api-key:hqklOe2QH1XbmtW6Wbgd1dtm9N7MjFxJ1hnq'--url 'https://api.setlist.fm/rest/1.0/artist/0bfba3d3-6a04-4779-bb0a-df07df5b0558'

"""
X-Firefox-Spdy: h2
content-length: 23
content-type: application/json
date: Mon, 20 Jan 2020 22:27:48 GMT
via: 1.1 fd5bb5b63be18c34495bdbea44226476.cloudfront.net (CloudFront)
x-amz-apigw-id: GntnsGtdIAMFynQ=
x-amz-cf-id: zgr90fWopfH70D-gXRHTueaHudQ71-tX2OAN8bMllW_4qu1SGfpZCQ==
x-amz-cf-pop: EWR52-C3
x-amzn-errortype: ForbiddenException
x-amzn-requestid: a60ffdd8-aadc-458f-b2a2-8aca4fe48eaa
x-cache: Error from cloudfront

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.5
Connection: keep-alive
DNT: 1
Host: api.setlist.fm
Referer: https://api.setlist.fm/docs/1.0/resource__1.0_search_artists.html
TE: Trailers
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0


GET /1.0/search/artists
Accept: application/json

__________________________________


rootURI = 'http://ws.audioscrobbler.com/2.0/'
keyChain = '&api_key='
apiKey = '49b1113c175157f4e71b434017fd0a6d'
endRequest = '&format=json'

# Queries
#albumSearch
#JSON: /2.0/?method=album.search&album=believe&api_key=YOUR_API_KEY&format=json

albumSearch = '?method=album.search&album='

#userArtist = input("What artist would you like to review? ")

#RAW CALLER (USING LITERAL URI)
import requests
import json
response = requests.get("http://ws.audioscrobbler.com//2.0/?method=geo.gettopartists&country=spain&api_key=49b1113c175157f4e71b434017fd0a6d&format=json")
tranferBlock = response.json()
with open ('transferBlockGEO.json','w',newline='') as jsonOutputFile:
	filewriter = json.dump(tranferBlock,jsonOutputFile)

print(response.status_code)
print(response.json())




def getSimilarArtist(userArtist):
#	rootURI = 'http://ws.audioscrobbler.com/2.0/'
	queryCall ='?method=artist.getsimilar&artist='
#	keyChain = '&api_key='
#	apiKey = '49b1113c175157f4e71b434017fd0a6d'
#	endRequest = '&format=json'
	outputBlock = []
	response = requests.get(rootURI+queryCall+userArtist+keyChain+apiKey+endRequest)
	transferBlock = response.json()
	parseBlock = transferBlock['similarartists']['artist']
	for x in parseBlock:
		del x['image']
		outputBlock.append(x)
	with open (userArtist+'_getSimilarArtist.json','w',newline='') as jsonOutputFile:
		filewriter = json.dump(outputBlock,jsonOutputFile)

	print("This statement should print when the script has successfully executed.")

#getSimilarArtist(userArtist)

userRegion = input("What region would you like to see detail on Top artists for?")

def georArtist(userRegion):
#	rootURI = 'http://ws.audioscrobbler.com/2.0/'
	queryCall ='?method=geo.gettopartists&country='
#	keyChain = '&api_key='
#	apiKey = '49b1113c175157f4e71b434017fd0a6d'
#	endRequest = '&format=json'
	outputBlock = []
	response = requests.get(rootURI+queryCall+userRegion+keyChain+apiKey+endRequest)
	transferBlock = response.json()
	parseBlock = transferBlock['topartists']['artist']
	for x in parseBlock:
		del x['image']
		outputBlock.append(x)
	with open (userRegiont+'_geoArtist.json','w',newline='') as jsonOutputFile:
		filewriter = json.dump(outputBlock,jsonOutputFile)

	print("This statement should print when the script has successfully executed.")

getSimilarArtist(userRegion)
#artistGetSimilar
#JSON: /2.0/?method=artist.getsimilar&artist=cher&api_key=YOUR_API_KEY&format=json



#getAlbumInfo
#JSON: /2.0/?method=album.getinfo&api_key=YOUR_API_KEY&artist=Cher&album=Believe&format=json

#ARTIST
#artistGetinfo
#JSON: /2.0/?method=artist.getinfo&artist=Cher&api_key=YOUR_API_KEY&format=json

#artistGetSimilar
#JSON: /2.0/?method=artist.getsimilar&artist=cher&api_key=YOUR_API_KEY&format=json

#artistGetTopAlbums
#JSON: /2.0/?method=artist.gettopalbums&artist=cher&api_key=YOUR_API_KEY&format=json

#artistGetTopTracks
#artistGetTopAlbums
#JSON: /2.0/?method=artist.gettoptracks&artist=cher&api_key=YOUR_API_KEY&format=json


#artistGeoGetTopArtists
#JSON: /2.0/?method=geo.gettopartists&country=spain&api_key=YOUR_API_KEY&format=json



keyChain = '&api_key='
apiKey = '49b1113c175157f4e71b434017fd0a6d'

endRequest = '&format=json'




topU2Albums = requests.get('http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist=u2&api_key=49b1113c175157f4e71b434017fd0a6d&format=json')
#filereader = json.loads(topU2Albums)
outcome = topU2Albums.json()
with open ('u2.json','w',newline='') as jsonOutputFile:
    filewriter = jsonOutputFile
    json.dump(outcome,filewriter)
print(outcome)

albumSearch = '?method=album.search&album='

#/2.0/?method=album.search&album=believe&api_key=YOUR_API_KEY&format=json


outputBlock = []
response = requests.get("http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist=brianeno&api_key=49b1113c175157f4e71b434017fd0a6d&format=json")
transferBlock = response.json()
parseBlock = transferBlock['toptracks']['track']
for x in parseBlock:
	del x['image']
	outputBlock.append(x)
with open ('FRIDAYartistOut2.json','w',newline='') as jsonOutputFile:
	filewriter = json.dump(outputBlock,jsonOutputFile)

"""
