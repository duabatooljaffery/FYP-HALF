document.getElementById('classifyButton').addEventListener('click', function () {
    const formData = new FormData();
    const imageInput = document.getElementById('imageInput');

    if (!imageInput.files.length) {
        alert("Please upload an image.");
        return;
    }

    formData.append('image', imageInput.files[0]);

    fetch('http://127.0.0.1:5000/classify', { // Flask API endpoint
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            const resultDiv = document.getElementById('result');
            document.getElementById('classificationResult').innerText = `Full Classification Result: ${JSON.stringify(data.result)}`;
            document.getElementById('dominantShape').innerText = `Dominant Shape: ${data.dominant_shape}`;
            document.getElementById('dominantScore').innerText = `Score: ${data.score.toFixed(2)}`;
            document.getElementById('beardSuggestion').innerText = `Beard Suggestion: ${data.beard_suggestion}`;
            document.getElementById('hairstyleSuggestion').innerText = `Hairstyle Suggestion: ${data.hairstyle_suggestion}`;
            resultDiv.style.display = 'block';
        }
    })
    .catch(error => console.error('Error:', error));
});
