from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import face_dataset
import trained_data
import face_recognization  # Ensure this file exists
import threading
import os

app = Flask(__name__)

current_script = None  # Track the running script
script_thread = None  # Store thread reference
camera = None  # Camera starts only when needed
lock = threading.Lock()  # Thread safety


def start_camera():
    """Start the camera when needed."""
    global camera
    if camera is None or not camera.isOpened():
        camera = cv2.VideoCapture(0)  # Open the camera
    return camera


def stop_camera():
    """Stop the camera when not in use."""
    global camera
    if camera is not None and camera.isOpened():
        camera.release()  # Release the camera
        camera = None  # Reset camera object


def generate_frames():
    """Stream video frames when the camera is active."""
    global camera
    camera = start_camera()  # Start camera only when needed
    while True:
        with lock:
            success, frame = camera.read()
            if not success:
                break
            else:
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index1.html')


@app.route('/video_feed')
def video_feed():
    """Stream live video to the webpage."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/task_completed')
def task_completed():
    """Show task completion message and return to homepage after 3 seconds."""
    return render_template('task_completed.html')


@app.route('/run_script', methods=['POST'])
def run_script():
    """Start a script and redirect back after completion."""
    global current_script, script_thread

    script_name = request.form['script']
    student_name = request.form.get('name', '').strip()

    if script_name == "face_dataset" and not student_name:
        return "❌ Please enter your name before capturing your face."

    def script_runner(script, use_camera, student_name=None):
        """Run the selected script inside a thread."""
        if use_camera:
            start_camera()  # Open camera if required
        if student_name:
            script.run(student_name)  # Run with student name
        else:
            script.run()  # Run normally
        if use_camera:
            stop_camera()  # Stop camera after script execution

    # Select and run the appropriate script
    if script_name == "face_dataset":
        current_script = "face_dataset"
        script_thread = threading.Thread(target=script_runner, args=(face_dataset, True, student_name))
    elif script_name == "trained_data":
        current_script = "trained_data"
        script_thread = threading.Thread(target=script_runner, args=(trained_data, False))
    elif script_name == "face_recognization":
        current_script = "face_recognization"
        script_thread = threading.Thread(target=script_runner, args=(face_recognization, True))

    if script_thread:
        script_thread.start()
        script_thread.join()  # Wait until the task is completed

    return redirect(url_for('task_completed'))  # Redirect to completion page



if __name__ == '__main__':
    app.run(debug=True)
