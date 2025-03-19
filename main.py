import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os

CLIENT_ID = "b5aed56aa7634bd2b9a942f8b6d5be41"
CLIENT_SECRET = "c66a5d6fdec44cdaaf36a55036365140"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="https://example.com/callback/",
        scope="user-top-read, user-read-recently-played"
    )
)

def calculateDeltas(list1, list2):
    for item1 in list1:
        for item2 in list2:
            if item1["name"] == item2["name"]:
                item1["delta"] = str(item2["rank"] - item1["rank"])
                if int(item1["delta"]) > 0:
                    item1["delta"] = "+" + item1["delta"]

def setBackgroundColor(item):
    if item != "NEW!" and int(item) < 0:
        return f"background-color: {'#600000'}"
    elif item != "NEW!" and int(item) != 0:
        return f"background-color: {'#006024'}"

artists_long = sp.current_user_top_artists(limit=50, time_range="long_term")
artists_long_list = []
for i, artist in enumerate(artists_long["items"]):
    artists_long_list.append({"rank" : i+1, "delta" : "NEW!", "name" : artist["name"], "url" : artist["external_urls"]["spotify"] + "#" + artist["name"]})

artists_medium = sp.current_user_top_artists(limit=50, time_range="medium_term")
artists_medium_list = []
for i, artist in enumerate(artists_medium["items"]):
    artists_medium_list.append({"rank" : i+1, "delta" : "NEW!", "name" : artist["name"], "url" : artist["external_urls"]["spotify"] + "#" + artist["name"]})
calculateDeltas(artists_medium_list, artists_long_list)

artists_short = sp.current_user_top_artists(limit=50, time_range="short_term")
artists_short_list = []
for i, artist in enumerate(artists_short["items"]):
    artists_short_list.append({"rank" : i+1, "delta" : "NEW!", "name" : artist["name"], "url" : artist["external_urls"]["spotify"] + "#" + artist["name"]})
calculateDeltas(artists_short_list, artists_medium_list)

tracks_long = sp.current_user_top_tracks(limit=50, time_range="long_term")
tracks_long_list = []
for i, track in enumerate(tracks_long["items"]):
    tracks_long_list.append({"rank" : i+1, "delta" : "NEW!", "name" : track["name"], "url" : track["external_urls"]["spotify"] + "#" + track["name"]})

tracks_medium = sp.current_user_top_tracks(limit=50, time_range="medium_term")
tracks_medium_list = []
for i, track in enumerate(tracks_medium["items"]):
    tracks_medium_list.append({"rank" : i+1, "delta" : "NEW!", "name" : track["name"], "url" : track["external_urls"]["spotify"] + "#" + track["name"]})
calculateDeltas(tracks_medium_list, tracks_long_list)

tracks_short = sp.current_user_top_tracks(limit=50, time_range="short_term")
tracks_short_list = []
for i, track in enumerate(tracks_short["items"]):
    tracks_short_list.append({"rank" : i+1, "delta" : "NEW!", "name" : track["name"], "url" : track["external_urls"]["spotify"] + "#" + track["name"]})
calculateDeltas(tracks_short_list, tracks_medium_list)

df_art_lon = pd.DataFrame(artists_long_list)
df_art_med = pd.DataFrame(artists_medium_list)
df_art_sho = pd.DataFrame(artists_short_list)

df_tra_lon = pd.DataFrame(tracks_long_list)
df_tra_med = pd.DataFrame(tracks_medium_list)
df_tra_sho = pd.DataFrame(tracks_short_list)

st.set_page_config(page_title="Your Spotify Rankings", page_icon=":medal:", layout="wide")
st.title("View your artist and track rankings")

tab_art, tab_tra = st.tabs(["Artists", "Tracks"])
with tab_art:
    col_art_lon, col_art_med, col_art_sho = st.columns(3)
    with col_art_lon:
        st.subheader("Long term")
        st.dataframe(
            df_art_lon,
            column_config={
                "rank": "Rank",
                "delta": "Variation",
                "url": st.column_config.LinkColumn("Artist", display_text=r"#(.*)", width="large"),
            },
            column_order=["rank", "url", "delta"],
            hide_index=True,
            use_container_width=False,
            height=(35*len(df_art_lon)+38)
        )
    with col_art_med:
        st.subheader("Medium term")
        st.dataframe(
            df_art_med.style.map(setBackgroundColor, subset=["delta"]),
            column_config={
                "rank": "Rank",
                "delta": "Variation",
                "url": st.column_config.LinkColumn("Artist", display_text=r"#(.*)", width="large"),
            },
            column_order=["rank", "url", "delta"],
            hide_index=True,
            use_container_width=False,
            height=(35*len(df_art_med)+38)
        )
    with col_art_sho:
        st.subheader("Short term")
        st.dataframe(
            df_art_sho.style.map(setBackgroundColor, subset=["delta"]),
            column_config={
                "rank": "Rank",
                "delta": "Variation",
                "url": st.column_config.LinkColumn("Artist", display_text=r"#(.*)", width="large"),
            },
            column_order=["rank", "url", "delta"],
            hide_index=True,
            use_container_width=False,
            height=(35*len(df_art_sho)+38)
        )

with tab_tra:
    col_tra_lon, col_tra_med, col_tra_sho = st.columns(3)
    with col_tra_lon:
        st.subheader("Long term")
        st.dataframe(
            df_tra_lon,
            column_config={
                "rank": "Rank",
                "delta": "Variation",
                "url": st.column_config.LinkColumn("Track", display_text=r"#(.*)", width="large"),
            },
            column_order=["rank", "url", "delta"],
            hide_index=True,
            use_container_width=False,
            height=(35*len(df_tra_lon)+38)
        )
    with col_tra_med:
        st.subheader("Medium term")
        st.dataframe(
            df_tra_med.style.map(setBackgroundColor, subset=["delta"]),
            column_config={
                "rank": "Rank",
                "delta": "Variation",
                "url": st.column_config.LinkColumn("Track", display_text=r"#(.*)", width="large"),
            },
            column_order=["rank", "url", "delta"],
            hide_index=True,
            use_container_width=False,
            height=(35*len(df_tra_med)+38)
        )
    with col_tra_sho:
        st.subheader("Short term")
        st.dataframe(
            df_tra_sho.style.map(setBackgroundColor, subset=["delta"]),
            column_config={
                "rank": "Rank",
                "delta": "Variation",
                "url": st.column_config.LinkColumn("Track", display_text=r"#(.*)", width="large"),
            },
            column_order=["rank", "url", "delta"],
            hide_index=True,
            use_container_width=False,
            height=(35*len(df_tra_sho)+38)
        )