import cv2
import numpy as np
import mysql.connector
import datetime
import pandas as pd
import os

EXCEL_FILE = "C:/Final/attendance/new_attendance.xlsx"  # Ensure the correct path

def get_student_names():
    """Fetch student ID-to-Name mapping from MySQL."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="face_recognition_db"
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM faces")  # Fetch stored names from MySQL
    name_mapping = {str(row[0]): row[1] for row in cursor.fetchall()}  # Convert to dictionary
    conn.close()
    return name_mapping

def run():
    """Recognize students and mark attendance in MySQL and Excel."""
    name_mapping = get_student_names()  # Fetch registered names
    
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="face_recognition_db"
    )
    cursor = conn.cursor()

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer/trainer.yml")

    vid_cam = cv2.VideoCapture(0)
    print("🟢 Attendance tracking started. Press 'q' to exit.")

    today_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Format: 2025-03-19
    recorded_students = set()  # Store students already marked today

    while True:
        ret, image_frame = vid_cam.read()
        if not ret:
            print("❌ Error: Cannot access webcam")
            break

        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            student_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            student_id = str(student_id)

            if student_id in name_mapping:
                student_name = name_mapping[student_id]
            else:
                student_name = "Unknown"

            timestamp = datetime.datetime.now().strftime('%H:%M')  # Time format: 08:30

            if student_name != "Unknown" and student_name not in recorded_students:
                # Check if attendance already exists for today
                cursor.execute("SELECT * FROM attendance WHERE name = %s AND date = %s", (student_name, today_date))
                existing_record = cursor.fetchone()

                if not existing_record:
                    # Insert attendance only if not already marked today
                    cursor.execute("INSERT INTO attendance (name, date, timestamp) VALUES (%s, %s, %s)", 
                                   (student_name, today_date, timestamp))
                    conn.commit()
                    
                    append_to_excel(student_name, today_date, timestamp)
                    recorded_students.add(student_name)  # Avoid duplicate entry for today
                    
                    print(f"✅ Attendance recorded: {student_name} at {timestamp}")

            # Display on screen
            cv2.rectangle(image_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image_frame, student_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Face Recognition - Attendance", image_frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    vid_cam.release()
    cv2.destroyAllWindows()
    conn.close()
    print("🔴 Attendance tracking stopped.")


def append_to_excel(student_name, date, timestamp):
    """Automatically create Excel structure and log attendance per day."""
    
    if not os.path.exists(EXCEL_FILE):
        # Create a new DataFrame with Students and today's date
        df = pd.DataFrame(columns=["Students", date])
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
        print("✅ Created new attendance file.")

    # Load existing Excel file
    df = pd.read_excel(EXCEL_FILE, engine='openpyxl')

    # **Fix: Ensure "Students" column exists**
    if "Students" not in df.columns:
        df.insert(0, "Students", "")  # Insert "Students" column if missing

    # Ensure the date column exists
    if date not in df.columns:
        df[date] = ""  # Add new date column if missing

    # Check if student is already in the "Students" column
    if student_name in df["Students"].values:
        index = df.index[df["Students"] == student_name].tolist()[0]  # Find student's row
        if pd.isna(df.at[index, date]) or df.at[index, date] == "":
            df.at[index, date] = f"✅ {timestamp}"  # Mark attendance only once
    else:
        # Add new student entry
        new_entry = pd.DataFrame({"Students": [student_name], date: [f"✅ {timestamp}"]})
        df = pd.concat([df, new_entry], ignore_index=True)  # Use concat instead of append

    # Save updated Excel file
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
    print(f"✅ Attendance added in Excel for {student_name} on {date}.")



if __name__ == "__main__":
    run()
