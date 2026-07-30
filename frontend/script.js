const video = document.getElementById("video");
const overlay = document.getElementById("overlay");
const toggleCamBtn = document.getElementById("toggleCamBtn");
const switchCamBtn = document.getElementById("switchCamBtn");

const emojiIcon = document.getElementById("emojiIcon");
const emojiDisplay = document.getElementById("emojiDisplay");
const emotionTitle = document.getElementById("emotionTitle");
const confidenceValue = document.getElementById("confidenceValue");
const progressBar = document.getElementById("progressBar");

const API_URL = "https://face-expression-detector.onrender.com/predict";

let currentStream = null;
let isCamActive = false;
let facingMode = "user"; // 'user' (front) or 'environment' (back)

const icons = {
  Happy: "😊",
  Sad: "😢",
  Angry: "😡",
  Fear: "😨",
  Surprise: "😮",
  Neutral: "😐",
  Disgust: "🤢"
};

// Start or Stop Camera
async function startCamera() {
  if (currentStream) {
    currentStream.getTracks().forEach((track) => track.stop());
  }

  try {
    currentStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: facingMode, width: { ideal: 640 }, height: { ideal: 480 } }
    });
    video.srcObject = currentStream;
    isCamActive = true;
    overlay.classList.remove("active");
    sendFrame();
  } catch (err) {
    console.error("Camera access failed:", err);
    overlay.classList.add("active");
    isCamActive = false;
  }
}

function stopCamera() {
  if (currentStream) {
    currentStream.getTracks().forEach((track) => track.stop());
  }
  isCamActive = false;
  overlay.classList.add("active");
}

toggleCamBtn.addEventListener("click", () => {
  if (isCamActive) {
    stopCamera();
  } else {
    startCamera();
  }
});

switchCamBtn.addEventListener("click", () => {
  facingMode = facingMode === "user" ? "environment" : "user";
  if (isCamActive) {
    startCamera();
  }
});

// Canvas Setup
const canvas = document.createElement("canvas");
const context = canvas.getContext("2d");

function sendFrame() {
  if (!isCamActive) return;

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
        .then((res) => res.json())
        .then((data) => {
          if (data.emotion && isCamActive) {
            updateUI(data.emotion, data.confidence);
          }
        })
        .catch((err) => console.error("API error:", err))
        .finally(() => {
          if (isCamActive) setTimeout(sendFrame, 800);
        });
    }, "image/jpeg", 0.85);
  } else {
    setTimeout(sendFrame, 300);
  }
}

function updateUI(emotion, confidence) {
  const emoji = icons[emotion] || "😐";

  if (emotionTitle.innerText !== emotion) {
    emojiDisplay.classList.add("bounce");
    setTimeout(() => emojiDisplay.classList.remove("bounce"), 300);
  }

  emojiIcon.innerText = emoji;
  emotionTitle.innerText = emotion;
  confidenceValue.innerText = `${confidence}%`;
  progressBar.style.width = `${confidence}%`;
}

// Auto-start on launch
startCamera();
