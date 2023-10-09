import cv2
import mediapipe as mp

obj = cv2.VideoCapture(0)
face_detect = mp.solutions.face_detection
while True:
    key, frame = obj.read()
    H, W, _ = frame.shape
    with face_detect.FaceDetection(model_selection=1, min_detection_confidence=0.3) as fd:
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out = fd.process(img_rgb)
        if out.detections is not None:
            for detection in out.detections:
                locationdt = detection.location_data
                bbox = locationdt.relative_bounding_box
                x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                x1 = int((x1 * W))
                y1 = int((y1 * H) - 15)
                w = int((w * W))
                h = int((h * H))
                frame = cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 10)
                frame = cv2.putText(frame, 'Human', (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255), 4)
                # __________To Blur Your face___________
                # if (x1>0 and y1>0)and(x1<W and y1<H):
                #     frame[y1:y1+h,x1:x1+h,:]=cv2.blur(frame[y1:y1+h,x1:x1+h,:],(30,30))
                # _______________________________________
        cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
obj.release()
cv2.destroyAllWindows()
