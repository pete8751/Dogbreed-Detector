class model_strategy:
    def __init__(self, concrete_model):
        self.concrete_model = concrete_model

    def load(self):
        self.concrete_model.load_model()

    def preprocess_input(self, input_data):
        return self.concrete_model.preprocess_input(input_data)

    def predict(self, input_data):
        return self.concrete_model.predict(input_data)
        


