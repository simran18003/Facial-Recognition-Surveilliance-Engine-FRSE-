import face_recognition
import pickle
import cv2
import os
import time

def capture_and_save_faces():
    """
    Opens the webcam to capture and save images for a new known person.
    """
    name = input("Enter the name of the person: ")
    if not name:
        print("Name cannot be empty. Aborting.")
        return False

    person_dir = os.path.join("known_faces", name)
    os.makedirs(person_dir, exist_ok=True)
    
    print(f"\n[INFO] Directory created for {name}.")
    print("[INFO] Preparing to capture 5 images. Please look at the camera.")
    print("Press 'c' to capture an image when ready. Press 'q' to quit.")

    # Initialize webcam -->0 and via phone -->1
    video_capture = cv2.VideoCapture(1)
    img_count = 0
    CAPTURES_REQUIRED = 5

    while img_count < CAPTURES_REQUIRED:
        ret, frame = video_capture.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break
        
        cv2.imshow('Video - Press "c" to capture, "q" to quit', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('c'):
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb_frame, model="hog")
            
            if len(boxes) == 1:
                img_count += 1
                img_path = os.path.join(person_dir, f"{name}_{img_count}.jpg")
                cv2.imwrite(img_path, frame)
                print(f"Captured image {img_count}/{CAPTURES_REQUIRED} and saved to {img_path}")
                time.sleep(0.5) 
            elif len(boxes) > 1:
                print("[WARNING] More than one face detected. Please ensure only one person is in frame.")
            else:
                print("[WARNING] No face detected. Please position yourself clearly in the frame.")

        elif key == ord('q'):
            print("[INFO] Quitting capture.")
            break
            
    video_capture.release()
    cv2.destroyAllWindows()
    if img_count < CAPTURES_REQUIRED:
        print("\n[WARNING] Did not capture the required number of images. Encoding may be less accurate.")
        proceed = input("Proceed with encoding? (y/n): ").lower()
        if proceed != 'y':
            print("Aborting encoding process.")
            return False
    return True

def encode_known_faces():
    """
    Scans the known_faces directory, creates all face encodings, and saves them
    to 'encodings.pickle'.
    """
    dataset_path = "known_faces"
    print("\n[INFO] Starting to process and encode all faces...")
    known_encodings = []
    known_names = []

    for name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, name)
        if not os.path.isdir(person_path):
            continue

        for filename in os.listdir(person_path):
            if not filename.endswith(('.jpg', '.jpeg', '.png')):
                continue
                
            image_path = os.path.join(person_path, filename)
            
            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            boxes = face_recognition.face_locations(rgb, model="hog") 
            encodings = face_recognition.face_encodings(rgb, boxes)
            
            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(name)

    print("[INFO] Serializing encodings...")
    data = {"encodings": known_encodings, "names": known_names}
    with open("encodings.pickle", "wb") as f:
        f.write(pickle.dumps(data))

    print("[INFO] Encodings saved successfully to encodings.pickle")


if __name__ == "__main__":
    # This block allows the script to run as a standalone application
    print("--- Face Recognition Setup ---")
    print("1. Register a new person via webcam")
    print("2. Encode existing photos in 'known_faces' folder")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        if capture_and_save_faces():
             encode_known_faces()
    elif choice == '2':
        encode_known_faces()
    else:
        print("Invalid choice. Please run the script again and enter 1 or 2.")