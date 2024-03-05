import tkinter as tk
from tkinter import ttk, filedialog
import cv2
from PIL import Image, ImageTk
import os
import face_recognition

def main():
    def start_camera():
        cap = cv2.VideoCapture(0)

        def capture_frame():
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("captured_image.jpg", frame)
                label_status.config(text="Image captured successfully!")
                button_save.config(state="normal")
            else:
                label_status.config(text="Failed to capture image.")

        def save_image():
            src_path = "captured_image.jpg"
            dest_path = filedialog.asksaveasfilename(initialdir="/", title="Save Image As", filetypes=(("JPEG files", "*.jpg"), ("all files", "*.*")))
            if dest_path:
                os.rename(src_path, dest_path)
                label_status.config(text=f"Image saved successfully at {dest_path}")
            else:
                label_status.config(text="Image save canceled.")

        def recognize_face():
            known_image_path = filedialog.askopenfilename(title="Select Known Image", filetypes=(("JPEG files", "*.jpg"), ("all files", "*.*")))
            if known_image_path:
                known_image = face_recognition.load_image_file(known_image_path)
                known_encodings = face_recognition.face_encodings(known_image)
                known_names = [os.path.splitext(os.path.basename(known_image_path))[0] for _ in known_encodings]

                if not known_encodings:
                    label_status.config(text="No faces found in the known image.")
                    return

                captured_image_path = "captured_image.jpg"
                captured_image = face_recognition.load_image_file(captured_image_path)
                captured_encodings = face_recognition.face_encodings(captured_image)

                if not captured_encodings:
                    label_status.config(text="No faces found in the captured image.")
                    return

                captured_encoding = captured_encodings[0]

                # Compare the captured image with the known image
                matches = face_recognition.compare_faces(known_encodings, captured_encoding)

                if any(matches):
                    first_match_index = matches.index(True)
                    recognized_name = known_names[first_match_index]
                    label_status.config(text=f"Face recognized as {recognized_name}!")
                else:
                    label_status.config(text="Face not recognized.")

        root = tk.Tk()
        root.title("Camera Feed")

        frame = tk.Frame(root)
        frame.pack()

        label_status = ttk.Label(frame, text="")
        label_status.pack()

        button_capture = ttk.Button(frame, text="Capture", command=capture_frame)
        button_capture.pack()

        button_save = ttk.Button(frame, text="Save Image", command=save_image, state="disabled")
        button_save.pack()

        button_recognize = ttk.Button(frame, text="Recognize Face", command=recognize_face)
        button_recognize.pack()

        label_camera = tk.Label(frame)
        label_camera.pack()

        def update_frame():
            nonlocal label_camera
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                label_camera.imgtk = imgtk
                label_camera.configure(image=imgtk)
                label_camera.after(10, update_frame)  # Update every 10 milliseconds

        update_frame()

        root.mainloop()
        cap.release()

    start_camera()

if __name__ == "__main__":
    main()