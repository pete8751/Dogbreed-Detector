from flask import Flask, request, jsonify
import base64
import re
from flask_cors import CORS
import requests
from dog_model import DogModel
from models_util import model_strategy, process_img_data
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app, resources={r"/analyze_image": {"origins": "http://localhost:3000"}})
loaded = False
model = model_strategy(DogModel("flask_backend\dog_model.py"))

def load():
    global loaded  # Declare 'loaded' as a global variable
    model.load()
    loaded = True
    print("Model loaded")
load()

@app.route('/')
# #handle preflight request
@app.route('/analyze_image/', methods=['OPTIONS'])
def handle_options():
    return '', 200, {
        'Access-Control-Allow-Origin': 'http://localhost:3000',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

@app.route('/analyze_image', methods=['POST'])

def analyze_image():
    print("recieved")
    try:
        data = request.get_json()
        image_url = data.get('imageUrl')
        print(image_url)
        if not image_url:
            return jsonify({'error': 'Image URL is missing'}), 400
        image_data = None
        print('1')
        if image_url.startswith('blob:'):
            # Extract base64-encoded image data from the URL
            image_data_match = re.search(r'blob:(.+)', image_url)
            if image_data_match:
                image_data_base64 = image_data_match.group(1)
                # Decode the base64-encoded image data
                image_data = base64.b64decode(image_data_base64)
                print("2")
            else:
                return jsonify({'error': 'Invalid blob URL'}), 400
        else:
            response = requests.get(image_url)
            if response.status_code != 200:
                return jsonify({'error': 'Failed to download image'}), 500
            image_data = response.content
        print("3")
        # Process the image in-memory
        try:
            print("Image Data:", image_data[:50])
            image = Image.open(BytesIO(image_data));
            print("Image opened successfully")
        except Exception as e:
            print(f'Error opening image: {str(e)}')
            return jsonify({'error': f'Error opening image: {str(e)}'}), 500

        image, form, width, height = process_img_data(image_data);
        print("7")
        # Check image format
        allowed_formats = {'JPEG', 'PNG'}
        if form not in allowed_formats:
            return jsonify({'error': f'Unsupported image format: {form}'}), 400
        # print("8")
        # Check image dimensions
        max_width = 1920  # Adjust the maximum width as needed
        max_height = 1080  # Adjust the maximum height as needed
        if width > max_width or height > max_height:
            return jsonify({'error': f'Image dimensions exceed the allowed limits ({max_width}x{max_height})'}), 400
        
        pre_processed_image = model.preprocess_input(image)
        # print("9")
        prediction = model.predict(pre_processed_image)
        # print("10")
        return jsonify({'success': 'Image analyzed successfully', 'Prediction': prediction}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
