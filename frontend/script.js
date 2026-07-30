const video = document.getElementById("video");
const emotionText = document.getElementById("emotion");
const confidenceText = document.getElementById("confidence");
const bar = document.getElementById("bar");

// Backend API Endpoint
const API_URL = "https://face-expression-detector.onrender.com/predict";

// Start webcam stream
navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
    // Start processing loop once webcam starts
    sendFrame();
  })
  .catch((error) => {
    console.error("Camera access error:", error);
  });

// Create invisible canvas for capturing frames
const canvas = document.createElement("canvas");
const context = canvas.getContext("2d");

// Emotion emoji mapping
const icons = {
  Happy: "😊",
  Sad: "😢",
  Angry: "😡",
  Fear: "😨",
  Surprise: "😮",
  Neutral: "😐",
  Disgust: "🤢"
};

function sendFrame() {
  if (video.readyState === video.HAVE_ENOUGH_DATA) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      let formData = new FormData();
      formData.append("file", blob, "frame.jpg");

      fetch(API_URL, {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          if (data.emotion) {
            const emoji = icons[data.emotion] || "😐";
            emotionText.innerHTML = `${emoji} ${data.emotion}`;
            confidenceText.innerHTML = `Confidence: ${data.confidence}%`;
            bar.style.width = `${data.confidence}%`;
          }
        })
        .catch((error) => {
          console.error("Prediction error:", error);
        })
        .finally(() => {
          // Send next frame 1 second AFTER previous request finishes
          setTimeout(sendFrame, 1000);
        });
    }, "image/jpeg", 0.7); // 0.7 compression speeds up network upload!
  } else {
    // Retry in 500ms if video frame isn't ready yet
    setTimeout(sendFrame, 500);
  }
}
