from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import requests
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the form data
        user_agent = request.form['user_agent']
        limit = request.form['limit']
        period = request.form['period']
        YOUR_API_KEY = '514456374eb1fd87b2bce60cf9643662'

        # Query the Last.fm API for the user's top tracks
        url = f'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user={user_agent}&api_key={YOUR_API_KEY}&format=json&limit={limit}&period={period}'
        response = requests.get(url)
        data = response.json()['toptracks']['track']

        # Create a dataframe of the top tracks
        top_tracks_df = pd.DataFrame({'artist': [track['artist']['name'] for track in data],
                                       'track': [track['name'] for track in data],
                                       'play_count': [int(track['playcount']) for track in data]})

        # Create a list of track URIs
        token = util.prompt_for_user_token(
        username='1231949457',
        scope='playlist-modify-private,playlist-modify-public,user-library-read',
        client_id='98f367dcd59542829594cf72533787d8',
        client_secret='00e41e05c04b44a88eefa5c3d0a5f188',
        redirect_uri='http://localhost:8888/callback'
        )

        sp = spotipy.Spotify(auth=token)
        track_uris = []
        for i, row in top_tracks_df.iterrows():
            result = sp.search(q=f"artist:{row['artist']} track:{row['track']}", type='track')
            if result['tracks']['items']:
                track_uris.append(result['tracks']['items'][0]['uri'])
            else:
                track_uris.append('')

        # Get the user's Spotify username
        user = sp.me()['id']

        # Create a new playlist in the user's account
        playlist_name = f"{limit} Top Tracks ({period})"
        playlist_description = f"Top {limit} tracks for {user_agent} in the {period} period"
        new_playlist = sp.user_playlist_create(user, playlist_name, public=False, description=playlist_description)

        # Add the top tracks to the playlist
        sp.playlist_add_items(new_playlist['id'], track_uris)

        # Render the success page
        return render_template('success.html', playlist_name=playlist_name, playlist_description=playlist_description)
    else:
        # Render the form page
        return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
