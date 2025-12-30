@echo off
REM --- 1. Navigate to the project directory ---
REM This command ensures the script runs from the correct folder, regardless of where the user double-clicks it.
cd /d "%~dp0"

echo Starting Surveillance Dashboard...

REM --- 2. Launch the Flask Server in a new, hidden window ---
REM The /B switch runs the command without waiting for it to finish.
start /B python app.py

REM --- 3. Wait for the server to initialize ---
REM Wait 5 seconds to give Flask time to fully start up and open the webcam feed.
timeout /t 5 /nobreak > nul

REM --- 4. Open the default browser to the Login Page ---
start "" "http://127.0.0.1:5000"

echo Presentation Ready.
exit