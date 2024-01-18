from flask import Flask
from dog_model import DogModel
from models_util import model_strategy

app = Flask(__name__)

model = model_strategy(DogModel("path/to/model"))

@app.route('/')

def home():
    return 'Hello, World!'

def load_model():
    model.load()

def to_png(image):
    return image

def preprocess_input(input_data):
    return model.preprocess_input(input_data)

def predict(input_data):
    return model.predict(input_data)












if __name__ == '__main__':
    app.run(debug=True)
