document.getElementById('imageUpload').addEventListener('change', handleImageUpload);
document.getElementById('predictButton').addEventListener('click', predictDisease);

let model;
async function loadModel() {
    model = await mobilenet.load();
    console.log('Model loaded');
}

loadModel();

function handleImageUpload(event) {
    const imageContainer = document.getElementById('imageContainer');
    imageContainer.innerHTML = '';
    const file = event.target.files[0];
    if (file) {
        const img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        imageContainer.appendChild(img);
    }
}

async function predictDisease() {
    const imageElement = document.querySelector('#imageContainer img');
    if (!imageElement) {
        alert('Please upload an image first.');
        return;
    }
    if (!model) {
        alert('Model is not yet loaded.');
        return;
    }
    const predictions = await model.classify(imageElement);
    displayPrediction(predictions);
}


function displayPrediction(predictions) {
    const predictionResult = document.getElementById('predictionResult');
    predictionResult.innerHTML = '';
    predictions.forEach(prediction => {
        const p = document.createElement('p');
        p.innerText = `${prediction.className}: ${Math.round(prediction.probability * 100)}%`;
        predictionResult.appendChild(p);
    });
}