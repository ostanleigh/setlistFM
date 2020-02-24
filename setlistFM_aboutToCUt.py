"""
This file calls to the setlistFM API.
-Passes an "Artist Name".  (
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

"""
import json
import csv
import requests


userArtistIn = input(f"What Artist are you interested in? (Eg. 'U2'): ")
userArtist = userArtistIn.replace(' ','%20')
artistPassVal = userArtistIn
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

with open (userArtist+'.json','w') as jsonOutputFileScratch:
    filewriter = json.dump(jsonObject,jsonOutputFileScratch)


def mbidTableUpdate(mbidOutput):
    with open ('mbidTable.csv','a', newline='') as csvOutputFile:
        filewriter = csv.writer(csvOutputFile)
        filewriter.writerow(mbidOutput)

with open (userArtist+'.json','w') as jsonOutputFileScratch:
    filewriter = json.dump(jsonObject,jsonOutputFileScratch)



mbidValSearchableObj = jsonObject['artist']
mbidValFinder = next((item for item in mbidValSearchableObj if item["sortName"] == userArtistIn),False)
if mbidValFinder == False:
    prepLastFirst = userArtistIn.replace(' ',',')
    splitVar = prepLastFirst.split(",")
    print(f"The value of splitVar is {splitVar}")
    print(f"The value of splitVar[0] is {splitVar[0]}")
    print(f"The value of splitVar[1] is {splitVar[1]}")
    lastFirst = (splitVar[1]+', '+splitVar[0])
    print (f"The value of lastFirst is {lastFirst}")
    mbidValFinder = next((item for item in mbidValSearchableObj if item[ "sortName" ] == lastFirst), False)
    artistPassVal = lastFirst
print(f"Confirming the post Generator value of 'mbidValFinder' is {mbidValFinder}")
mbid = mbidValFinder['mbid']
print(f"Confirming the value of 'mbid' is: {mbid}")

if len(mbidTableVal)== 0:
    mbidOutput = [artistPassVal, mbid]
    mbidTableUpdate(mbidOutput)
