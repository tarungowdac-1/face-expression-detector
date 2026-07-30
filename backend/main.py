from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.emotion import predict_emotion


app = FastAPI(
    title="Face Emotion Detector API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "message": "Emotion Detector API Running"
    }



@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    image_bytes = await file.read()

    result = predict_emotion(
        image_bytes
    )

    return result
