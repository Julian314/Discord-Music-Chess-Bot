import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import random

def spotify_playlist(results, sp):
    '''RETURNS A LIST OF SONG NAMES AND ARTIST NAMES FROM A SPOTIFY PLAYLIST'''
    songs = []
    for item in results['tracks']['items']:
        track = item['track']
        tuple = (sp.track(track['id'])['album']['artists'][0]['name'], sp.track(track['id'])['name'])
        songs.append(tuple)
    return songs

def spotify_track(result, sp):
    '''RETURNS THE NAME OF A ARTIST AND SONGNAME'''
    return (sp.track(result['id'])['album']['artists'][0]['name'], sp.track(result['id'])['name'])




def spotify(source):
    '''RETURNS LIST OF SONGNAMES AND ARTISTS FROM A SPOTIFY LINK'''
    cid = ''    #you get this from your spotify developer account
    secret = "" #you get this from your spotify developer account
    client_credentials_manager = SpotifyClientCredentials(client_id = cid, client_secret = secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    if "playlist" in source:
        playlist_id = source
        results = sp.playlist(playlist_id)
        songs = spotify_playlist(results, sp)
        random.shuffle(songs)

        return songs

# Define a regular expression pattern to match the desired substring
    elif "track" in source:
        songs = []
        pattern = r"/track/(.*?)(\?|$)"

# Use re.search() to find the matching substring
        match = re.search(pattern, source)

# Check if a match was found
        if match:
            # Extract the matched substring
            extracted_substring= match.group(1)
            result = sp.track(extracted_substring)
            songs.append(spotify_track(result, sp))
            return songs
        else:
            print("No match found.")

    return songs
