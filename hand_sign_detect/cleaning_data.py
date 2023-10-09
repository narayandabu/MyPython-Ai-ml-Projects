import os
import pickle
import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.5)

DATA_DIR = './hand_sign_detect/raw_data/Dataset/train'

data = []
labels = []
for dir_ in os.listdir(DATA_DIR):
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        data_aux = []
        cleaned_x = []
        cleaned_y = []

        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    cleaned_x.append(x)
                    cleaned_y.append(y)
                    data_aux.append(x - min(cleaned_x))
                    data_aux.append(y - min(cleaned_y))
            data.append(data_aux)
            labels.append(dir_)
            


f = open('data.pickle', 'wb')
pickle.dump({'data': data, 'labels': labels}, f)
f.close()