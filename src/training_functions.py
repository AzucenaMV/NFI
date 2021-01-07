import tensorflow as tf
import numpy as np
from src.classes import *


def simplest_nn(train_input: TrainInput):
    input_image = train_input.data[0]
    input_labels = train_input.labels[0]
    input_image = input_image.reshape(1,161,6)
    filter_s = 1
    kernel_s = 5
    conv_layer = tf.keras.layers.Conv1D(filter_s, kernel_s, activation=tf.nn.relu)
    pool_layer = tf.keras.layers.MaxPool1D(5, strides = 5)
    model = tf.keras.Sequential([conv_layer, conv_layer, pool_layer, conv_layer, conv_layer, pool_layer])
    output = model.predict(input_image)
    return output
