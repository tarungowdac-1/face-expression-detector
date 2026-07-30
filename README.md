# 🧠 AI Real-Time Face Emotion Detector

A full-stack, end-to-end Computer Vision web application that detects human facial emotions in real-time using Deep Learning. The core neural network was trained on Google Colab using TensorFlow/Keras, wrapped in a low-latency FastAPI backend on Render, and connected to a responsive web UI hosted on Vercel.

---

## 📌 Project Overview

Understanding facial expressions in real-time is a fundamental problem in computer vision with applications in user experience analysis, mental health monitoring, and interactive AI applications.

This project bridges the gap between machine learning model development and web deployment:
1. **Model Training & Experimentation:** Leveraging cloud GPU resources on Google Colab to process large image datasets, train Convolutional Neural Networks (CNNs), and export optimized inference weights.
2. **Backend API Engineering:** Converting the saved model into a lightweight REST API using FastAPI that receives video frames as binary image payloads and returns real-time emotion classifications with confidence scores.
3. **Frontend Integration:** Building an asynchronous HTML5/JavaScript application that captures camera streams via WebRTC, compresses frames on the fly using the Canvas API, and renders real-time prediction overlays without blocking the user interface.

---

## 📊 Dataset & Model Training (Google Colab)

The neural network model was trained using **Google Colab** to utilize free GPU hardware acceleration for efficient backpropagation and parameter tuning.

### Dataset
- **Dataset:** [FER2013 / Facial Expression Recognition Dataset](https://www.kaggle.com/datasets/msambare/fer2013/data)
- **Target Classes (7 Core Emotions):** *Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise*
- **Format:** $48 \times 48$ grayscale facial images.

### Training Pipeline (`train.py`)
- **Preprocessing:** Rescaling, normalization, and data augmentation (random flips, rotations, and zooms) to improve generalization.
- **Architecture:** Convolutional Neural Network (CNN) with Batch Normalization, ReLU activations, Dropout layers for regularization, and Softmax output.
- **Optimization:** Trained using the Adam optimizer with Sparse Categorical Cross-Entropy loss.
- **Export:** Saved the trained model architecture and weights (`.h5` / `.keras`) inside the `models/` folder for deployment inference.

---

## ✨ Features

- **Real-Time Detection:** Captures webcam frames dynamically directly from the browser.
- **Deep Learning Inference:** Accurately classifies facial expressions into 7 distinct emotion categories.
- **FastAPI REST API:** Low-latency API endpoint handling image frame payloads.
- **Optimized Frontend Fetch Loop:** Asynchronous fetch queue using `setTimeout` callbacks to prevent network congestion, request stacking, and server rate-limiting.
- **Decoupled Architecture:** Clean separation of frontend UI, backend API, and ML pipeline.

---

## 🛠️ Tech Stack

- **Machine Learning & Data Science:** Python, TensorFlow / Keras, OpenCV, MediaPipe, NumPy, Pandas, Matplotlib, Scikit-learn
- **Model Training Environment:** Google Colab (GPU-accelerated)
- **Backend Framework:** FastAPI, Uvicorn, Gunicorn, `python-multipart`
- **Frontend UI:** HTML5, CSS3, JavaScript (WebRTC Canvas API)
- **Deployment Cloud Platforms:** Render (Backend), Vercel (Frontend)

---

## 📁 Repository Structure

```text
├── backend/
│   ├── app.py / main.py   # FastAPI server entry point
│   ├── emotion.py         # Image preprocessing & model inference script
│   └── requirements.txt   # Backend dependencies
├── frontend/
│   ├── index.html         # Web UI layout
│   ├── script.js          # Webcam capture & asynchronous API fetch logic
│   └── style.css          # UI styling & dynamic confidence bar
├── models/                # Saved trained model weights (.h5 / .keras)
├── src/ / scripts/        # Training scripts & local real-time testing
└── README.md              # Project documentation

```

---

## ⚙️ Local Development Setup

### 1. Clone the Repository

```bash
git clone [https://github.com/tarungowdac-1/face-expression-detector.git](https://github.com/tarungowdac-1/face-expression-detector.git)
cd face-expression-detector

```

### 2. Set Up Backend

```bash
cd backend
python -m venv venv
# Activate virtual environment:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload

```

The backend API will run locally at `http://127.0.0.1:8000`.

### 3. Set Up Frontend

1. Open `frontend/script.js` and set `API_URL` to `http://127.0.0.1:8000/predict`.
2. Open `frontend/index.html` in your web browser.

---

## 📡 API Reference

### `POST /predict`

Accepts an image frame via `multipart/form-data` and returns the predicted emotion with confidence metrics.

**Request:**

* Body: `FormData` containing key `"file"` (image binary blob)

**Response:**

```json
{
  "emotion": "Happy",
  "confidence": 94.5
}

```
