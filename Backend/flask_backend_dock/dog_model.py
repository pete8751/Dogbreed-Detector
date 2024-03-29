import os
from model_processing_adt import ModelADT
from tflite_runtime.interpreter import Interpreter
import numpy as np
import cv2
    

# List of dog breeds
dog_breeds = [
    "Chihuahua", "Japanese Spaniel", "Maltese Dog", "Pekinese", "Shih-Tzu", 
    "Blenheim Spaniel", "Papillon", "Toy Terrier", "Rhodesian Ridgeback", 
    "Afghan Hound", "Basset", "Beagle", "Bloodhound", "Bluetick", 
    "Black-And-Tan Coonhound", "Walker Hound", "English Foxhound", "Redbone", 
    "Borzoi", "Irish Wolfhound", "Italian Greyhound", "Whippet", "Ibizan Hound", 
    "Norwegian Elkhound", "Otterhound", "Saluki", "Scottish Deerhound", 
    "Weimaraner", "Staffordshire Bullterrier", "American Staffordshire Terrier", 
    "Bedlington Terrier", "Border Terrier", "Kerry Blue Terrier", "Irish Terrier", 
    "Norfolk Terrier", "Norwich Terrier", "Yorkshire Terrier", 
    "Wire-Haired Fox Terrier", "Lakeland Terrier", "Sealyham Terrier", "Airedale", 
    "Cairn", "Australian Terrier", "Dandie Dinmont", "Boston Bull", 
    "Miniature Schnauzer", "Giant Schnauzer", "Standard Schnauzer", 
    "Scotch Terrier", "Tibetan Terrier", "Silky Terrier", 
    "Soft-Coated Wheaten Terrier", "West Highland White Terrier", "Lhasa", 
    "Flat-Coated Retriever", "Curly-Coated Retriever", "Golden Retriever", 
    "Labrador Retriever", "Chesapeake Bay Retriever", "German Short-Haired Pointer", 
    "Vizsla", "English Setter", "Irish Setter", "Gordon Setter", 
    "Brittany Spaniel", "Clumber", "English Springer", "Welsh Springer Spaniel", 
    "Cocker Spaniel", "Sussex Spaniel", "Irish Water Spaniel", "Kuvasz", 
    "Schipperke", "Groenendael", "Malinois", "Briard", "Kelpie", 
    "Komondor", "Old English Sheepdog", "Shetland Sheepdog", "Collie", 
    "Border Collie", "Bouvier Des Flandres", "Rottweiler", "German Shepherd", 
    "Doberman", "Miniature Pinscher", "Greater Swiss Mountain Dog", 
    "Bernese Mountain Dog", "Appenzeller", "Entlebucher", "Boxer", 
    "Bull Mastiff", "Tibetan Mastiff", "French Bulldog", "Great Dane", 
    "Saint Bernard", "Eskimo Dog", "Malamute", "Siberian Husky", 
    "Affenpinscher", "Basenji", "Pug", "Leonberg", "Newfoundland", 
    "Great Pyrenees", "Samoyed", "Pomeranian", "Chow", "Keeshond", 
    "Brabancon Griffon", "Pembroke", "Cardigan", "Toy Poodle", 
    "Miniature Poodle", "Standard Poodle", "Mexican Hairless", "Dingo", 
    "Dhole", "African Hunting Dog"
]

# Model Path
relative_path = 'model_files/quantized_model.tflite'
local_model_path = os.path.abspath(relative_path)

class DogModel(ModelADT):
    def __init__(self, model_path):
        # Call the constructor of the parent class (ModelADT)
        super().__init__(model_path)

    def load_model(self):
        # Specific implementation for loading a dog-related model
        print(f"Loading dog model from: {self.model_path}")
        try:
            self.loaded_model = Interpreter(model_path=local_model_path)
            self.loaded_model.allocate_tensors()
            print("success:")
        except Exception as e:
            print('model_files/quantized_model.tflite')
            print(local_model_path)
            print(e)
            return e

    def preprocess_input(self, input_data):
        # input_data will be image object obtained from PIL.Image.open().
        image_array = np.array(input_data)

        target_size = (299, 299);  
        resized_image_array = cv2.resize(image_array, target_size)

        # preprocessed_data = xception_preprocess_input(resized_image_array)
        resized_image_array = resized_image_array.astype('float32')
        resized_image_array /= 127.5
        resized_image_array -= 1

        batch_output = np.expand_dims(resized_image_array, axis=0)
        print(batch_output.shape)
        # I might need to add a dimension to the image array to make it compatible with the model.
        return batch_output

    def predict(self, input_data):
        # Specific implementation for predicting dog breed (input_data should be preprocessed first)
        if self.loaded_model is None:
            raise ValueError("Dog model not loaded. Call load_model first.")
        
        # Specific implementation for predicting dog breed
        print("Predicting dog breed")
        # Replace the following line with the actual prediction logic for a dog model
        # For example, if using a specific dog model's predict method:
        # dog_breed_predictions = self.loaded_model.predict(input_data)
        input_tensor_index = self.loaded_model.get_input_details()[0]['index']
        self.loaded_model.set_tensor(input_tensor_index, input_data)
        self.loaded_model.invoke()
        output_tensor_index = self.loaded_model.get_output_details()[0]['index']
        print(output_tensor_index)
        dog_breed_predictions = self.loaded_model.get_tensor(output_tensor_index)
        # print(dog_breed_predictions)
        # Get the top 5 predicted classes and their probabilities
        top5_classes = np.argsort(dog_breed_predictions[0])[-5:][::-1]
        top5_probabilities = dog_breed_predictions[0][top5_classes]

        # Extract the breed names for the top 5 classes
        top5_breeds = [dog_breeds[i] for i in top5_classes]
        #zip into tuples.
        prediction_pairs = zip(top5_breeds, top5_probabilities)
        predictions = [{"breed": breed, "probability": float(prob)} for breed, prob in prediction_pairs]
        return predictions

    def execute(self, input_data):
        # creating model
        model = Interpreter(model_path=local_model_path)
        model.allocate_tensors()
        # processing data
        image_array = np.array(input_data)

        target_size = (299, 299);  
        resized_image_array = cv2.resize(image_array, target_size)

        # preprocessed_data = xception_preprocess_input(resized_image_array)
        resized_image_array = resized_image_array.astype('float32')
        resized_image_array /= 127.5
        resized_image_array -= 1

        processed_data = np.expand_dims(resized_image_array, axis=0)
        
        if model is None:
            raise ValueError("Dog model not loaded. Call load_model first.")
        
        # Specific implementation for predicting dog breed
        print("Predicting dog breed")
        
        input_tensor_index = model.get_input_details()[0]['index']
        model.set_tensor(input_tensor_index, processed_data)
        model.invoke()
        output_tensor_index = model.get_output_details()[0]['index']
        print(output_tensor_index)
        dog_breed_predictions = model.get_tensor(output_tensor_index)

        model = 0
        # Get the top 5 predicted classes and their probabilities
        top5_classes = np.argsort(dog_breed_predictions[0])[-5:][::-1]
        top5_probabilities = dog_breed_predictions[0][top5_classes]

        # Extract the breed names for the top 5 classes
        top5_breeds = [dog_breeds[i] for i in top5_classes]
        #zip into tuples.
        prediction_pairs = zip(top5_breeds, top5_probabilities)
        predictions = [{"breed": breed, "probability": float(prob)} for breed, prob in prediction_pairs]
        return predictions