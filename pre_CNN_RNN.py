import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 

from tensorflow.keras.applications import Xception
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import preprocess_input
# from tensorflow.keras.models import Model
import numpy as np

import cv2
# import face_recognition

# Load Xception model pre-trained on ImageNet without the top layer
cnn = Xception(weights='imagenet', include_top=False, pooling='avg')  # Use 'avg' pooling for 1D vector

# Function to extract features from an individual image
def extract_features(img_path):
    img = image.load_img(img_path, target_size=(299, 299))  # Xception expects 299x299 input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # Preprocess to match Xception's input format
    features = cnn.predict(img_array)  # Extract features
    return features  # Returns a 1D feature vector

# Example usage
img_path = 'examples/fake-test.jpg'  # Replace with your image path
features = extract_features(img_path)
print("Extracted features:", features)


#define info
video_path = 'examples/id0_id1_0000.mp4'
FRAMES_NUM = 10


# Load the pre-trained face detector (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to capture a fixed number of frames from a video
def capture_frames(video_path, num_frames=FRAMES_NUM):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate the interval to capture frames evenly
    interval = max(total_frames // num_frames, 1)
    
    captured_frames = []
    current_frame_index = 0
    
    while cap.isOpened() and len(captured_frames) < num_frames:
        ret, frame = cap.read()
        if not ret:
            break
        
        if current_frame_index % interval == 0:
            captured_frames.append(frame)
        
        current_frame_index += 1
    
    cap.release()
    
    # Return the captured frames
    return captured_frames

# Example usage
frames = capture_frames(video_path, num_frames=FRAMES_NUM)

# #visualization
# for i, frame in enumerate(frames):
#     cv2.imshow(f'Frame {i+1}', frame)
#     cv2.waitKey(500)  # Display each frame for 500 ms

cv2.destroyAllWindows()


