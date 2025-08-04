import spotipy
import spotify.oauth2 as SpotifyOAuth
import streamlit as st
import polars as pl
import os

CLIENT_ID = os.getenv.get("CLIENT_ID")
CLIENT_SECRET = os.getenv.get("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                     client_id = CLIENT_ID, 
                     client_secret = CLIENT_SECRET, 
                     redirect_uri = REDIRECT_URI,
                     scope = "user-top-read")
                     )

st.set_page_config(page_title="Spotify Data Pipeline", page_icon=":musical_note:")