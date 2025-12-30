import os
import csv

# --- Configuration ---
LOG_FILE = "unknown_logs/logs.csv"
UNKNOWN_IMAGES_DIR = "unknown_logs/images"
HEADER = ['timestamp', 'image_file']

def clear_all_logs():
    print("--- Starting Log Cleanup ---")
    
    # 1. Clear all image files
    if os.path.exists(UNKNOWN_IMAGES_DIR):
        for filename in os.listdir(UNKNOWN_IMAGES_DIR):
            file_path = os.path.join(UNKNOWN_IMAGES_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                print(f"[CLEANUP] Deleted image: {filename}")
            except Exception as e:
                print(f"[ERROR] Failed to delete {file_path}. Reason: {e}")
    else:
        print("[INFO] Image directory not found, skipping image deletion.")

    # 2. Delete and recreate the CSV file
    try:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
            print(f"[CLEANUP] Deleted old log file: {LOG_FILE}")
        
        # 3. Recreate the file with header row
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)
        print(f"[SUCCESS] {LOG_FILE} recreated with header. Logs are clear.")

    except Exception as e:
        print(f"[ERROR] Could not clear or recreate {LOG_FILE}. Please check permissions. Reason: {e}")
    
    print("--- Cleanup Complete. Restart Dashboard. ---")


if __name__ == "__main__":
    clear_all_logs()