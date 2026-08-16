# Smart-Attendance
A smart project to mark attendance using camera-based face recognition and fingerprint authentication.
Project Overview

The Smart Attendance System is an automated attendance management system developed using face recognition and fingerprint authentication. The project is designed to improve attendance security, accuracy, and efficiency while reducing manual work and proxy attendance.

The system combines ESP32-CAM, ESP32 DevKit V1, R307 Fingerprint Sensor, SSD1306 OLED Display, Python/OpenCV, and digital attendance storage into one integrated solution.

Key Features

Face detection and recognition using ESP32-CAM and Python
Fingerprint authentication using the R307 fingerprint sensor
Dual biometric verification using Face ID + Fingerprint ID
Attendance is marked only when both identities belong to the same registered student
Real-time authentication status through the OLED display
Automatic attendance recording with date and time
Wireless communication between ESP32 boards
Google Sheets integration for attendance management
Scope for future cloud and mobile application integration

System Working

The ESP32-CAM captures the student's face.
The Python application detects and recognizes the face using OpenCV and the Face Recognition library.
If the face belongs to a registered student, the corresponding Face ID is retained.
The system requests fingerprint authentication.
The R307 Fingerprint Sensor scans the student's fingerprint.
The fingerprint sensor identifies the registered Fingerprint ID.
The Python application compares the Face ID and Fingerprint ID.
If both IDs correspond to the same student, attendance is marked.
If either authentication fails or the IDs do not match, attendance is not marked.
After successful verification, the attendance record is stored digitally with the student's identity, date, and time and can be sent to Google Sheets.

Authentication Logic

Face Detection → Face Recognition → Face ID

Face ID + Fingerprint ID → Compare

If both IDs match → Attendance Marked → Google Sheets

If IDs do not match → Attendance Not Marked

Hardware Components

ESP32-CAM – Captures live facial images/video and provides Wi-Fi connectivity.
ESP32 DevKit V1 – Acts as the main controller and coordinates the fingerprint sensor and OLED display.
R307 Fingerprint Sensor – Performs fingerprint enrollment and verification.
SSD1306 OLED Display – Provides real-time status messages.
Power Supply and Connecting Wires – Provide power and interconnections between the modules.

Software Components

Python
OpenCV
Face Recognition Library
NumPy
Requests
Arduino IDE
ESP32 firmware
Google Sheets integration
Digital attendance storage

Project Structure

Smart-Attendance-System/

python/
esp32/
arduino/
dataset/
docs/
README.md
.gitignore

Privacy

Student face images, personal attendance records, API credentials, and other private data should not be uploaded to a public GitHub repository.

Advantages

Automated attendance marking
Dual-layer biometric verification
Reduced risk of proxy attendance
Reduced manual work and paperwork
Real-time authentication feedback
Low-cost and scalable prototype
Easy to upgrade with cloud storage and mobile applications

Applications

Schools and colleges
Offices and companies
Industries and factories
Laboratories and research centres
Secure workplaces
Smart security and access-control systems

Future Scope

Cloud-based attendance storage
Google Sheets and database integration
Mobile application integration
Web-based attendance dashboard
Improved AI-based face recognition
RFID/NFC authentication
Large-scale database and server integration
Real-time attendance analytics and notifications

Academic Information

Degree: Bachelor of Engineering (B.E.)
Branch: Mechatronics Engineering
Institution: The Oxford College of Engineering, Bengaluru
Academic Year: 2025–2026

Smart Attendance System — Face Recognition + Fingerprint Authentication
