let mediaRecorder;
let recordedChunks = [];

function startRecording() {
    // Access the user's camera
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(function(stream) {
        const videoElement = document.getElementById('videoElement');
        videoElement.srcObject = stream;

        // Create a new MediaRecorder to record the stream
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = function(event) {
            recordedChunks.push(event.data);
        };

        mediaRecorder.onstop = function() {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            const url = URL.createObjectURL(blob);
            const downloadLink = document.getElementById('downloadLink');
            downloadLink.href = url;
            downloadLink.style.display = 'inline'; // Show the download link
            downloadLink.download = 'demo_interview.webm';
        };

        // Start recording
        mediaRecorder.start();
    }).catch(function(error) {
        console.error('Error accessing camera and microphone:', error);
    });
}

function stopRecording() {
    // Stop the recording and save the video
    if (mediaRecorder) {
        mediaRecorder.stop();
    }
}
