import os
import cv2
import numpy as np
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "emotion_model.keras")

EMOTIONS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# 1. Load your Keras CNN model
model = tf.keras.models.load_model(MODEL_PATH)

# 2. Load OpenCV's built-in face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def predict_emotion(image_bytes):
  # Convert bytes to image
  np_array = np.frombuffer(image_bytes, np.uint8)
  frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

  if frame is None:
    return {"error": "Invalid image"}

  # Convert full frame to grayscale
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # Detect faces in the frame
  faces = face_cascade.detectMultiScale(
      gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
  )

  # Fallback: If no face detected, fall back to center/full crop
  if len(faces) == 0:
    face_roi = gray
  else:
    # Get the bounding box of the largest face detected
    x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
    face_roi = gray[y : y + h, x : x + w]

  # Resize ONLY the cropped face ROI to 48x48
  face = cv2.resize(face_roi, (48, 48))

  # Normalize pixels (0.0 to 1.0)
  face = face / 255.0

  # Reshape to match model input (1, 48, 48, 1)
  face = np.expand_dims(face, axis=0)
  face = np.expand_dims(face, axis=-1)

  # Make prediction
  prediction = model.predict(face, verbose=0)
  emotion_index = np.argmax(prediction)
  confidence = float(np.max(prediction))

  return {
      "emotion": EMOTIONS[emotion_index],
      "confidence": round(confidence * 100, 2),
  }
