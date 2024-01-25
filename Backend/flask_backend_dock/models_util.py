from PIL import Image

class model_strategy:
    def __init__(self, concrete_model):
        self.concrete_model = concrete_model

    def load(self):
        self.concrete_model.load_model()

    def preprocess_input(self, input_data):
        return self.concrete_model.preprocess_input(input_data)

    def predict(self, input_data):
        return self.concrete_model.predict(input_data)
    
    def evaluate(self, input_data):
        processed_data = self.preprocess_input(input_data);
        evaluation = self.predict(processed_data);
        return evaluation;

    def execute(self, input_data):
        return self.concrete_model.execute(input_data)
def process_img_data(file):
    content = Image.open(file);
    if content.mode != 'RGB':
        content = content.convert('RGB');
    return content, content.format, content.size[0], content.size[1]

