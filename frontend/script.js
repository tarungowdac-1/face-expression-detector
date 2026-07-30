const video = document.getElementById("video");

const emotionText = document.getElementById("emotion");

const confidenceText = document.getElementById("confidence");

const bar = document.getElementById("bar");


// Backend API
const API_URL = "http://127.0.0.1:8000/predict";


// Start webcam

navigator.mediaDevices
.getUserMedia({
    video: true
})
.then(stream => {

    video.srcObject = stream;

})
.catch(error => {

    console.log("Camera error:", error);

});



// Create canvas for screenshots

const canvas = document.createElement("canvas");

const context = canvas.getContext("2d");



// Send frame every 1 second

setInterval(() => {


    if(video.readyState === video.HAVE_ENOUGH_DATA){


        canvas.width = video.videoWidth;

        canvas.height = video.videoHeight;


        context.drawImage(
            video,
            0,
            0,
            canvas.width,
            canvas.height
        );


        canvas.toBlob(blob => {


            let formData = new FormData();


            formData.append(
                "file",
                blob,
                "frame.jpg"
            );



            fetch(
                API_URL,
                {
                    method:"POST",
                    body:formData
                }
            )

            .then(response => response.json())

            .then(data => {


                if(data.emotion){


                   const icons = {

    "Happy":"😊",
    "Sad":"😢",
    "Angry":"😡",
    "Fear":"😨",
    "Surprise":"😮",
    "Neutral":"😐",
    "Disgust":"🤢"

};


emotionText.innerHTML =
icons[data.emotion] + " " + data.emotion;


                    confidenceText.innerHTML =
                    "Confidence: "
                    + data.confidence
                    + "%";



                    bar.style.width =
                    data.confidence + "%";


                }


            })

            .catch(error => {

                console.log(error);

            });


        },
        "image/jpeg");


    }


},1000);
