
# HTML/JavaScript code from the previous step
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Microphone Recording</title>
</head>
<body>

<button id="recordButton">Start Recording</button>

<script>
    let mediaRecorder;
    let audioChunks = [];

    async function startRecording() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play();

            console.log(audioBlob);
            // Here you can upload the blob to your server or process it further
        };

        mediaRecorder.start();
        audioChunks = [];
        document.getElementById("recordButton").innerText = "Stop Recording";
    }

    function stopRecording() {
        mediaRecorder.stop();
        document.getElementById("recordButton").innerText = "Start Recording";
    }

    document.getElementById("recordButton").addEventListener("click", () => {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            stopRecording();
        } else {
            startRecording();
        }
    });
</script>

</body>
</html>
"""

# Use the Streamlit components.html function to embed the HTML code
components.html(html_code, height=100)

