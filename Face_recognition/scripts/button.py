import streamlit as st
from button import start_camera

def main():
    st.title("Face Recognition App")

    # Folder containing known face images
    known_faces_folder = r"C:\Users\meenu\OneDrive\Desktop\Face Recognition\images"

    # Button to start the camera
    st.button("Start Camera")

if __name__ == "__main__":
    main()
