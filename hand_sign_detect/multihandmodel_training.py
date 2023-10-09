import os
import pickle
import mediapipe as mp
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.5)

DATA_DIR = './hand_sign_detect/raw_data/Dataset'

single_hand_data = []
single_hand_labels = []
multiple_hand_data = []
multiple_hand_labels = []

for dir_ in os.listdir(DATA_DIR):

  for img_path in os.listdir(os.path.join(DATA_DIR,dir_)):
        data_aux = []
        cleaned_x = []
        cleaned_y = []

        img = cv2.imread(os.path.join(DATA_DIR,dir_,img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)
        # single hand
        if results.multi_hand_landmarks is not None and len(results.multi_hand_landmarks)==1 :
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    cleaned_x.append(x)
                    cleaned_y.append(y)
                    data_aux.append(x - min(cleaned_x))
                    data_aux.append(y - min(cleaned_y))
            single_hand_data.append(data_aux)
            single_hand_labels.append(dir_)
        # multi hand
        if results.multi_hand_landmarks is not None and len(results.multi_hand_landmarks)==2 :
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    cleaned_x.append(x)
                    cleaned_y.append(y)
                    data_aux.append(x - min(cleaned_x))
                    data_aux.append(y - min(cleaned_y))
            multiple_hand_data.append(data_aux)
            multiple_hand_labels.append(dir_)

single_hand_data = np.asarray(single_hand_data)
single_hand_labels = np.asarray(single_hand_labels)
multiple_hand_data = np.asarray(multiple_hand_data)
multiple_hand_labels = np.asarray(multiple_hand_labels)

single_hand_model=RandomForestClassifier()
multiple_hand_model=RandomForestClassifier()
single_hand_model.fit(single_hand_data,single_hand_labels)
multiple_hand_model.fit(multiple_hand_data,multiple_hand_labels)

f = open('single_hand_model.p', 'wb')
pickle.dump({'single_hand_model': single_hand_model}, f)
f.close()
f = open('multiple_hand_model.p', 'wb')
pickle.dump({'multiple_hand_model': multiple_hand_model}, f)
f.close()
        





