import face_recognition  # Face recognition library
import cv2  # OpenCV library
import os  # For file and directory operations
import numpy as np  # For mathematical calculations

# Set the path to the database
image_dir = r"C:\Miniconda3\envs\oss\known_faces"  # Path to the folder containing saved face images
known_face_encodings = []  # List for face encodings
known_face_names = []  # List for face names

# Extract features from saved images
print("Loading known faces...")
for file_name in os.listdir(image_dir):  # Iterate over all files in the directory
    image_path = os.path.join(image_dir, file_name)  # Generate the file path
    try:
        image = face_recognition.load_image_file(image_path)  # Load the face image
        encoding = face_recognition.face_encodings(image)[0]  # Extract the first face encoding
        known_face_encodings.append(encoding)  # Save the extracted encoding
        known_face_names.append(os.path.splitext(file_name)[0])  # Save the file name as the person's name
        print(f"Loaded: {file_name}")  # Output successfully loaded file
    except IndexError:  # Handle cases where no face is detected
        print(f"Face not found in {file_name}. Skipping...")
print("Finished loading known faces.")  # Indicate completion of face data loading

# Camera setup
print("Starting camera...")
video_capture = cv2.VideoCapture(0)  # Start capturing from the default camera (ID 0)
while True:
    ret, frame = video_capture.read()  # Read a frame from the camera
    if not ret:  # Exit if frame capture fails
        print("Failed to grab frame. Exiting...")
        break

    # Convert BGR image to RGB (face_recognition uses RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Detect face locations and extract encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)  # Detect face locations
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)  # Extract face encodings

    # Process each detected face in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the detected face with known faces in the database
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
        name = "Unknown"  # Default value for unidentified faces
        # Find the most similar face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)  # Calculate similarity
        best_match_index = np.argmin(face_distances)  # Get the index of the closest match
        if matches[best_match_index]:  # If a match is found
            name = known_face_names[best_match_index]  # Update name with the matched face

        # Draw a rectangle around the face and display the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # Draw a red rectangle around the face
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)  # Display the name

    # Show the resulting frame
    cv2.imshow('Face Recognition', frame)
