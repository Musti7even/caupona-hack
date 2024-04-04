import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd
import requests

# -------------- app config ---------------

st.set_page_config(page_title="Flashcards", page_icon="🚀")

# ---------------- functions ----------------

# external css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# callbacks
def callback():
    st.session_state.button_clicked = True

response = requests.get("https://caupona-backend.azurewebsites.net/get_flashcard_topics")

if response.status_code == 200:
    response = response.json()
    fachs = response["topics"]
    
else:
    fachs=[]

rows=[]
def callback2():
    st.session_state.button2_clicked = True
fach=""

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
    if len(fachs)>0:

        fach = st.selectbox("Choose a subject", options=fachs)
        st.write("**Streamlit app created by:**")
        st.write("CAUPONA team for QHack 2023")

    
    
# ---------------- CSS ----------------

local_css("style.css")

# ---------------- SESSION STATE ----------------

if "button_clicked" not in st.session_state:
    st.session_state["button_clicked"] = False

if "button2_clicked" not in st.session_state:
    st.session_state["button2_clicked"] = False

if "q_no" not in st.session_state:
    st.session_state["q_no"] = 0

if "q_no_temp" not in st.session_state:
    st.session_state.q_no_temp = 0

# ---------------- Main page ----------------

for fach in fachs:
    data = {
        "topic": "Bayesian Optimization",  # Replace these with actual key-value pairs you want to send
    }

    response = requests.post("https://caupona-backend.azurewebsites.net/get_flashcards_for_topic", json=data)


    if response.status_code == 200:
        response = response.json()
        rows = response["flashcards"]
    else:
        rows = []
    rows = pd.DataFrame(rows)

if len(rows) > 0:
    st.title(f"Flashcards {fach}")
    no = len(rows)
    st.caption("Currently we have " + str(no) + " questions in the database")

    # ---------------- questions & answers logic ----------------

    col1, col2 = st.columns(2)
    with col1:
        question = st.button(
            "Draw question", on_click=callback, key="Draw", use_container_width=True
        )
    with col2:
        answer = st.button(
            "Show answer", on_click=callback2, key="answer", use_container_width=True
        )

    if question or st.session_state["button_clicked"]:
        # randomly select question number
        new_id = random.randint(0, no - 1)
        while new_id == st.session_state.q_no:
            new_id = random.randint(0, no - 1)

        st.session_state["q_no"] = new_id

        # this 'if' checks if algorithm should use value from temp or new value (temp assigment in else)
        if st.session_state.button2_clicked:
            st.markdown(
                f'<div class="blockquote-wrapper"><div class="blockquote"><h1><span style="color:#37474F">{rows.iloc[st.session_state.q_no_temp].question}</span></h1><h4>&mdash; question no. {st.session_state.q_no_temp+1}</em></h4></div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="blockquote-wrapper"><div class="blockquote"><h1><span style="color:#37474F">{rows.iloc[st.session_state.q_no].question}</span></h1><h4>&mdash; question no. {st.session_state.q_no+1}</em></h4></div></div>',
                unsafe_allow_html=True,
            )
            # keep memory of question number in order to show answer
            st.session_state.q_no_temp = st.session_state.q_no

        if answer:
            st.markdown(
                f"<div class='answer'><span style='font-weight: bold; color:#6d7284;'>answer to question number {st.session_state.q_no_temp+1}</span><br><br>{rows.iloc[st.session_state.q_no_temp].answer}</div>",
                unsafe_allow_html=True,
            )
            st.session_state.button2_clicked = False

    # this part normally should be on top however st.markdown always adds divs even it is rendering non visible parts?

    st.markdown(
        '<div><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Barlow+Condensed&family=Cabin&display=swap" rel="stylesheet"></div>',
        unsafe_allow_html=True,
    )
else:
    st.title(f"Flashcards {fach}")
    st.write("📚 No cards available. Please ask in the Chat to create flashcards for a specific subject.")
