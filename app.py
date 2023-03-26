import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
"""from flask_session import Session"""
from tempfile import mkdtemp
import datetime
import pandas as pd
from lastfm import lastfm
from werkzeug.wrappers import Response
from io import StringIO
import csv
import lastfmapi


# Configure application
app = Flask(__name__)

@app.route("/", methods =["GET","POST"])

def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        """print("hello")"""
        username = request.form.get('username')
        songs = request.form.get('songs')
        period = request.form.get('period')
        pc = request.form.get('pc')
        filter = request.form.get('filter')



        r = lastfm_get({
            'method': 'user.gettoptracks',
            'user': username,
            'limit': songs,
            'period': period
        })
        """print(file)"""

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


        # def generate(x):
        #     data = StringIO()
        #     w = csv.writer(data)
        #
        #     # write header
        #     if pc == 'T':
        #         w.writerow(('Song', 'Artist','Playcount'))
        #     else:
        #         w.writerow(('Song', 'Artist'))
        #     yield data.getvalue()
        #     data.seek(0)
        #     data.truncate(0)
        #
        #     # write each log item
        #     for item in x:
        #         if pc =='T':
        #             w.writerow((
        #                 item[0],
        #                 item[1],
        #                 item[2]
        #             ))
        #         else:
        #             w.writerow((
        #                 item[0],
        #                 item[1],
        #             ))
        #
        #         yield data.getvalue()
        #         data.seek(0)
        #         data.truncate(0)
        #
        #     # stream the response as the data is generated
        # response = Response(generate(file), mimetype='text/csv')
        # # add a filename
        # response.headers.set("Content-Disposition", "attachment", filename=username+"'s Top "+str(songs)+" "+period+".csv")
        # return response
        #
        # """return render_template('index.html')"""





@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home():
    return redirect('/')

"""if __name__=="__main__":
    app.run(debug=True)"""
