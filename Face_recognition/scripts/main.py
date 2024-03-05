# main.py
import tkinter as tk
import streamlit as st
from camera import CameraHandler

def main():
    # Set Streamlit title
    st.title("Face Recognition App")

    # Create a button to start the camera
    start_camera_button = st.button("Start Camera")

    # Check if the button is clicked
    if start_camera_button:
        # Folder containing known face images
        known_faces_folder = r"C:\Users\meenu\OneDrive\Desktop\Face Recognition\images"

        # Create an instance of the CameraHandler
        camera_handler = CameraHandler(known_faces_folder)

        # Create a tkinter window
        root = tk.Tk()
        root.title("Camera App")

        # Create a label to display the camera feed
        camera_label = tk.Label(root)
        camera_label.pack()

        # Start capturing video
        camera_handler.capture_video(root, camera_label)

        # Start the tkinter main loop
        root.mainloop()

if __name__ == "__main__":
    main()