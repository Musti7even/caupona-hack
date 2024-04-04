from streamlit_mic_recorder import speech_to_text
import streamlit as st
from openai import OpenAI
import requests
import base64

AZURE_OPENAI_ENDPOINT = "https://Qtts.api.cognitive.microsoft.com"
AZURE_OPENAI_API_KEY = "6361c848fc8b42459948acdbf1e7cbaa"


st.title("Talk with your AI-friend 🤖")
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
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
    
def callback():
    if st.session_state.my_stt_output:
        # Here you can add the action you want to perform with the speech-to-text output
        text = st.session_state.my_stt_output
        print("User: " + text)
        client = OpenAI(
            api_key="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")
        gptRespnse = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}])

        print("GPT: " + gptRespnse.choices[0].message.content)
        gptResponseText = gptRespnse.choices[0].message.content


        url = f"https://openai-mannheimdemo.openai.azure.com/openai/deployments/Qtts/audio/speech?api-version=2024-02-15-preview"

        # The headers for the request
        headers = {
            "api-key": AZURE_OPENAI_API_KEY,
            "Content-Type": "application/json",
        }

        # The data to be sent with the request
        data = {
            "model": "tts-1",
            "input": gptResponseText,
            "voice": "alloy"
        }
        # Sending the POST request
        response = requests.post(url, headers=headers, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Saving the response content to an MP3 file
            with open("speech.mp3", "wb") as f:
                f.write(response.content)
            print("The speech was successfully saved as speech.mp3")
            autoplay_audio("speech.mp3")
        else:
            print(f"Failed to generate speech. Status code: {response.status_code}, Message: {response.text}")
                


# Here, the speech_to_text function is called and configured with a callback.
# The callback is triggered after the speech is converted to text.
speech_to_text(key='my_stt', callback=callback)
