import os
import cv2


DATA_DIR = 'hand_sign_detect/raw_data/Dataset'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


dataset_size = 300

cap = cv2.VideoCapture(0)
data_type=input("Enter the Name of the sign ! \n")
if not os.path.exists(os.path.join(DATA_DIR, data_type)):
    os.makedirs(os.path.join(DATA_DIR, data_type))
    print('Collecting data for class {}'.format(data_type))
    done = False
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, 'Ready? Press "g" to go ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('g'):
            break
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        cv2.imwrite(os.path.join(DATA_DIR, data_type, '{}.jpg'.format(counter)), frame)
        counter +=1

cap.release()
cv2.destroyAllWindows()