from flask import Flask, request, jsonify
from flask_cors import CORS
from dog_model import DogModel
from models_util import model_strategy, process_img_data


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
         # Access the uploaded file
        file = request.files['file']

        # # Access other form data
        # image_url = request.form.get('imageUrl')
    
        # Process the image in-memory
        print("1")
        print(file)

        image, form, width, height = process_img_data(file)
        print(image)
        print(form)
        print(width)
        print(height)

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
        prediction = model.predict(pre_processed_image)

        return jsonify({'success': 'Image analyzed successfully', 'Prediction': prediction}), 200

    except Exception as e:
        print(e);
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
