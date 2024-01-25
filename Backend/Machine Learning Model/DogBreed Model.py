from tensorflow.keras import layers, models, preprocessing, applications
import tensorflow_datasets as tfds
import numpy as np
import cv2

dataset, metadata = tfds.load('stanford_dogs', as_supervised=True, with_info=True)
train_dataset, test_dataset = dataset['train'], dataset['test']

# trainData = list(train_dataset.as_numpy_iterator())
# print(trainData)
print(test_dataset)

num_train_examples = metadata.splits['train'].num_examples
num_test_examples = metadata.splits['test'].num_examples
class_names = metadata.features['label'].names

np.save('/content/class_names.npy', class_names)

# print(training_labels)
print(num_train_examples)
print(num_test_examples)
print(class_names)

#Helper function extracting images, and labels, and resizing images, then returning list of labels and images.
def extractData(dataset):
    image_list = []
    label_list = []

    for batch_data in dataset.batch(batch_size=1).as_numpy_iterator():
        image, label = batch_data
        img = cv2.resize(image[0], target_shape, interpolation=cv2.INTER_AREA)
        image_list.append(img)
        label_list.append(label[0])

    return (image_list, label_list)

# Convert the lists to NumPy arrays
target_shape = (100, 100)

training_images_array, training_labels_array = extractData(train_dataset)
testing_images_array, testing_labels_array = extractData(test_dataset)

training_images_array, testing_images_array = np.array(training_images_array), np.array(testing_images_array)

# Calculating means and standard deviations for each feature.
train_mean, train_std = np.mean(training_images_array), np.std(training_images_array)
test_mean, test_std = np.mean(testing_images_array), np.std(testing_images_array)

# Normalizing. I add epsilon incase std is exactly 0.
epsilon = 0.0001
training_norm_data = (training_images_array - train_mean) / (train_std + epsilon)
testing_norm_data = (testing_images_array - test_mean) / (test_std + epsilon)

np.save('/content/train_dataset.npy', training_norm_data)
np.save('/content/train_labels.npy', training_labels_array)
np.save('/content/testing_dataset.npy', testing_norm_data)
np.save('/content/testing_labels.npy', testing_labels_array)

training_norm_data = np.load('/content/train_dataset.npy')
training_labels_array = np.load('/content/train_labels.npy')
testing_norm_data = np.load('/content/testing_dataset.npy')
testing_labels_array = np.load('/content/testing_labels.npy')
class_names = np.load('/content/class_names.npy')

training_labels_array, testing_labels_array = np.array(training_labels_array), np.array(testing_labels_array)


extra_training, extra_training_labels = testing_norm_data[:3000], testing_labels_array[:3000]
training_norm_data = np.concatenate((training_norm_data, extra_training), axis=0)
training_labels_array = np.concatenate((training_labels_array, extra_training_labels), axis=0)

print(training_norm_data.shape)
validation_images_array, validation_labels_array = testing_norm_data[3000:7000], testing_labels_array[3000:7000]
testing_norm_data, testing_labels_array = testing_norm_data[7000:], testing_labels_array[7000:]

train_datagen = preprocessing.image.ImageDataGenerator(
        rotation_range=20,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,)

# Creating the validation_generator
validation_datagen = preprocessing.image.ImageDataGenerator(
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,)

train_generator = train_datagen.flow(training_norm_data, training_labels_array, batch_size=32)
validation_generator = validation_datagen.flow(validation_images_array, validation_labels_array, batch_size = 32)

base_model = applications.Xception(
    input_shape=(100, 100, 3),
    include_top=False,
    weights="imagenet",
    pooling=None,  # Global average pooling for flattening
)

model = models.Sequential()
model.add(base_model)

model.add(layers.Flatten())
model.add(layers.Dense(120, activation='softmax'))

model.layers[0].trainable = False

pre_trained_data = model.predict(train_generator)

np.save('/content/pre_trained_bottleneck_features.npy', pre_trained_data)

pre_trained_data = model.predict(train_generator)

np.save('/content/pre_trained_bottleneck_features.npy', pre_trained_data)

train_data = np.load('/content/pre_trained_bottleneck_features.npy')

model = models.Sequential()
model.add(layers.Flatten(input_shape=train_data.shape[1:]))
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(120, activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(train_data, training_labels_array, epochs=10, validation_data=validation_generator)


model.summary()
