import cv2
import face_recognition  # type: ignore
import os
import requests
import numpy as np
from datetime import datetime
import time
import serial
import threading
import gspread
import google.oauth2.service_account

# ==========================
# CONFIGURATION
# ==========================

DATASET = "dataset"
ATTENDANCE_FILE = "attendance.csv"

ESP32_CAPTURE = "http://10.97.3.223//capture"  # <-- update if your CAM's IP changes

# Google Sheets
GOOGLE_SHEET_ID = "1nnThEEu8-9focHInSZ2nva61FSXeax7eeY0e7mfYJXA"
SERVICE_ACCOUNT_FILE = "smart-attendance-502504-beb55a5098f1.json"

# ==========================
# GOOGLE SHEETS SETUP
# ==========================

sheet = None
try:
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = google.oauth2.service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
    print("Connected to Google Sheet.")
except Exception as e:
    print("Could not connect to Google Sheets - attendance will still be saved locally.")
    print("Reason:", e)

# ESP32 DevKit (fingerprint) - update COM port to match Device Manager
arduino = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)

# Map fingerprint IDs to names - fill this in based on what you enrolled
fingerprint_map = {
    1: "",
    2: "", 
}

FINGERPRINT_TIMEOUT = 10  # seconds to wait for a scan after a face is recognized

# ==========================
# LOAD DATASET
# ==========================

known_encodings = []
known_names = []

print("Loading Dataset...")

for student_id in os.listdir(DATASET):
    student_folder = os.path.join(DATASET, student_id)
    if not os.path.isdir(student_folder):
        continue

    for image_file in os.listdir(student_folder):
        image_path = os.path.join(student_folder, image_file)
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if len(encodings) > 0:
                known_encodings.append(encodings[0])
                known_names.append(student_id)
                print(f"Loaded: {student_id}")
        except Exception as e:
            print("Error:", image_path, e)

print(f"\nTraining Complete")
print(f"Total Faces Loaded: {len(known_names)}")

# ==========================
# SHARED STATE (guarded by lock - touched from both threads)
# ==========================

lock = threading.Lock()
marked_today = {}
waiting_for_fingerprint = False
recognized_face = None
verification_start_time = 0

def send_to_arduino(line: str):
    try:
        arduino.write((line + "\n").encode())
    except Exception as e:
        print("Serial write error:", e)

def display(line1: str, line2: str = ""):
    send_to_arduino(f"DISPLAY:{line1}|{line2}")

# ==========================
# ATTENDANCE
# ==========================

def write_to_google_sheet(row):
    if sheet is None:
        return
    try:
        sheet.append_row(row)
    except Exception as e:
        print("Google Sheets write failed (attendance is still saved locally):", e)

def mark_attendance(name, method="fingerprint"):
    now = datetime.now()
    current_time = time.time()

    with lock:
        if name in marked_today and current_time - marked_today[name] < 10:
            return False
        marked_today[name] = current_time

    date = now.strftime("%Y-%m-%d")
    clock = now.strftime("%H:%M:%S")

    with open(ATTENDANCE_FILE, "a") as f:
        f.write(f"{name},{date},{clock},{method}\n")

    print(f"Attendance Marked ({method}): {name}")

    # Push to Google Sheets in a background thread so a slow/flaky
    # network call never delays the camera loop or fingerprint scanning.
    threading.Thread(
        target=write_to_google_sheet,
        args=([name, date, clock, method],),
        daemon=True
    ).start()

    return True

# ==========================
# FINGERPRINT LISTENER THREAD
# ==========================

def fingerprint_listener():
    global waiting_for_fingerprint, recognized_face

    while True:
        try:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode(errors="ignore").strip()

                if line.startswith("FP:"):
                    with lock:
                        currently_waiting = waiting_for_fingerprint
                        face_at_scan_time = recognized_face

                    if not currently_waiting:
                        # No face was verified first - ignore this scan.
                        # Remove this check if you want fingerprint-only mode.
                        print("Fingerprint scanned but no face was verified first - ignoring.")
                        continue

                    fp_id = int(line.split(":")[1])
                    fp_name = fingerprint_map.get(fp_id, f"Unknown_FP_{fp_id}")

                    # --- FIX: cross-check fingerprint owner against the face
                    # that actually triggered this verification window. ---
                    if fp_name.startswith("Unknown_FP_"):
                        print(f"Fingerprint ID {fp_id} is not in fingerprint_map - not marked.")
                        display("Unknown", "fingerprint")

                    elif fp_name != face_at_scan_time:
                        # Someone else's fingerprint was used to confirm this face.
                        print(f"Mismatch: face was '{face_at_scan_time}' but fingerprint "
                              f"belongs to '{fp_name}' - not marked.")
                        display("Mismatch!", "Face/FP differ")

                    else:
                        marked = mark_attendance(fp_name, method="face+fingerprint")
                        if marked:
                            display(f"Welcome {fp_name}", "Attendance Marked")
                        else:
                            display(f"{fp_name}", "Already marked")

                    with lock:
                        waiting_for_fingerprint = False
                        recognized_face = None

                    time.sleep(2)  # let the message stay on screen
                    display("Smart Attendance", "Show your face")

        except Exception as e:
            print("Fingerprint listener error:", e)
        time.sleep(0.1)

fp_thread = threading.Thread(target=fingerprint_listener, daemon=True)
fp_thread.start()

# ==========================
# CAMERA LOOP
# ==========================

print("\nConnecting to ESP32-CAM...\n")
display("Smart Attendance", "Show your face")

while True:
    try:
        response = requests.get(ESP32_CAPTURE, timeout=5)
        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if frame is None:
            print("Frame Error")
            continue

        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            if True in matches:
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match = np.argmin(face_distances)
                if matches[best_match]:
                    name = known_names[best_match]

            top, right, bottom, left = face_location
            top *= 2; right *= 2; bottom *= 2; left *= 2

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            with lock:
                already_waiting = waiting_for_fingerprint

            if name != "Unknown" and not already_waiting:
                with lock:
                    recognized_face = name
                    waiting_for_fingerprint = True
                    verification_start_time = time.time()

                print(f"\nFace Verified : {name}")
                print("Please scan your fingerprint...")
                display(f"Hi {name}!", "Scan fingerprint")

        with lock:
            timed_out = (waiting_for_fingerprint and
                         time.time() - verification_start_time > FINGERPRINT_TIMEOUT)

        if timed_out:
            print("Fingerprint verification timed out.")
            with lock:
                waiting_for_fingerprint = False
                recognized_face = None
            display("Timed out", "Try again")
            time.sleep(1.5)
            display("Smart Attendance", "Show your face")

        cv2.imshow("Smart Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Esc to quit
            break

    except Exception as e:
        print("Camera Error:", e)

cv2.destroyAllWindows()
arduino.close()
