# import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import datasets, layers, models
# The following is a python ML model that will be used to classify breeds of dogs.

(training_images, training_labels), (testing_images, testing_labels) = datasets.cifar10.load_data()
training_images, testing_images = training_images / 255, testing_images / 255

class_names = ['Plane', 'Car', 'Bird', 'Deer', 'Cat', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']

print(type(training_images))
print(type(training_labels))

# for i in range(16):
#     plt.subplot(4, 4, i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.imshow(training_images[i], cmap=plt.cm.binary)
#     plt.xlabel(class_names[training_labels[i][0]])
#
# plt.show()
#
training_images = training_images[:20000]
training_labels = training_labels[:20000]
testing_images = testing_images[:4000]
testing_labels = testing_labels[:4000]

print(testing_images.shape)
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
