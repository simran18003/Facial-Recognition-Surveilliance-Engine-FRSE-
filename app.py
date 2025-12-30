import cv2
import face_recognition
import numpy as np
import os
import pickle
from flask import Flask, render_template, Response, request, redirect, url_for, flash
from datetime import datetime
import time
import csv
import threading
import requests # <-- ADDED IMPORT

# --- TELEGRAM CONSTANTS (YOU MUST EDIT THESE TWO LINES) ---
# Paste your Bot Token and your personal Chat ID here
TELEGRAM_BOT_TOKEN = "7548902683:AAFYuMKq8fPACUfHW-DGB5Fw-f7A75ZRbFs" 
# Update this line:
TELEGRAM_CHAT_ID = "-4882099524"
# -----------------------------------------------------------


# --- APPLICATION SETUP ---
app = Flask(__name__)
app.secret_key = "supersecretkey" 

# --- GLOBAL VARIABLES AND CONSTANTS ---
ENCODINGS_PATH = "encodings.pickle"
UNKNOWN_LOGS_DIR = "unknown_logs"
UNKNOWN_IMAGES_DIR = os.path.join(UNKNOWN_LOGS_DIR, "images")
LOG_FILE = os.path.join(UNKNOWN_LOGS_DIR, "logs.csv")

# Performance Tuning
RESIZE_FACTOR = 0.25 
UNKNOWN_LOG_COOLDOWN = 10.0 
CUSTOM_TOLERANCE = 0.65 

# Threading globals
output_frame = None
lock = threading.Lock()
video_capture = cv2.VideoCapture(1) # Using webcam -->0 and via phone -->1

# --- DIRECTORY AND FILE SETUP ---
os.makedirs(UNKNOWN_IMAGES_DIR, exist_ok=True)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'image_file'])

# --- LOAD ENCODINGS ---
print("[INFO] Loading encodings...")
try:
    with open(ENCODINGS_PATH, "rb") as f:
        data = pickle.load(f)
except FileNotFoundError:
    print(f"[ERROR] Encodings file not found at {ENCODINGS_PATH}. Please run encode_faces.py first.")
    data = {"encodings": [], "names": []}


# --- TELEGRAM NOTIFICATION FUNCTION (NEW) ---
def send_telegram_alert(timestamp, image_file):
    """Sends a photo and a message to the Telegram chat."""
    
    # 1. Send the photo
    photo_path = os.path.join(UNKNOWN_IMAGES_DIR, image_file)
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    caption = f"🚨 **INTRUDER ALERT!** 🚨\n\n**Time:** {timestamp}\n**Status:** Unidentified Subject Logged."
    
    try:
        with open(photo_path, 'rb') as photo:
            response = requests.post(url, 
                                     data={'chat_id': TELEGRAM_CHAT_ID, 
                                           'caption': caption,
                                           'parse_mode': 'Markdown'},
                                     files={'photo': photo})
        
        if response.status_code != 200:
            print(f"[ERROR-TELEGRAM] Failed to send photo: {response.text}")
        else:
            print(f"[INFO-TELEGRAM] Alert sent successfully for {image_file}.")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR-TELEGRAM] Connection error during Telegram API call: {e}")
# ---------------------------------------------


# --- RECOGNITION THREAD (MODIFIED) ---
def run_recognition():
    global output_frame, lock, video_capture, data, TELEGRAM_BOT_TOKEN
    last_log_time = 0
    
    while True:
        success, frame = video_capture.read()
        if not success:
            time.sleep(0.1)
            continue
        
        small_frame = cv2.resize(frame, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(data["encodings"], face_encoding)
            name = "Unknown"
            
            face_distances = face_recognition.face_distance(data["encodings"], face_encoding)
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                
                if face_distances[best_match_index] < CUSTOM_TOLERANCE:
                    name = data["names"][best_match_index]
            
            face_names.append(name)
            
            if name == "Unknown":
                current_time = time.time()
                if current_time - last_log_time > UNKNOWN_LOG_COOLDOWN:
                    last_log_time = current_time
                    timestamp = datetime.now()
                    img_name = f"unknown_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
                    img_path = os.path.join(UNKNOWN_IMAGES_DIR, img_name)
                    
                    with lock:
                        save_frame = frame.copy() 
                    
                    # 1. Save Log Data
                    cv2.imwrite(img_path, save_frame)
                    log_timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    with open(LOG_FILE, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([log_timestamp_str, img_name])
                        
                    # 2. Send Telegram Alert (NEW CALL)
                    # We only send the alert if the token is properly configured
                    if TELEGRAM_BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN_HERE":
                        send_telegram_alert(log_timestamp_str, img_name)
                    else:
                        print("[WARNING] Telegram alert skipped. Bot token not configured.")

        # Drawing logic remains the same
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top = int(top / RESIZE_FACTOR)
            right = int(right / RESIZE_FACTOR)
            bottom = int(bottom / RESIZE_FACTOR)
            left = int(left / RESIZE_FACTOR)

            color = (0, 0, 255) if name == "Unknown" else (0, 255, 0)
            
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        with lock:
            output_frame = frame.copy()


def generate_frames():
    # ... (remains the same) ...
    global output_frame, lock
    while True:
        with lock:
            if output_frame is None:
                continue
            
            (flag, encoded_image) = cv2.imencode(".jpg", output_frame)
            if not flag:
                continue
        
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
              bytearray(encoded_image) + b'\r\n')

# --- FLASK ROUTES (Skipped for brevity, remain the same) ---
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def index():
    logs = []
    try:
        known_names_count = len(data['names'])
    except Exception:
        known_names_count = 0
        
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader, None) 
            all_logs = list(reader)
            for row in reversed(all_logs):
                if row: 
                    logs.append({"timestamp": row[0], "image_file": row[1]})
    return render_template('index.html', logs=logs, known_count=known_names_count)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logs')
def show_logs():
    logs = []
    try:
        known_names_count = len(data['names'])
    except Exception:
        known_names_count = 0
        
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader, None) 
            all_logs = list(reader)
            for row in reversed(all_logs):
                if row: 
                    logs.append({"timestamp": row[0], "image_file": row[1]})
    return render_template('logs.html', logs=logs, known_count=known_names_count) 

@app.route('/add_person')
def add_person():
    try:
        known_names_count = len(data['names'])
    except Exception:
        known_names_count = 0
        
    return render_template('add_person.html', known_count=known_names_count)

@app.route('/logs/images/<filename>')
def get_log_image(filename):
    from flask import send_from_directory
    return send_from_directory(UNKNOWN_IMAGES_DIR, filename)

if __name__ == '__main__':
    t = threading.Thread(target=run_recognition)
    t.daemon = True
    t.start()
    
    app.run(debug=True, threaded=True, use_reloader=False)

video_capture.release()