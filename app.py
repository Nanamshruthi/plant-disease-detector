import os
from flask import Flask
from keras.models import load_model
import gdown

app = Flask(__name__)

# Configuration
app.config['MODEL_PATH'] = os.path.join(os.path.dirname(__file__), 'model.h5')

def initialize_model():
    """Load or download the model with proper error handling"""
    model_path = app.config['MODEL_PATH']
    
    # Debugging information
    print("\n=== Debugging Information ===")
    print("Current directory:", os.getcwd())
    print("Directory contents:", os.listdir())
    print("Full model path:", os.path.abspath(model_path))
    
    # Try to load existing model first
    if os.path.exists(model_path):
        print(f"Found existing model at {model_path}")
        try:
            return load_model(model_path)
        except Exception as e:
            print(f"Error loading existing model: {e}")
            os.remove(model_path)  # Remove corrupted file
            print("Removed potentially corrupted model file")
    
    # Download from Google Drive if not found locally
    print("Attempting to download model...")
    try:
        # Make sure your Google Drive file is shared as "Anyone with the link"
        file_id = '1GFbmdxkKRakJAUWdaQbdK3le9p-6X_BM'  # REPLACE WITH YOUR ACTUAL FILE ID
        gdown.download(
            f'https://drive.google.com/uc?id={file_id}',
            model_path,
            quiet=False
        )
        
        # Verify download
        if not os.path.exists(model_path):
            raise RuntimeError("Download completed but file not created")
            
        print(f"Model successfully downloaded to {model_path}")
        return load_model(model_path)
        
    except Exception as e:
        print(f"\n❌ Critical Error: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Verify the Google Drive file ID is correct")
        print("2. Ensure the file is shared as 'Anyone with the link'")
        print("3. Check your internet connection")
        print("4. For production, consider bundling model.h5 with your deployment")
        raise

# Initialize model when starting the app
try:
    model = initialize_model()
    print("✅ Model successfully loaded!")
except Exception as e:
    print(f"❌ Failed to initialize model: {e}")
    # You might want to exit here if your app can't run without the model
    # import sys; sys.exit(1)

@app.route('/')
def home():
    return "Model loading application is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
