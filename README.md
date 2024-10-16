# Attendance System
Attendance System using Face Recognition with Realtime Database
**Overview**
This project implements an Attendance System using Face Recognition technology integrated with a Realtime Database (e.g., Firebase). The system is designed to automate attendance tracking by detecting and recognizing faces through a live webcam feed. The recognized faces are matched with pre-encoded facial data, and attendance is marked in a database. Additionally, employee details such as attendance count, email, phone number, and more are displayed on the user interface.

**Features**
Face Recognition: Utilizes the face_recognition library to detect and recognize faces.
Real-time Database Integration: Uses Firebase's Realtime Database to store employee details and attendance records.
Employee Details: Displays information such as total attendance, name, email, phone number, and more for each recognized face.
Automatic Attendance Logging: Marks attendance in real time when an employee's face is detected.
Scalable & Secure: Secure integration with Firebase for real-time updates and cloud-based storage.
Image Uploading: Supports uploading employee images to Firebase Storage for recognition purposes.

**Technologies Used**
Python: Core language for the project.
OpenCV: For image processing and handling webcam feeds.
face_recognition: For face detection and recognition.
Firebase Realtime Database: To store employee data and attendance records.
Firebase Storage: For storing employee images.
Git: For version control and collaboration.

**Prerequisites**
Make sure you have the following installed:
Python 3.x
OpenCV (cv2)
face_recognition library
Firebase Admin SDK
Git

**How It Works**

**1. Face Detection and Recognition**
The system uses OpenCV to capture frames from the webcam.
Detected faces are encoded and compared with pre-stored facial encodings.
If a match is found, the employee's details are fetched from Firebase.
**2. Attendance Marking**
When an employee's face is recognized, their attendance is automatically marked in the Realtime Database.
The employee's attendance count is updated, and their details are displayed.
**3. UI Display**
A custom user interface is used to show the employee’s name, attendance count, and other details.
The system can display an image of the employee alongside their details.
