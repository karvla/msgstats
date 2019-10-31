import regex as re
import pickle
from datetime import timedelta, datetime, date
import indexing
import matplotlib.pyplot as plt
from setup import path_cache, path_home
import os
import argparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import sys

with open(path_cache, 'rb') as f:
    _, _, _, pts, _, _ = pickle.load(f)

def spotify_urls(name):
    url_ts = []
    for seq in [pts[name]["to"], pts[name]["from"]]:
        for msg in seq:
            urls = re.findall('http\S+spotify.com\/track\S+', msg["content"])
            if not urls:
                continue
            ts = msg["timestamp"]

            [url_ts.append((url, ts)) for url in urls]
    return list(map(lambda x: x[0], sorted(url_ts, key=lambda x: int(x[1]))))

def add_to_playlist(name):
    scope = "playlist-modify-private playlist-modify-private user-library-modify user-read-private"
    token = util.prompt_for_user_token("Arvid Larsson", scope)
    sp = spotipy.Spotify(auth=token)

    username = sp.user(user_id)["display_name"]
    sp.user_playlist_create(user_id, name.split()[0], False)
    playlists = sp.user_playlists(user_id)
    playlist_id = playlists["items"][0]["id"]

    urls = spotify_urls(name)
    ids = list(map(lambda x: sp.track(x)["id"], urls))
    sp.user_playlist_add_tracks(username, playlist_id, ids)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Creates a Spotify playlist from all the Spotify songs shared via Facebook Messenger for a given person."
    )

    parser.add_argument(
        "user_id",
        type=str,
        nargs=1,
        help="The spotify user id. A long string of digits. Can be found by in the url when a profile is shared: open.spotify.com/user/USERID",
    )

    parser.add_argument(
        "friend_name",
        type=str,
        nargs="+",
        help="The name of a person.",
    )

    args = parser.parse_args()
    friend_name = " ".join(args.friend_name)
    user_id = args.user_id[0]
    add_to_playlist(friend_name)
    print("Playlist was created successfully!")









