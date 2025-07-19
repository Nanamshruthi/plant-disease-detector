import os
import numpy as np
from keras.models import load_model
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image
from flask import send_from_directory



app = Flask(__name__)

# Load your model
model =load_model('model.h5')
print('Model loaded. Check http://127.0.0.1:5000/')

# Disease labels and additional information
disease_info = {
    0: {
        'name': 'Healthy',
        'confidence': 0,
        'recommendation': 'The plant appears to be healthy. Maintain current care routine.'
    },
    1: {
        'name': 'Powdery Mildew',
        'confidence': 0,
        'recommendation': 'Apply fungicides like sulfur or potassium bicarbonate. Improve air circulation and avoid overhead watering.'
    },
    2: {
        'name': 'Rust',
        'confidence': 0,
        'recommendation': 'Remove infected leaves. Apply fungicides containing chlorothalonil or mancozeb. Avoid wetting foliage when watering.'
    }
}

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def getResult(image_path):
    img = load_img(image_path, target_size=(225, 225))
    x = img_to_array(img)
    x = x.astype('float32') / 255.
    x = np.expand_dims(x, axis=0)
    predictions = model.predict(x)[0]
    return predictions

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Get prediction
            predictions = getResult(file_path)
            predicted_class = np.argmax(predictions)
            confidence = float(predictions[predicted_class]) * 100
            
            # Prepare response
            response = {
                'status': 'success',
                'prediction': disease_info[predicted_class]['name'],
                'confidence': f"{confidence:.2f}%",
                'recommendation': disease_info[predicted_class]['recommendation'],
                'image_url': f"/uploads/{filename}"
            }
            
            return jsonify(response)
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
