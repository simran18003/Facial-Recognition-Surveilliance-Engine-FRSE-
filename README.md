🔐 Facial Recognition Surveillance Engine (FRSE)
<p align="center"> <strong>Real-Time Facial Recognition Surveillance System with IoT & Telegram Alerts</strong> </p> <p align="center"> 🎓 7th Semester Major Project &nbsp;|&nbsp; 👁️ Computer Vision &nbsp;|&nbsp; 📱 IoT Integration </p>
📌 About the Project

Facial Recognition Surveillance Engine (FRSE) is a real-time security surveillance system developed as a 7th Semester Major Project.
The system automatically detects known and unknown individuals, captures evidence of intruders, logs events, and sends instant Telegram alerts with images and timestamps.

To enhance security and recognition accuracy, this project integrates a smartphone camera as an IoT device using Camo Studio, instead of relying on a low-quality laptop webcam.

🎓 Academic Details

Project Type: Major Project

Semester: 7th Semester

Domain: Computer Vision, IoT, Security Systems

Application: Real-Time Surveillance & Intruder Detection

📱 IoT Camera Integration (Key Highlight)

Unlike traditional systems that use built-in webcams, this project uses a smartphone camera connected via Camo Studio, which acts as a virtual webcam for OpenCV.

✅ Why Smartphone Camera?

📸 Higher resolution & sharper images

🌙 Better low-light performance

🎯 Improved face recognition accuracy

🔌 Seamless integration with OpenCV

cv2.VideoCapture(0)


This approach significantly improves surveillance quality and reliability.

🚨 Telegram Alert System

When an unknown face (intruder) is detected:

📸 Snapshot is captured automatically

⏱ Timestamp is generated

📩 Image + alert message sent via Telegram Bot

📊 Event appears on the dashboard

🗂 Logs & images stored locally

This enables instant remote monitoring.

✨ Key Features

🎥 Real-time face detection & recognition

📱 Smartphone camera integration (IoT)

🚨 Automatic intruder detection

📸 Image capture with timestamp

🔔 Telegram alerts with photo evidence

📊 Flask-based web dashboard

🧵 Multi-threaded processing

🔐 Secure API key handling (.env)

📁 CSV-based logging

🛠️ Technologies Used
Language:	Python
Computer Vision:	OpenCV, face_recognition
Backend:	Flask
Numerical:	NumPy
Alerts	Telegram: Bot API
IoT Camera:	Camo Studio
Performance:	Threading
Logging:	CSV
Security:	python-dotenv
📂 Project Structure
facial-recognition-surveillance/
│
├── app.py
├── encodings.pickle
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── logs.html
│   └── add_person.html
│
├── static/
│   ├── css/
│   └── js/
│
├── unknown_logs/
│   ├── images/
│   └── logs.csv
│
├── .gitignore
├── .env.example
└── README.md

▶️ How to Run the Project
🔹 1. Clone the Repository
git clone https://github.com/your-username/Facial-Recognition-Surveilliance-Engine-FRSE-.git
cd Facial-Recognition-Surveilliance-Engine-FRSE-

🔹 2. (Optional) Create Virtual Environment
python -m venv venv
venv\Scripts\activate

🔹 3. Install Dependencies manually:

pip install opencv-python face_recognition flask numpy python-dotenv requests

🔹 4. Configure Environment Variables

Create a .env file:

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id


⚠️ Never upload .env to GitHub

🔹 5. Connect Smartphone Camera

Install Camo Studio (PC)

Install Camo App (Phone)

Connect phone via USB/Wi-Fi

Select Camo Camera as input device

🔹 6. Run the Application
python app.py


Open in browser:

http://127.0.0.1:5000

📊 Dashboard Features

Live camera feed

Intruder detection logs

Timestamped image records

Registered faces count

🔐 Security Practices

❌ No hard-coded secrets

✅ Environment variables (.env)

✅ .gitignore prevents leaks

🔄 Token revocation supported

❌ Surveillance data excluded from GitHub

🗣️ Viva / Interview Explanation

“This project is a real-time facial recognition surveillance system where I integrated a smartphone camera as an IoT device using Camo Studio for better accuracy.
Whenever an intruder is detected, the system captures an image, logs the event, and sends a Telegram alert with timestamp and photo evidence.”

🚀 Future Enhancements

Confidence score for recognition

Cloud database integration

Mobile dashboard app

Multi-camera support

AI-based behavior analysis

🏁 Conclusion

This project demonstrates a practical implementation of computer vision and IoT integration for real-world security use cases.
It emphasizes performance, automation, and secure system design, making it suitable for academic evaluation and industry-level discussion.
