import cv2
import requests

# Set to your live Render API URL or local URL for testing
API_URL = "https://face-expression-detector.onrender.com/predict"
# API_URL = "http://127.0.0.1:8000/predict" # Uncomment for local backend testing

camera = cv2.VideoCapture(0)

print("Starting Real-time Emotion Detector Test...")
print("Press 'q' in the window to exit.")

while True:
    ret, frame = camera.read()
    if not ret:
        print("Error: Could not read frame from camera.")
        break

    # Convert frame to JPEG byte stream
    _, img_encoded = cv2.imencode(".jpg", frame)

    try:
        response = requests.post(
            API_URL,
            files={
                "file": (
                    "image.jpg",
                    img_encoded.tobytes(),
                    "image/jpeg"
                )
            },
            timeout=3  # Prevent camera freeze if network drops
        )

        if response.status_code == 200:
            result = response.json()
            emotion = result.get('emotion', 'Detecting...')
            confidence = result.get('confidence', 0)

            text = f"{emotion}: {confidence}%"

            # Draw prediction text on webcam feed
            cv2.putText(
                frame,
                text,
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv2.LINE_AA
            )
        else:
            print(f"API Error: Status {response.status_code}")

    except Exception as e:
        print(f"Connection Error: {e}")

    cv2.imshow("Realtime Emotion Detector API Test", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
