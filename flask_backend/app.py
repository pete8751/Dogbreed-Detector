from flask import Flask, request, jsonify
import requests
from io import BytesIO
from PIL import Image
from dog_model import DogModel
from models_util import model_strategy, process_img_data

app = Flask(__name__)
loaded = False
model = model_strategy(DogModel("path/to/model"))

def load():
    global loaded  # Declare 'loaded' as a global variable
    model.load_model()
    loaded = True
    print("Model loaded")

load()

@app.route('/')

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    try:
        data = request.get_json()
        image_url = data.get('imageUrl')

        if not image_url:
            return jsonify({'error': 'Image URL is missing'}), 400

        # Download the image from the URL
        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to download image'}), 500

        # Process the image in-memory
        image, form, width, height = process_img_data(response.content);

        # Check image format
        allowed_formats = {'JPEG', 'PNG'}
        if form not in allowed_formats:
            return jsonify({'error': f'Unsupported image format: {form}'}), 400

        # Check image dimensions
        max_width = 1920  # Adjust the maximum width as needed
        max_height = 1080  # Adjust the maximum height as needed
        if width > max_width or height > max_height:
            return jsonify({'error': f'Image dimensions exceed the allowed limits ({max_width}x{max_height})'}), 400
        
        pre_processed_image = model.preprocess_input(image)
        prediction = model.predict(pre_processed_image)
        return jsonify({'success': 'Image analyzed successfully', 'Prediction': prediction}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

app = Flask(__name__)









if __name__ == '__main__':
    app.run(debug=True)
