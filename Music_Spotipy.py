import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import random

def spotify_playlist(results, sp):
    songs = []
    for item in results['tracks']['items']:
        track = item['track']
        tuple = (sp.track(track['id'])['album']['artists'][0]['name'], sp.track(track['id'])['name'])
        songs.append(tuple)
    return songs

def spotify_track(result, sp):
    return (sp.track(result['id'])['album']['artists'][0]['name'], sp.track(result['id'])['name'])




def spotify(source):
    cid = 'bc030da8d3114800aa1e2204f8c19086'
    secret = "34c39960b17d466c9b86300a0062dc79"
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