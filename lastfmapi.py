API_KEY = '514456374eb1fd87b2bce60cf9643662'
#USER_AGENT = input("User? ")
#limit = int(input("Number of tracks? "))
#period = input("Period? (overall, 7day, 1month, 3month, 6month, 12month)")

#user (Required) : The user name to fetch top tracks for.
#period (Optional) : overall | 7day | 1month | 3month | 6month | 12month - The time period over which to retrieve top tracks for.
#limit (Optional) : The number of results to fetch per page. Defaults to 50.
#page (Optional) : The page number to fetch. Defaults to first page.
#api_key (Required) : A Last.fm API key.

import requests
import json
import pandas as pd
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)



r = lastfm_get({
    'method': 'user.gettoptracks',
    'user': USER_AGENT,
    'limit': limit,
    'period': period
})


data = r.json()
tracks = data['toptracks']['track']
df = pd.DataFrame(columns = ["track", "artist", "playcount"])
for track in tracks:

    track_name = track['name']
    artist = track['artist']['name']
    playcount = int(track['playcount'])
    df= df.append({"track":track_name, "artist":artist, "playcount": playcount},ignore_index = True)


# Set up Spotify API credentials and authenticate with Spotify

token = util.prompt_for_user_token(
username='1231949457',
scope='playlist-modify-private,playlist-modify-public,user-library-read',
client_id='98f367dcd59542829594cf72533787d8',
client_secret='00e41e05c04b44a88eefa5c3d0a5f188',
redirect_uri='http://localhost:8888/callback'
)

sp = spotipy.Spotify(auth=token)

# Create a new Spotify playlist with a given name and description
playlist_name = USER_AGENT + "'s Top "+str(limit)+" tracks "+period
playlist_description = "A playlist of my top Last.fm tracks"
playlist = sp.user_playlist_create(user=sp.current_user()["id"], name=playlist_name, description=playlist_description)

# Iterate through the rows of the DataFrame and add each track to the playlist
for i, row in df.iterrows():
    artist = row["artist"]
    track = row["track"]
    results = sp.search(q="artist:{} track:{}".format(artist, track), type="track")
    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        sp.playlist_add_items(playlist_id=playlist["id"], items=[track_uri])
