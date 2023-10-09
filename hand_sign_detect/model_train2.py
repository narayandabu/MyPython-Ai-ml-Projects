import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import os
import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.5)

DATA_DIR = './hand_sign_detect/raw_data/Dataset/train'

single_hand_data = np.array([])
single_hand_labels = np.array([])
multiple_hand_data = np.array([])
multiple_hand_labels = np.array([])

for dir_ in os.listdir(DATA_DIR):
    ct=0
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        if ct==113:
            break
        cleaned_x = []
        cleaned_y = []
        data_aux = []
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
            data=np.append(data,data_aux)
            labels=np.append(labels,dir_)
        ct+=1
    print(dir_)
for dir_ in os.listdir(DATA_DIR):
    ct=0
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        if ct==113:
            break
        cleaned_x = []
        cleaned_y = []
        data_aux = []
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
            data=np.append(data,data_aux)
            labels=np.append(labels,dir_)
        ct+=1
    print(dir_)
print(data.shape," ",labels.shape)

x_train=data, y_train=labels

model = RandomForestClassifier()
model.fit(x_train, y_train)

f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()