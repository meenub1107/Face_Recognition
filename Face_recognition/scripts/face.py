import cv2
import os
import face_recognition

class FacialFeaturesRecognizer:
    def __init__(self, known_faces_folder):
        self.known_face_encodings, self.known_face_names = self.load_known_faces(known_faces_folder)

    def load_known_faces(self, known_faces_folder):
        known_face_encodings = []
        known_face_names = []

        for filename in os.listdir(known_faces_folder):
            if filename.endswith((".jpg", ".png")):
                known_image = face_recognition.load_image_file(os.path.join(known_faces_folder, filename))
                face_encoding = face_recognition.face_encodings(known_image)[0]
                known_face_encodings.append(face_encoding)
                known_face_names.append(os.path.splitext(filename)[0])

        return known_face_encodings, known_face_names

    def recognize_person(self, frame):
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown" if not any(matches) else self.known_face_names[matches.index(True)]
            print(f"Detected person: {name}")

if __name__ == "__main__":
    known_faces_folder = r"C:\Users\meenu\OneDrive\Desktop\Face Recognition\images"
    recognizer = FacialFeaturesRecognizer(known_faces_folder)

    # Load a sample image
    test_image = face_recognition.load_image_file(r"C:\Users\meenu\OneDrive\Desktop\Face Recognition\images\Meenu.png")

    # Recognize persons in the image
    recognizer.recognize_person(test_image)
