import streamlit as st

def main():
    # Title of the app
    st.title("Upload Lecture Materials")

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
