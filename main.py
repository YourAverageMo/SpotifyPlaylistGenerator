import json
import os

import requests
import spotipy
from bs4 import BeautifulSoup
from dotenv import find_dotenv, load_dotenv
from spotipy.oauth2 import SpotifyOAuth

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
BASE_URL = "https://www.billboard.com/charts/hot-100/"
SCOPE = "playlist-modify-private"

# --------------- SCRAP BILLBOARD TOP 100 ---------------


def scrap():
    """scraps above URL and ->

    Returns:
        print(): web scrap data saved into local dir 
    """
    response = requests.get(BASE_URL + date)
    webpage = response.text

    with open("./scrap_dump.text", mode="w") as f:
        f.write(webpage)
    return print(f"\n scrapped and saved")


# --------------- CREATE TOP 100 SONGS LIST ---------------
def gen_top_100_songs_list():
    with open("./scrap_dump.text", mode="r") as f:
        soup = BeautifulSoup(f, "html.parser")

    songs_raw = soup.findAll(name="li", class_="o-chart-results-list__item")

    songs = []
    for song in songs_raw:
        new_song = song.find(name="h3", id="title-of-a-story")
        if new_song == None:
            pass
        else:
            songs.append(new_song.getText().strip())
    with open("./top_100_songs.json", mode="w") as f:
        json.dump(songs, f)


# --------------- CREATE SONG URI'S LIST ---------------
def get_song_uri():
    with open("top_100_songs.json", mode="r") as f:
        songs = json.load(f)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope=SCOPE,
                                                   show_dialog=True,
                                                   cache_path="token.txt"))

    user_id = sp.current_user()
    songs_uri = []
    for song in songs:
        try:
            search = sp.search(q=song, type="track", limit=1, market="us")
        except IndexError:
            pass
        else:
            songs_uri.append(search["tracks"]["items"][0]["uri"])
    with open("./songs_uri.json", mode="w") as f:
        json.dump(songs_uri, f)


# --------------- GEN PLAYLIST FROM URI LIST ---------------
def gen_playlist():
    with open("./songs_uri.json", mode="r") as f:
        songs_uri = json.load(f)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope=SCOPE,
                                                   show_dialog=True,
                                                   cache_path="token.txt"))

    user_id = sp.current_user()["id"]
    playlist_id = sp.user_playlist_create(user=user_id,
                                          name=f"{date} Billboard 100",
                                          public=False)
    sp.user_playlist_add_tracks(user=user_id,
                                playlist_id=playlist_id["id"],
                                tracks=songs_uri)



# --------------- ENTER FUNCS U WANT TO USE BELOW ---------------
# currently this program doesnt do anything. i isolated the functions while programing them so i can write them up individually. also wrote some of the data to files then opened them back up when necessary to avoid scrapping websites constantly while im testing the code.

# you can use whichever functions you want to do whatever you want the names are pretty self-explanatory. but the proper order to start from scratch is:
# scrap() -> gen_top_100_songs_list() -> get_song_uri() -> gen_playlist()

date = input("What year you would like to travel to in YYYY-MM-DD format?\n"
             )  #date is only used during initial scrap and generating playlist

# scrap()
# gen_top_100_songs_list()
# get_song_uri()
# gen_playlist()