import configparser
from spotipy import SpotifyOAuth
from spotipy import Spotify
from spotipy import SpotifyPKCE

config = configparser.ConfigParser()
config.read('settings.ini')

scope = "user-read-recently-played"

DB_CONNSTR = config['SPOTIFY']['DB_CONNSTR']


def data():
    # manager = SpotifyOAuth(client_id=config['SPOTIFY']['CLIENT_ID'],
    #                        client_secret=config['SPOTIFY']['CLIENT_SECRET'],
    #                        redirect_uri=config['SPOTIFY']['SPOTIPY_REDIRECT_URI'],
    #                        scope=scope)

    # sp = Spotify(auth_manager=manager)

    sp2 = Spotify(auth_manager=SpotifyPKCE(client_id=config['SPOTIFY']['CLIENT_ID'],
                                           redirect_uri=config['SPOTIFY']['SPOTIPY_REDIRECT_URI'],
                                           scope=scope, open_browser=False))
    return sp2

# print(data().current_user_recently_played(limit=4, after=1))
