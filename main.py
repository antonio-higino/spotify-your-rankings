import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import os

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

artists_short = sp.current_user_top_artists(limit=20, time_range="short_term")
artists_short_names = [artist["name"] for artist in artists_short["items"]]

artists_medium = sp.current_user_top_artists(limit=20, time_range="medium_term")
artists_medium_names = [artist["name"] for artist in artists_medium["items"]]

artists_long = sp.current_user_top_artists(limit=20, time_range="long_term")
artists_long_names = [artist["name"] for artist in artists_long["items"]]

tracks_short = sp.current_user_top_tracks(limit=20, time_range="short_term")
tracks_short_names = [track["name"] for track in tracks_short["items"]]

tracks_medium = sp.current_user_top_tracks(limit=20, time_range="medium_term")
tracks_medium_names = [track["name"] for track in tracks_medium["items"]]

tracks_long = sp.current_user_top_tracks(limit=20, time_range="long_term")
tracks_long_names = [track["name"] for track in tracks_long["items"]]

st.set_page_config(page_title="Your Spotify Rankings", page_icon=":medal:", layout="wide")
st.title("View your artist and track rankings")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Curto prazo")
    st.write("Artistas:", artists_short_names, "Músicas:", tracks_short_names)

with col2:
    st.subheader("Médio prazo")
    st.write("Artistas:", artists_medium_names, "Músicas:", tracks_medium_names)

with col3:
    st.subheader("Longo prazo")
    st.write("Artistas:", artists_long_names, "Músicas:", tracks_long_names)