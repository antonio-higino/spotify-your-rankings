import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import os
from dataclasses import dataclass

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-top-read, user-read-recently-played"
    )
)

@dataclass
class ArtistOrTrack:
    rank: int
    delta: int | None
    name: str
    url: str

artists_long = sp.current_user_top_artists(limit=20, time_range="long_term")
artists_long_list = []
for i, artist in enumerate(artists_long["items"]):
    artists_long_list.append(ArtistOrTrack(i+1, None, artist["name"], artist["external_urls"]["spotify"]))

artists_medium = sp.current_user_top_artists(limit=20, time_range="medium_term")
artists_medium_list = []
for i, artist in enumerate(artists_medium["items"]):
    artists_medium_list.append(ArtistOrTrack(i+1, None, artist["name"], artist["external_urls"]["spotify"]))
for art_med in artists_medium_list:
    for art_lon in artists_long_list:
        if art_med.name == art_lon.name:
            art_med.delta = art_lon.rank - art_med.rank

artists_short = sp.current_user_top_artists(limit=20, time_range="short_term")
artists_short_list = []
for i, artist in enumerate(artists_short["items"]):
    artists_short_list.append(ArtistOrTrack(i+1, None, artist["name"], artist["external_urls"]["spotify"]))
for art_sho in artists_short_list:
    for art_med in artists_medium_list:
        if art_sho.name == art_med.name:
            art_sho.delta = art_med.rank - art_sho.rank

tracks_long = sp.current_user_top_tracks(limit=20, time_range="long_term")
tracks_long_list = []
for i, track in enumerate(tracks_long["items"]):
    tracks_long_list.append(ArtistOrTrack(i+1, None, track["name"], track["external_urls"]["spotify"]))

tracks_medium = sp.current_user_top_tracks(limit=20, time_range="medium_term")
tracks_medium_list = []
for i, track in enumerate(tracks_medium["items"]):
    tracks_medium_list.append(ArtistOrTrack(i+1, None, track["name"], track["external_urls"]["spotify"]))
for tra_med in tracks_medium_list:
    for tra_lon in tracks_long_list:
        if tra_med.name == tra_lon.name:
            tra_med.delta = tra_lon.rank - tra_med.rank

tracks_short = sp.current_user_top_tracks(limit=20, time_range="short_term")
tracks_short_list = []
for i, track in enumerate(tracks_short["items"]):
    tracks_short_list.append(ArtistOrTrack(i+1, None, track["name"], track["external_urls"]["spotify"]))
for tra_sho in tracks_short_list:
    for tra_med in tracks_medium_list:
        if tra_sho.name == tra_med.name:
            tra_sho.delta = tra_med.rank - tra_sho.rank

# for item in artists_medium_list:
#     print(item.name, item.rank, item.delta)

artists_long_string = ""
for item in artists_long_list:
    artists_long_string += "Rank: " + str(item.rank) + " " + item.name + " Delta: " + str(item.delta)

print(artists_long_string)

st.set_page_config(page_title="Your Spotify Rankings", page_icon=":medal:", layout="wide")
st.title("View your artist and track rankings")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Longo prazo")
    st.write("Artistas:")
    st.write(artists_long_string)
    st.write("Músicas:")
    st.write_stream(tracks_long_list)

with col2:
    st.subheader("Médio prazo")
    st.write("Artistas:", artists_medium_list, "Músicas:", tracks_medium_list)

with col3:
    st.subheader("Curto prazo")
    st.write("Artistas:", artists_short_list, "Músicas:", tracks_short_list)