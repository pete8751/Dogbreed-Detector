import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow_datasets as tfds
from keras.src.utils import to_categorical
from tensorflow.keras import ImageDataGenerator, layers, models

# The following is a python ML model that will be used to classify breeds of dogs.

dataset, metadata = tfds.load('stanford_dogs', as_supervised=True, with_info=True)
train_dataset, test_dataset = dataset['train'], dataset['test']

num_train_examples = metadata.splits['train'].num_examples
num_test_examples = metadata.splits['test'].num_examples
class_names = metadata.features['label'].names

# Helper function extracting images, and labels, and resizing images, then returning list of labels and images.
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

target_shape = (64, 64)
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

training_labels_array, testing_labels_array = np.array(training_labels_array), np.array(testing_labels_array)

# I wanted to add an extra 3000 images for training, so I removed these from validation, and added them to testing.
# I give 3000 images for validation, and around 1500 images for testing.

extra_training, extra_training_labels = testing_norm_data[:3000], testing_labels_array[:3000]
training_norm_data = np.concatenate((training_norm_data, extra_training), axis=0)
training_labels_array = np.concatenate((training_labels_array, extra_training_labels), axis=0)

print(training_norm_data.shape)
validation_images_array, validation_labels_array = testing_norm_data[3000:7000], testing_labels_array[3000:7000]
testing_norm_data, testing_labels_array = testing_norm_data[7000:], testing_labels_array[7000:]


def display_image(image_array):
    plt.imshow(image_array)
    plt.axis('off')
    plt.show()


image = training_images_array[0]
print(image.shape)

print(validation_images_array.shape)

image_test = testing_images_array[0]

# Comparing Training images and label list.
display_image(image)
print(class_names[training_labels_array[0]])

# Comparing testing images and label list
display_image(image_test)
print(class_names[testing_labels_array[0]])


# training_images = training_images[:20000]
# training_labels = training_labels[:20000]
# testing_images = testing_images[:4000]
# testing_labels = testing_labels[:4000]

# Now that I have testing_norm_data, I can create a generator for the training data.
# I will use the ImageDataGenerator class to create a generator for the training data.
# Because my data is categorical, I will need to be careful with the train_datagen.flow() method.
# To pass categorical data to a model that expects binary data, you should convert your data to
# binary using the to_categorical function. Keras provides the to_categorical() function for this purpose.
# The to_categorical() function takes one argument: the list, numpy array or scalar to convert into a matrix
# of binary values (0 and 1) on the class axis. The class axis is the axis that has a different value for each class.
# In this case, the class axis is 0 because there are 120 classes that go from 0 to 119.
# The to_categorical() function returns a matrix with the same dimensions as the input matrix, but with a
# binary vector representation. The vector representation has a length of the number of classes in the dataset.
# The vector representation has a 1 in the column of the class value and 0 in all other columns for each row of the matrix.
# In other words, each row is a one hot encoding of the original matrix.
# If I had a list of 5 labels from the training dataset, they would look as follows:
# [2, 0, 2, 1, 2]
# If I convert this list to a matrix using the to_categorical() function, the result would be a matrix with 5 rows and 3 columns.
# The first row would have a 1 in the second column, the second row would have a 1 in the first column,
# the third row would have a 1 in the second column, the fourth row would have a 1 in the third column,
# and the fifth row would have a 1 in the second column. The rest of the values in the matrix would be 0.
# The matrix would look as follows:
# [[0, 1, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 0]]
# The following code will convert the labels to categorical data.
training_labels_array = to_categorical(training_labels_array)
validation_labels_array = to_categorical(validation_labels_array)
testing_labels_array = to_categorical(testing_labels_array)


train_datagen = ImageDataGenerator(
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)
train_generator = train_datagen.flow(training_norm_data, training_labels_array, batch_size=32)

# logits and labels must have the same first dimension, got logits shape [32,120] and labels shape [3840]
# 	 [[{{node sparse_categorical_crossentropy/SparseSoftmaxCrossEntropyWithLogits/SparseSoftmaxCrossEntropyWithLogits}}]] [Op:__inference_train_function_72890]
# I get the above error when I use the following model.
# I think the issue is that the labels are in the range of 0-119, but the model is expecting 0-1.
# The model is expecting a binary classification, but we have 120 classes.
# To fix this, we can use sparse_categorical_crossentropy instead of binary_crossentropy.
# I made this change, but still get tha same error.
# The issue is that the logits have shape [32,120], but the labels have shape [3840].
# The labels should have shape [32,120] as well.
# I don't know how to fix this.


model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), input_shape=(3, 150, 150)))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Conv2D(32, (3, 3)))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Conv2D(64, (3, 3)))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Flatten())  # this converts our 3D feature maps to 1D feature vectors
model.add(layers.Dense(64))
model.add(layers.Activation('relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1))
model.add(layers.Activation('sigmoid'))

# model.compile(loss='binary_crossentropy',
#               optimizer='adam',
#               metrics=['accuracy'])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
#now we can fit the model
# The following model causes an issue, because the labels are in the range of 0-119, but the model is expecting 0-1.
# The model is expecting a binary classification, but we have 120 classes.
# To fix this, we can use sparse_categorical_crossentropy instead of binary_crossentropy.
model.fit(train_generator, epochs=10, validation_data=(validation_images_array, validation_labels_array))

# model.fit(training_norm_data, training_labels_array, epochs=10, validation_data=(validation_images_array, validation_labels_array))










# model = models.Sequential()
# model.add(layers.Conv2D(64, (3, 3), activation='relu', input_shape=(64, 64, 3)))
# model.add(layers.MaxPooling2D(2, 2))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D(2, 2))
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.Flatten())
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dense(120, activation='softmax'))
#
# model.compile(optimizer='adam', loss='sparce categorical_crossentropy', metrics=['accuracy'])
#
# model.fit(training_images, training_labels, epochs=10, validation_data=(testing_images, testing_labels))
