import streamlit as st
import os

print(os.getcwd())
print("\n")
video_file = open('/data/vid.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes, format="video/mp4", start_time=3)
