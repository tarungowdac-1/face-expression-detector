import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "emotion_model.keras"
)


IMAGE_SIZE = 48


EMOTIONS = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]


CAMERA_INDEX = 0