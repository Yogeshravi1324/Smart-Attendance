# Smart-Attendance
A smart project to mark attendance with camera and fingerprint
## Project Overview

The **Smart Attendance System** is an automated attendance management system developed using **face recognition and fingerprint authentication**. The project is designed to improve attendance security, accuracy, and efficiency while reducing manual work and proxy attendance.

The system combines **ESP32-CAM, ESP32 DevKit V1, R307 Fingerprint Sensor, SSD1306 OLED Display, Python/OpenCV, and digital attendance storage** into one integrated solution.

## Key Features

- Face detection and recognition using ESP32-CAM and Python.
- Fingerprint authentication using the R307 fingerprint sensor.
- Dual biometric verification using **Face ID + Fingerprint ID**.
- Attendance is marked only when both identities belong to the same registered student.
- Real-time authentication status through the OLED display.
- Automatic attendance recording with date and time.
- Wireless communication between ESP32 boards.
- Scope for cloud/Google Sheets integration and future monitoring applications.

## System Working

The authentication process follows these steps:

1. The **ESP32-CAM** captures the student's face.
2. The Python application detects and recognizes the face using **OpenCV and the Face Recognition library**.
3. If the face belongs to a registered student, the corresponding **Face ID** is retained.
4. The system requests fingerprint authentication.
5. The **R307 Fingerprint Sensor** scans the student's fingerprint.
6. The fingerprint sensor identifies the registered **Fingerprint ID**.
7. The Python application compares the Face ID and Fingerprint ID.
8. If both IDs correspond to the same student, **attendance is marked**.
9. If either authentication fails or the IDs do not match, **attendance is not marked**.
10. After successful verification, the attendance record is stored digitally with the student's identity, date, and time.

## Authentication Logic

```text
             Face Detection
                   |
                   v
             Face Recognition
                   |
             Face Matched?
              /          \
            No            Yes
            |              |
         Reject        Store Face ID
                           |
                           v
                  Fingerprint Scan
                           |
                           v
                    Fingerprint ID
                           |
                           v
                  Compare Both IDs
                    /          \
                 Match       No Match
                   |             |
                   v             v
          Mark Attendance      Reject
                   |
                   v
             Store Attendance
```

## Hardware Components

- **ESP32-CAM** – captures live facial images/video and provides Wi-Fi connectivity.
- **ESP32 DevKit V1** – acts as the main controller and coordinates the fingerprint sensor and OLED.
- **R307 Fingerprint Sensor** – performs fingerprint enrollment and verification.
- **SSD1306 OLED Display** – provides real-time status messages.
- **Power supply and connecting wires** – provide power and interconnections between the modules.

## Software Components

- Python
- OpenCV
- Face Recognition Library
- NumPy
- Requests
- Arduino IDE
- ESP32 firmware
- Digital attendance database/storage
- Google Sheets integration (planned/implemented as part of the project workflow)

## Project Structure

```text
Smart-Attendance-System/
│
├── python/
│   └── Python source code
│
├── esp32/
│   └── ESP32-CAM / ESP32 source code
│
├── arduino/
│   └── Arduino source code
│
├── dataset/
│   └── Local student face dataset
│
├── docs/
│   ├── Project Report.pdf
│   └── Presentation.pdf
│
├── README.md
└── .gitignore
```

> **Privacy:** Student face images, personal attendance records, API credentials, and other private data should not be uploaded to a public GitHub repository.

## Advantages

- Automated attendance marking.
- Dual-layer biometric verification.
- Reduced risk of proxy attendance.
- Reduced manual work and paperwork.
- Real-time authentication feedback.
- Low-cost and scalable prototype.
- Can be extended with cloud storage and web/mobile applications.

## Applications

- Schools and colleges
- Offices and companies
- Industries and factories
- Laboratories and research centres
- Secure workplaces
- Smart security and access-control systems

## Future Scope

The system can be further improved through:

- Cloud-based attendance storage.
- Google Sheets/database integration.
- Mobile application integration.
- Web-based attendance dashboard.
- Improved AI-based face recognition.
- RFID/NFC authentication.
- Large-scale database and server integration.
- Real-time attendance analytics and notifications.

## Academic Information

**Degree:** Bachelor of Engineering (B.E.)  
**Branch:** Mechatronics Engineering  
**Institution:** The Oxford College of Engineering, Bengaluru  
**Academic Year:** 2025–2026

## References

The project report references work and documentation related to:

- Face recognition and biometric recognition.
- OpenCV.
- ESP32-CAM.
- R307 Fingerprint Sensor.
- Arduino IDE.
- Python Face Recognition Library.

---

**Smart Attendance System — Face Recognition + Fingerprint Authentication**
