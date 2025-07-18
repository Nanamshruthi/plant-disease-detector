import os
import numpy as np
from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image
import gdown

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config.update(
    UPLOAD_FOLDER='uploads',
    ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif', 'webp'},
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB
    MODEL_PATH='model.h5'
)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Download model if not present (Google Drive)
if not os.path.exists(app.config['MODEL_PATH']):
    print("⏳ Downloading model from Google Drive...")
    try:
        gdown.download(
            'https://drive.google.com/uc?id=1GFbmdxkKRakJAUWdaQbdK3le9p-6X_BM',
            app.config['MODEL_PATH'],
            quiet=False
        )
        print("✅ Model downloaded successfully!")
    except Exception as e:
        print(f"❌ Model download failed: {str(e)}")
        raise

# Load model
try:
    model = load_model(app.config['MODEL_PATH'])
    print("🚀 Model loaded successfully!")
except Exception as e:
    print(f"❌ Model loading failed: {str(e)}")
    raise

# Disease information
DISEASE_INFO = {
    0: {
        'name': 'Healthy',
        'recommendation': 'The plant appears healthy. Maintain current care routine.'
    },
    1: {
        'name': 'Powdery Mildew',
        'recommendation': 'Apply sulfur-based fungicides weekly. Improve air circulation.'
    },
    2: {
        'name': 'Rust',
        'recommendation': 'Remove infected leaves. Use chlorothalonil fungicides.'
    }
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def predict_disease(image_path):
    """Process image and return predictions"""
    img = Image.open(image_path).convert('RGB').resize((225, 225))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)[0]
    return predictions

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def handle_prediction():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': f'Allowed formats: {app.config["ALLOWED_EXTENSIONS"]}'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get prediction
        predictions = predict_disease(filepath)
        class_id = np.argmax(predictions)
        confidence = float(predictions[class_id]) * 100
        
        return jsonify({
            'status': 'success',
            'prediction': DISEASE_INFO[class_id]['name'],
            'confidence': f"{confidence:.2f}%",
            'recommendation': DISEASE_INFO[class_id]['recommendation'],
            'image_url': f"/uploads/{filename}"
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
