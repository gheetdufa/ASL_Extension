import os
import pickle
import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './data'

data = []
labels = []

# Define the length of the feature vector based on the expected number of landmarks and the features extracted
NUM_LANDMARKS = 21  # Mediapipe typically detects 21 landmarks
FEATURES_PER_LANDMARK = 2  # x and y coordinates
EXPECTED_FEATURE_LENGTH = NUM_LANDMARKS * FEATURES_PER_LANDMARK

for dir_ in os.listdir(DATA_DIR):
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        data_aux = [0] * EXPECTED_FEATURE_LENGTH  # Initialize with zeros

        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    # Calculate the index for the feature vector
                    index = i * FEATURES_PER_LANDMARK
                    data_aux[index] = x
                    data_aux[index + 1] = y

        data.append(data_aux)
        labels.append(dir_)

with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)
