import tensorflow as tf
import numpy as np
from src.classes import *


def simplest_nn(train_input: TrainInput):
    all_images = train_input.data
    all_labels = train_input.labels
    split_point = len(all_images)//2
    train_images = all_images[:split_point]
    validation_images = all_images[split_point:]
    train_labels = all_labels[:split_point]
    validation_labels = all_labels[split_point:]
    # input_image = train_input.data[0]
    # input_labels = train_input.labels[0].reshape(1,6)
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
    model.add(tf.keras.layers.Flatten())
    batch_size = 50  # number of samples processed before the model is updated
    num_epochs = 10  # number of complete passes through the training dataset before the training stops

    # Compiling the model adds a loss function, optimiser and metrics to track during training
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss=tf.keras.losses.sparse_categorical_crossentropy,
                  metrics=['accuracy'])

    model.fit(x=train_images,
              y=train_labels,
              batch_size=batch_size,
              epochs=num_epochs,
              validation_data=(validation_images, validation_labels.astype(np.float32)))
    print(model.summary())
    return "ok"
