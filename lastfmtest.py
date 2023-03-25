import requests
import math
import pandas
from bs4 import BeautifulSoup
from werkzeug.wrappers import Response
from datetime import datetime
from io import StringIO
import csv


def lastfm(username="Des321", songs=50, period="LAST_30_DAYS", filter="N"):
    l=[]
    include_pc = True
    pages = math.ceil(int(songs)/50)
    print(pages)
    #base_url="https://www.last.fm/user/"+username+"/library/tracks?date_preset="+period+"&page="
    base_url="https://www.last.fm/user/"+username+"/library/tracks"

    if filter == "T":
        kitkat = pandas.read_csv("filter.csv")

    counter = 0
    for page in range (1,pages+1,1):
        print(base_url+str(page))
        #exit()

        r=requests.get(base_url)
        c=r.content
        soup=BeautifulSoup(c,"html.parser")
        #print(soup)
        Artist=soup.find_all("td",{"class":"chartlist-artist"})
        #Artist=soup.find_all("td")
        print(Artist)
        #exit()
        Song=soup.find_all("td",{"class":"chartlist-name"})
        print(Song)
        PlayCount=soup.find_all("td",{"class":"chartlist-bar"})
        print(PlayCount)

        #exit()

        if filter != "T":

            for (a, b, c) in zip(Song,Artist,PlayCount):

                 d={}
                 d["Song"]=a.text.replace("\n","").replace("'","")
                 d["Artist"]=b.text.replace("\n","").replace("'","")
                 if include_pc == True:
                     d["PlayCount"]=c.text.replace("\n","").replace("scrobbles","").replace(" ","").replace("scrobble","")

                 if counter >= int(songs):
                     break
                 else:
                      l.append(d)
                      counter = counter + 1


        else:

            for (a, b, c) in zip(Song,Artist,PlayCount):

                 next = "False"
                 for index,row in kitkat.iterrows():
                     if row['Song'] == a.text.replace("\n","").replace("'","") and row['Artist'] == b.text.replace("\n","").replace("'",""):
                         next = "True"
                         break
                 if next == "True":
                     next = "False"
                     pass
                 else:

                     d={}
                     d["Song"]=a.text.replace("\n","").replace("'","")
                     d["Artist"]=b.text.replace("\n","").replace("'","")
                     if include_pc == True:
                         d["PlayCount"]=c.text.replace("\n","").replace("scrobbles","").replace(" ","").replace("scrobble","")

                     if counter >= int(songs):
                         break
                     else:

                          l.append(d)
                          counter = counter + 1


    df=pandas.DataFrame(l)
    """df.to_csv("C:\\"+username+"'s Top "+str(songs)+" "+period+".csv", index = False)"""
    file=list(zip(*map(df.get, df)))

    print(file)
    return file


lastfm(username="Des321", songs=50, period="LAST_365_DAYS", filter="N")

"""lastfm("Des321", 100, "LAST_365_DAYS", "T")"""
