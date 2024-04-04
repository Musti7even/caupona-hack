import streamlit as st

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
def main():
    # Title of the app
    st.title("Upload Lecture Materials")
    st.sidebar.success("Select a demo above.")
    
    with st.sidebar:
        add_logo()
    # File uploader allows user to add any type of file
    # Set accept_multiple_files to True to allow multiple file uploads
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "docx", "txt", "mp4"], accept_multiple_files=True)

    # Example of how to handle the uploaded files
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            # You can use the files here (e.g., save them or process them)
            st.write("Filename:", uploaded_file.name)
            # Add more processing here as needed

if __name__ == "__main__":
    main()


    
