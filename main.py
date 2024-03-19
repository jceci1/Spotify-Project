import os
import spotipy

from pytube import YouTube
from youtubesearchpython import VideosSearch
from spotipy.oauth2 import SpotifyOAuth



# Replace with your own client ID and client secret
CLIENT_ID = 'Insert Client ID Here'
CLIENT_SECRET = 'Insert Client Secret Here'
REDIRECT_URI = 'http://localhost:5000/callback'  


# Create a spotipy client with user authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope="playlist-read-private"))

# Get the playlist by name
playlists = sp.current_user_playlists()
playlist_id = None
for playlist in playlists['items']:
    if playlist['name'] == 'Test':
        playlist_id = playlist['id']
        break


# Get the tracks in the playlist
tracks = sp.playlist_tracks(playlist_id)


# Iterate through the tracks and print their names and artists
trackDetails = []

for item in tracks['items']:
    tempList = []
    track = item['track']
    

    tempList.append(track['name'])
  
    for artist in track['artists']:
  
        tempList.append(artist['name'])

    trackDetails.append(tempList)


download_directory = 'directory to be downloaded to'

for track in trackDetails:
    search = " ".join(track)
    videosSearch = VideosSearch(search, limit=1)
    video_url = videosSearch.result()['result'][0]['link']
    yt = YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    output_file = f"{download_directory}/{yt.title}"
    stream.download(output_path=download_directory, filename=yt.title)
    print(f"Downloaded audio for {track[0]}, {track[1]}")



