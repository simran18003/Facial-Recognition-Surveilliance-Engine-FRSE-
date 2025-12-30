@echo off
REM --- 1. Navigate to the project directory ---
cd /d "%~dp0"

echo ==========================================================
echo === FACE ENROLLMENT & ENCODING TOOL ===
echo ==========================================================

REM --- Optional: Check if the main application is running ---
REM This is a helpful warning for the user
echo WARNING: Ensure the main dashboard is CLOSED (Ctrl+C) before running this tool.
pause

REM --- 2. Run the Python Encoding Script ---
REM This launches the interactive menu defined in encode_faces.py
python encode_faces.py

echo.
echo ==========================================================
echo === ENCODING COMPLETE. RESTART DASHBOARD NOW. ===
echo ==========================================================
pause

exit