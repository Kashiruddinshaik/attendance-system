import cv2
import numpy as np
import mysql.connector
import os

def run():
    # Create LBPH Face Recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load Haarcascade for face detection
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Connect to MySQL Database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="face_recognition_db"
    )
    cursor = conn.cursor()

    # Fetch faces from MySQL
    cursor.execute("SELECT id, name, image FROM faces")
    faces_data = cursor.fetchall()

    # Initialize dataset
    face_samples = []
    ids = []
    name_mapping = {}

    if not faces_data:
        print("❌ No faces found in database. Training aborted.")
        return  # Use return instead of exit() to prevent crashing Flask

    for id, name, image_blob in faces_data:
        img_array = np.frombuffer(image_blob, np.uint8)
        img_decoded = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)

        faces = face_detector.detectMultiScale(img_decoded)
        for (x, y, w, h) in faces:
            face_samples.append(img_decoded[y:y+h, x:x+w])
            ids.append(id)
            name_mapping[id] = name  # Store ID-to-Name mapping

    # Train the recognizer
    recognizer.train(face_samples, np.array(ids))

    # Save trained model
    trainer_path = "trainer"
    if not os.path.exists(trainer_path):
        os.makedirs(trainer_path)
    recognizer.save(f"{trainer_path}/trainer.yml")

    conn.close()
    print(f"🎉 Training complete! Model saved at '{trainer_path}/trainer.yml'.")

# Ensure the script only runs when explicitly called
if __name__ == "__main__":
    run()
