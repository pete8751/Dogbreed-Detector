import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras import datasets, layers, models

print(tfds.load('stanford_dogs', as_supervised=True, with_info=True))
