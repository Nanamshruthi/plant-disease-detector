from flask import Flask, request, jsonify
import os
import random
from datetime import datetime

app = Flask(__name__)

# Mock disease data
DISEASE_INFO = {
    'healthy': {
        'name': 'Healthy Plant',
        'treatment': 'Your plant appears healthy! No treatment needed.',
        'confidence': random.uniform(90, 99)
    },
    'powdery_mildew': {
        'name': 'Powdery Mildew',
        'treatment': '1. Apply sulfur or potassium bicarbonate\n2. Improve air circulation\n3. Remove affected leaves',
        'confidence': random.uniform(80, 95)
    },
    'leaf_spot': {
        'name': 'Leaf Spot',
        'treatment': '1. Apply copper-based fungicide\n2. Water at the base only\n3. Remove infected leaves',
        'confidence': random.uniform(75, 90)
    }
}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Get a random disease for demonstration
    disease_key = random.choice(list(DISEASE_INFO.keys()))
    disease_data = DISEASE_INFO[disease_key]
    
    return jsonify({
        'disease': disease_data['name'],
        'confidence': f"{disease_data['confidence']:.1f}%",
        'treatment': disease_data['treatment'],
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
