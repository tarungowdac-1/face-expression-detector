import cv2

from src.emotion import EmotionDetector


detector = EmotionDetector()


camera = cv2.VideoCapture(0)


while True:

    ret, frame = camera.read()

    if not ret:
        break


    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )


    faces = face_cascade.detectMultiScale(
        gray,
        1.3,
        5
    )


    for (x,y,w,h) in faces:

        face = frame[
            y:y+h,
            x:x+w
        ]


        emotion, confidence = detector.predict(
            face
        )


        text = f"{emotion} {confidence*100:.2f}%"


        cv2.rectangle(
            frame,
            (x,y),
            (x+w,y+h),
            (0,255,0),
            2
        )


        cv2.putText(
            frame,
            text,
            (x,y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0,255,0),
            2
        )


    cv2.imshow(
        "Emotion Detector",
        frame
    )


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



camera.release()

cv2.destroyAllWindows()