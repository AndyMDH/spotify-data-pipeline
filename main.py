import spotipy
from spotipy.oauth2 import SpotifyOAuth  
import streamlit as st
import polars as pl
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:3000"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                     client_id = CLIENT_ID, 
                     client_secret = CLIENT_SECRET, 
                     redirect_uri = REDIRECT_URI,
                     scope = "user-top-read user-read-private")
                     )

st.set_page_config(page_title="Spotify Data Pipeline", page_icon=":musical_note:")
st.title("Andy's Top Spotify Songs")
st.write("Explore your Spotify data.")

top_tracks = sp.current_user_top_tracks(limit=15, time_range="short_term")
track_ids = [track["id"] for track in top_tracks["items"]]

try:
    audio_feature = sp.audio_features(track_ids)
    
    df = pl.DataFrame(audio_feature)
    df["track_name"] = [track["name"] for track in top_tracks["items"]]
    df = df["track_name", "acousticness", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "tempo", "valence"]
    df.set_index("track_name",inplace=True)

    st.subheader("Audio Features for Top 15 Tracks")
    st.bar_chart(df, height = 500)
    
except Exception as e:
    st.error(f"Error getting audio features: {str(e)}")
    st.write("This might be a permissions issue. Try re-authorizing the app.")
    st.write("If the problem persists, check your Spotify app settings.")