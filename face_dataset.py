import cv2
import mysql.connector
import numpy as np

def run(name="Unknown"):
    # Load Haarcascade for face detection
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    print(f"✅ Capturing face for: {name}")

    # Connect to MySQL Database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="face_recognition_db"
    )
    cursor = conn.cursor()

    # Start capturing faces
    print(f"📸 Capturing images for {name}... Press 'q' to quit.")
    vid_cam = cv2.VideoCapture(0)

    if not vid_cam.isOpened():
        print("❌ Error: Cannot access webcam")
        return  # Use return instead of exit() to prevent crashing Flask

    count = 0
    while True:
        ret, image_frame = vid_cam.read()
        if not ret:
            print("❌ Error: Cannot access webcam")
            break

        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            _, img_encoded = cv2.imencode(".jpg", gray[y:y+h, x:x+w])
            img_blob = img_encoded.tobytes()

            cursor.execute("INSERT INTO faces (name, image) VALUES (%s, %s)", (name, img_blob))
            conn.commit()
            print(f"✅ Saved face {count} for {name}")

        cv2.imshow("Face Capture", image_frame)

        if count >= 100 or (cv2.waitKey(10) & 0xFF == ord('q')):
            break

    vid_cam.release()
    cv2.destroyAllWindows()
    conn.close()
    print(f"✅ Face dataset collection complete for {name} (Stored in MySQL).")

# Ensure the script only runs when explicitly called
if __name__ == "__main__":
    run()
