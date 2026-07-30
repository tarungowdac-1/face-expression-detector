import cv2
import requests


API_URL = "http://127.0.0.1:8000/predict"


camera = cv2.VideoCapture(0)


while True:

    ret, frame = camera.read()

    if not ret:
        break


    # Convert frame to jpg
    _, img_encoded = cv2.imencode(
        ".jpg",
        frame
    )


    try:

        response = requests.post(
            API_URL,
            files={
                "file": (
                    "image.jpg",
                    img_encoded.tobytes(),
                    "image/jpeg"
                )
            }
        )


        result = response.json()


        text = (
            f"{result.get('emotion')} "
            f"{result.get('confidence')}%"
        )


        cv2.putText(
            frame,
            text,
            (20,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )


    except Exception as e:

        print(e)


    cv2.imshow(
        "Realtime Emotion Detector",
        frame
    )


    if cv2.waitKey(1) & 0xff == ord("q"):
        break



camera.release()
cv2.destroyAllWindows()
