import streamlit as st
from openai import AzureOpenAI
import os
import pandas as pd
import numpy as np
import random

import validators
from io import BytesIO
from gtts import gTTS, gTTSError
import requests

import streamlit as st
import streamlit_book as stb


if 'initialized' not in st.session_state:
    # Initialization code here
    st.session_state['is_video_active'] = False
    st.session_state['is_download_active'] = False
    st.session_state['is_quiz_active'] = False
    st.session_state['video_time'] = 0
    # Mark as initialized
    st.session_state['initialized'] = True
    st.session_state["quiz_options"] = {"28":True,
             "2":False,
             "- 5":False,
             "129":False}
    
    ##Video
    st.session_state['is_video'] = False
    st.session_state['timestamp'] = 0



## CODE TO DELETE


def convert_df():
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    df = pd.DataFrame({
    'A': np.random.randint(1, 10, 5),
    'B': np.random.rand(5),
    'C': np.random.choice(['X', 'Y', 'Z'], 5)
    })
    return df.to_csv().encode('utf-8')

csv = convert_df()


## ------------------------
quiz_correct = ""
quiz_wrong = []
shuffled_quiz_options = {"28":True,
             "2":False,
             "- 5":False,
             "129":False}

def extract_first_quiz_answers(response_json):
    print(response_json)
    global shuffled_quiz_options
    global is_quiz_active

    quiz1 = response_json["output"]["quiz_questions"]["quiz1"]
    for i in range(len(quiz1["options"])):
        if i == quiz1["correct_index"]:
            continue
        quiz_wrong.append(quiz1["options"][i])
        print(i)
        print(quiz1["options"][i])
    quiz_correct = quiz1["options"][quiz1["correct_index"]]

    quiz_options = {quiz_correct:True,
             quiz_wrong[0]:False,
             quiz_wrong[1]:False,
             quiz_wrong[2]:False}
    items = list(quiz_options.items())
    random.shuffle(items)
    shuffled_quiz_options = dict(items)
    st.session_state["quiz_options"]

    st.session_state['is_quiz_active'] = True






    

st.title("Chat with your AI-friend 🤖")


import time
def stream_data(message):
    for word in message.split(" "):
        yield word + " "
        time.sleep(0.02)
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

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
    
# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "QHackGPT3"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
        
# Display assistant response in chat message container
    with st.chat_message("assistant"):
        url = "https://caupona-backend.azurewebsites.net/chat"
        print(st.session_state.messages[-1]["content"])
        data = {
            "input": st.session_state.messages[-1]["content"],  # Replace these with actual key-value pairs you want to send
        }
        httpResponse = requests.post(url, json=data)
        print(httpResponse)
        json_data = httpResponse.json()
        type = json_data["output"]["return_type"]
        if type == "chat":
            response = st.write_stream(stream_data(json_data["output"]["text"]))
            st.session_state.messages.append({"role": "assistant", "content": response})
        if type == "quiz_questions":
            extract_first_quiz_answers(json_data)
        if type =="timestamp":
            # Proceed with your code to read and display the video file
            video_file = open('data/lecture_6.mp4', 'rb')
            video_bytes = video_file.read()

            st.session_state["is_video"] = True
            st.session_state["timestamp"] = json_data["output"]["timestamp"]







if st.session_state['is_download_active']:
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )

def show_audio_player(ai_content: str) -> None:
    sound_file = BytesIO()
    try:
        tts = gTTS(text=ai_content, lang="en")
        tts.write_to_fp(sound_file)
        st.write("")
        st.audio(sound_file)
    except gTTSError as err:
        st.error(err)


# show_audio_player("ai_content")
# import streamlit.components.v1 as components

# if is_video_active:
#     video_file = open('data/lecture_6.mp4', 'rb')
#     video_bytes = video_file.read()

#     st.video(video_bytes, format="video/mp4", start_time=video_time)

if st.session_state['is_quiz_active']:
    stb.multiple_choice("### Thats your question generated by GPT", st.session_state["quiz_options"])

if st.session_state['is_video']:
    st.video(video_bytes, format="video/mp4", start_time=st.session_state["timestamp"])


