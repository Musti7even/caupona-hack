import streamlit as st
from openai import AzureOpenAI
import os
import pandas as pd
import numpy as np

from streamlit_extras.app_logo import add_logo 
import validators
from io import BytesIO
from gtts import gTTS, gTTSError


## CODE TO DELETE
add_logo("http://placekitten.com/120/120")


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

st.title("COPILOT")


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
print(7)
print(os.getenv("AZURE_OPENAI_ENDPOINT"))
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
        # TODO send HTTP request here
        stream = "Hey ich bin Mustafa \n\n\nHier ist viel Chat\n\n\nHey ich bin Mustafa \n\n\nHier ist viel Chat\n\n\nHey ich bin Mustafa \n\n\nHier ist viel Chat\n\n\n"
        response = st.write_stream(stream_data(stream))
    st.session_state.messages.append({"role": "assistant", "content": response})


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


show_audio_player("ai_content")
import streamlit.components.v1 as components
