import streamlit as st
import os

# Obtain the current working directory
current_path = os.getcwd()

# Proceed with your code to read and display the video file
video_file = open('data/lecture_6.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes, format="video/mp4", start_time=3)
