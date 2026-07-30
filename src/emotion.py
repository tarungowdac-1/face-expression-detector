import os
import cv2
import numpy as np
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "emotion_model.keras")

EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# Load model once when server starts
model = tf.keras.models.load_model(MODEL_PATH)

# Load Haar Cascade face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def predict_emotion(image_bytes):
  # Convert bytes to image
  np_array = np.frombuffer(image_bytes, np.uint8)
  frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

  if frame is None:
    return {"error": "Invalid image"}

  # Convert frame to grayscale
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # Detect faces
  faces = face_cascade.detectMultiScale(
      gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
  )

  # Edge case: No face detected in image
  if len(faces) == 0:
    return {
        "emotion": "No Face Detected",
        "confidence": 0.0,
        "error": "No face found in frame",
    }

  # Isolate largest face and square the crop region
  x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
  size = max(w, h)
  margin = int(size * 0.1)

  y1 = max(0, y - margin)
  y2 = min(frame.shape[0], y + h + margin)
  x1 = max(0, x - margin)
  x2 = min(frame.shape[1], x + w + margin)

  face_roi = gray[y1:y2, x1:x2]

  # Equalize contrast & normalize image
  face_roi = cv2.equalizeHist(face_roi)
  face = cv2.resize(face_roi, (48, 48))
  face = face / 255.0

  # Reshape for Keras (1, 48, 48, 1)
  face = np.expand_dims(face, axis=0)
  face = np.expand_dims(face, axis=-1)

  # Predict
  prediction = model.predict(face, verbose=0)
  emotion_index = np.argmax(prediction)
  confidence = float(np.max(prediction))

  return {
      "emotion": EMOTIONS[emotion_index],
      "confidence": round(confidence * 100, 2),
  }
