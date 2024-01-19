from model_processing_adt import ModelADT
from tensorflow.keras import layers, models, applications
from keras.applications.xception import preprocess_input
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
model_path = "./model_files"

class DogModel(ModelADT):
    def __init__(self, model_path):
        # Call the constructor of the parent class (ModelADT)
        super().__init__(model_path)

    def load_model(self):
        # Specific implementation for loading a dog-related model
        print(f"Loading dog model from: {self.model_path}")
        base_model = applications.Xception(
        input_shape=(299, 299, 3),
        include_top=False,
        weights="imagenet",
        pooling=None,  # Global average pooling for flattening
        )

        model = models.Sequential()
        model.add(base_model)
        model.layers[0].trainable = False
        model.add(layers.Flatten())
        model.add(layers.Dense(256, activation='relu'))
        model.add(layers.BatchNormalization())
        model.add(layers.Dense(256, activation='relu'))
        model.add(layers.Dropout(0.3))
        model.add(layers.BatchNormalization())
        model.add(layers.Dense(120, activation='softmax'))
        model.load_weights(r"model_files\best_full_weights.h5")
        self.loaded_model = model

    def preprocess_input(self, input_data):
        # input_data will be image object obtained from PIL.Image.open().
        image_array = np.array(input_data)
        target_size = (300, 300);  
        resized_image_array = cv2.resize(image_array, target_size)
        preprocessed_data = preprocess_input(resized_image_array)

        # I might need to add a dimension to the image array to make it compatible with the model.
        return preprocessed_data

    def predict_dog_breed(self, input_data):
        # Specific implementation for predicting dog breed (input_data should be preprocessed first)
        if self.loaded_model is None:
            raise ValueError("Dog model not loaded. Call load_model first.")
        
        # Specific implementation for predicting dog breed
        print("Predicting dog breed")
        # Replace the following line with the actual prediction logic for a dog model
        # For example, if using a specific dog model's predict method:
        dog_breed_predictions = self.loaded_model.predict(input_data)

        # Get the top 5 predicted classes and their probabilities
        top5_classes = np.argsort(dog_breed_predictions)[-5:][::-1]
        top5_probabilities = dog_breed_predictions[top5_classes]

        # Extract the breed names for the top 5 classes
        top5_breeds = [dog_breeds[i] for i in top5_classes]
        #zip into tuples.
        predictions = zip(top5_breeds, top5_probabilities)

        return predictions