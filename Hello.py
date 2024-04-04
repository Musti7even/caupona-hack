import streamlit as st

st.set_page_config(
    page_title="Caupona Copilot",
    page_icon="🤖",

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

st.write("# Welcome to Student Companion!")
st.write("## Our app is a one-stop solution for students to learn, practice and revise concepts. 🚀")

st.write("Presented by Team Caupona (2) for QHack 2024 🚀")
st.sidebar.success("Select a demo above.")


with st.sidebar:
    add_logo()
    