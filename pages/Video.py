import streamlit as st
import os


def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://upload.wikimedia.org/wikipedia/commons/2/2a/Microsoft_365_Copilot_Icon.svg);
                background-repeat: no-repeat;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Student Companion";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

with st.sidebar:
    add_logo()
    
# Obtain the current working directory
current_path = os.getcwd()

# Proceed with your code to read and display the video file
video_file = open('data/lecture_6.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes, format="video/mp4", start_time=3)

st.write("🎥")
