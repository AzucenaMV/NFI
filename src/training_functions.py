import tensorflow as tf
import numpy as np
from src.classes import *


def simplest_nn(train_input: TrainInput):
    input_image = train_input.data[0]
    input_labels = train_input.labels[0].reshape(1,6)
    print(input_image.shape)
    input_image = input_image.reshape(1,161,6,1)
    print(input_image.shape)
    # should probably add more filters, but not sure how to choose it
    filter_s = 1
    # maybe should manually set zero padding for one dimension, so 6 doesn't decrease
    kernelsize = (3,1)
    poolsize = (3,1)
    # can also flatten within layers
    # example adds dense layer, then dropout, dense, dense
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(filter_s, kernelsize, activation=tf.nn.relu))
    model.add(tf.keras.layers.MaxPool2D(poolsize))
    model.add(tf.keras.layers.Conv2D(filter_s, kernelsize, activation=tf.nn.relu))
    model.add(tf.keras.layers.MaxPool2D(poolsize))
    model.add(tf.keras.layers.Conv2D(filter_s, kernelsize, activation=tf.nn.relu))
    model.add(tf.keras.layers.Conv2D(filter_s, kernelsize, activation=tf.nn.relu))
    model.add(tf.keras.layers.MaxPool2D(poolsize))
    model.add(tf.keras.layers.MaxPool2D(poolsize))
    output = model.predict(input_image)
    print(model.summary())
    print(output.shape)
    return output
