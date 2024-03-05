# camera.py
import cv2
import streamlit as st
import tkinter as tk
from PIL import Image, ImageTk
import face_recognition
import os

class CameraHandler:
    def __init__(self, known_faces_folder):
        self.cap = cv2.VideoCapture(0)
        self.camera_on = False

        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            exit()

        self.known_face_encodings, self.known_face_names = self.load_known_faces(known_faces_folder)

    def load_known_faces(self, known_faces_folder):
        known_face_encodings = []
        known_face_names = []

        for filename in os.listdir(known_faces_folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                # Load and encode the known face
                known_image = face_recognition.load_image_file(os.path.join(known_faces_folder, filename))
                face_encoding = face_recognition.face_encodings(known_image)[0]
                known_face_encodings.append(face_encoding)
                known_face_names.append(os.path.splitext(filename)[0])  # Extracting name from the file name

        return known_face_encodings, known_face_names

    def recognize_faces(self, frame):
        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Initialize variables for accuracy calculation
        total_faces = len(face_locations)
        correct_matches = 0

        # Loop through each face in the current frame
        for face_location, face_encoding in zip(face_locations, face_encodings):
            # Compare with known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match is found, use the name of the first matching known face
            if any(matches):
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
                correct_matches += 1

            # Draw a rectangle around the face
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Calculate accuracy rate
            accuracy_rate = (correct_matches / total_faces) * 100 if total_faces > 0 else 0

            # Add face name and accuracy rate above the rectangle
            font = cv2.FONT_HERSHEY_DUPLEX
            text = f"{name}, Accuracy: {accuracy_rate:.2f}%"
            cv2.putText(frame, text, (left + 6, top - 20), font, 0.6, (0, 255, 0), 1)

        return frame

    def update_camera_feed(self, label):
        if self.camera_on:
            ret, frame = self.cap.read()

            if ret:
                frame_with_faces = self.recognize_faces(frame)
                img = Image.fromarray(cv2.cvtColor(frame_with_faces, cv2.COLOR_BGR2RGB))
                img_tk = ImageTk.PhotoImage(image=img)

                label.img = img_tk
                label.config(image=img_tk)

            label.after(10, lambda: self.update_camera_feed(label))  # Schedule the next update

    def capture_video(self, root, label):
        self.camera_on = True
        self.update_camera_feed(label)

        # Check for 'q' key press to close the camera
        root.bind('<Key>', lambda event: self.on_key_press(event, root))

        root.protocol("WM_DELETE_WINDOW", self.turn_off_camera)  # Handle window close event

        root.mainloop()

        self.camera_on = False

        self.cap.release()
        cv2.destroyAllWindows()

    def on_key_press(self, event, root):
        if event.char.lower() == 'q':
            self.turn_off_camera(root)

    def turn_off_camera(self, root):
        self.camera_on = False
        root.destroy()

if __name__ == "__main__":
    # Folder containing known face images
    known_faces_folder = r"C:\Users\meenu\OneDrive\Desktop\Face Recognition\images"

    camera_handler = CameraHandler(known_faces_folder)

    # Create a tkinter window
    root = tk.Tk()
    root.title("Camera App")

    # Create a label to display the camera feed
    camera_label = tk.Label(root)
    camera_label.pack()

    # Start capturing video
    camera_handler.capture_video(root, camera_label)
