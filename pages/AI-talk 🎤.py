from streamlit_mic_recorder import speech_to_text
import streamlit as st
from openai import OpenAI
import requests
import base64
import os

AZURE_OPENAI_ENDPOINT = "https://Qtts.api.cognitive.microsoft.com"
AZURE_OPENAI_API_KEY = "6361c848fc8b42459948acdbf1e7cbaa"


st.title("Talk with your AI-friend 🤖")
# Initialize the placeholder for the audio component at a suitable location in your app
audio_placeholder = st.empty()

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()

    title = ""
    md = f"""
        <div>
            <p style='text-align:center; font-weight:bold;'>{title}</p>
            <audio controls autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        </div>
        """
    # Update the placeholder with the new markdown
    audio_placeholder.markdown(md, unsafe_allow_html=True)

    # Attempt to delete the file after loading it to the placeholder
    try:
        os.remove(file_path)
    except Exception as e:
        st.error(f"Failed to delete the audio file. Error: {str(e)}")



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
# Initialize i in Streamlit's session state if it doesn't exist
if 'i' not in st.session_state:
    st.session_state.i = 0

def callback():
    if st.session_state.my_stt_output:
        text = st.session_state.my_stt_output
        
        # Initializing the OpenAI client with your API key
        client = OpenAI(api_key="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")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )

        gptResponseText = response.choices[0].message.content

        # Preparing the request for the TTS API
        url = f"https://openai-mannheimdemo.openai.azure.com/openai/deployments/Qtts/audio/speech?api-version=2024-02-15-preview"
        headers = {
            "api-key": "6361c848fc8b42459948acdbf1e7cbaa",
            "Content-Type": "application/json",
        }
        data = {
            "model": "tts-1",
            "input": gptResponseText,
            "voice": "alloy"
        }

        # Sending the request
        response = requests.post(url, headers=headers, json=data)

        # Handling the response
        if response.status_code == 200:
            filename = "speech" + str(st.session_state.i) + ".mp3"
            with open(filename, "wb") as f:
                f.write(response.content)
            autoplay_audio(filename)  # This function will replace the old audio with the new one
            st.session_state.i += 1  # Incrementing for the next file name
        else:
            st.error(f"Failed to generate speech. Status code: {response.status_code}, Message: {response.text}")

        # Resetting the state for the next input
        st.session_state.my_stt_output = None



# Integrating the speech_to_text function with the Streamlit UI
speech_to_text(key='my_stt', callback=callback)