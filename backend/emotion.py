import os
import cv2
import numpy as np
import tensorflow as tf


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "emotion_model.keras"
)


EMOTIONS = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]


model = tf.keras.models.load_model(MODEL_PATH)


def predict_emotion(image_bytes):

    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    frame = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    if frame is None:
        return {
            "error": "Invalid image"
        }


    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    face = cv2.resize(
        gray,
        (48,48)
    )


    face = face / 255.0


    face = np.expand_dims(
        face,
        axis=0
    )


    face = np.expand_dims(
        face,
        axis=-1
    )


    prediction = model.predict(
        face,
        verbose=0
    )


    emotion_index = np.argmax(
        prediction
    )


    confidence = float(
        np.max(prediction)
    )


    return {
        "emotion": EMOTIONS[emotion_index],
        "confidence": round(confidence * 100, 2)
    }
