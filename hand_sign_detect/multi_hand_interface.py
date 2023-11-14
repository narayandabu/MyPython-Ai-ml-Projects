import pickle
import cv2
import mediapipe as mp
import numpy as np

path1 = 'C:/Users/naray/OneDrive/Desktop/Devlopment/AiML/hand_sign_detect/single_hand_model.p'
path2 = 'C:/Users/naray/OneDrive/Desktop/Devlopment/AiML/hand_sign_detect/multiple_hand_model.p'
model1_dict = pickle.load(open(path1, 'rb'))
model2_dict = pickle.load(open(path2, 'rb'))

single_hand_model = model1_dict['single_hand_model']
multiple_hand_model = model2_dict['multiple_hand_model']


cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

while True:
    if  cv2.waitKey(1) & 0xFF == ord('q'):
        break
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
 
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks is not None and len(results.multi_hand_landmarks)==1 :
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,  
                    hand_landmarks,  
                    mp_hands.HAND_CONNECTIONS,  
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                
                    x_.append(x)
                    y_.append(y)

                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            prediction = single_hand_model.predict([np.asarray(data_aux)])
            predicted_character = prediction[0]
        
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, "single-hand", (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                    cv2.LINE_AA)
            cv2.putText(frame, "Predicted {}".format(predicted_character), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                    cv2.LINE_AA)
    if results.multi_hand_landmarks is not None and len(results.multi_hand_landmarks)==2 :
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,  
                    hand_landmarks,  
                    mp_hands.HAND_CONNECTIONS,  
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                
                    x_.append(x)
                    y_.append(y)

                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            prediction = multiple_hand_model.predict([np.asarray(data_aux)])
            predicted_character = prediction[0]
            cv2.putText(frame, "multi-hand", (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                    cv2.LINE_AA)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, "Predicted {}".format(predicted_character), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                    cv2.LINE_AA)
    cv2.imshow('frame', frame)
    

cap.release()
cv2.destroyAllWindows()