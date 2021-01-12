import tensorflow as tf
import numpy as np
from src.classes import *
import matplotlib.pyplot as plt

def create_model():
    # should probably add more filters, but not sure how to choose it
    filter_s = 3
    # maybe should manually set zero padding for one dimension, so 6 doesn't decrease
    kernelsize = (3, 2)
    poolsize = (3, 1)
    # can also flatten within layers
    # example adds dense layer, then dropout, dense, dense
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(6, kernelsize, activation=tf.nn.relu))
    model.add(tf.keras.layers.Conv2D(6, kernelsize, activation=tf.nn.relu))
    model.add(tf.keras.layers.MaxPool2D(poolsize))
    model.add(tf.keras.layers.Conv2D(6, kernelsize, activation=tf.nn.relu))
    model.add(tf.keras.layers.Conv2D(6, kernelsize, activation=tf.nn.relu))
    model.add(tf.keras.layers.MaxPool2D(poolsize))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dropout(rate=0.5))
    model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(6, activation=tf.nn.softmax))
    return model


def simplest_nn(train_input: TrainInput):
    all_images = tf.random.shuffle(train_input.data.reshape(-1, 161, 6, 1))
    all_labels = tf.random.shuffle(train_input.labels.reshape(-1, 6))
    # print(all_images.shape, all_labels.shape)
    train_images, validation_images, test_images = tf.split(all_images, [1300, 1300, 3332])
    train_labels, validation_labels, test_labels = tf.split(all_labels, [1300, 1300, 3332])

    input_image = train_input.data[0].reshape(1, 161, 6, 1)
    input_labels = train_input.labels[0].reshape(1, 6)

    model = create_model()

    print(model.predict(input_image).shape, input_labels.shape)
    model.summary()
    batch_size = 200  # number of samples processed before the model is updated
    num_epochs = 100  # number of complete passes through the training dataset before the training stops

    # Compiling the model adds a loss function, optimiser and metrics to track during training
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss=tf.keras.losses.categorical_crossentropy,
                  metrics=['accuracy'])

    history = model.fit(x=train_images,
              y=train_labels,
              batch_size=batch_size,
              epochs=num_epochs,
              validation_data=(validation_images, validation_labels))

    # plot loss
    plt.subplot(211)
    plt.title('Cross Entropy Loss')
    plt.plot(history.history['loss'], color='blue', label='train')
    plt.plot(history.history['val_loss'], color='red', label='test')
    plt.ylim(0, 2)
    # plot accuracy
    plt.subplot(212)
    plt.title('Classification Accuracy')
    plt.plot(history.history['accuracy'], color='blue', label='train')
    plt.plot(history.history['val_accuracy'], color='red', label='test')
    plt.ylim(0, 1)
    # add legend
    plt.legend()
    # Tweak spacing between subplots to prevent labels from overlapping
    plt.subplots_adjust(hspace=0.5)

    metric_values = model.evaluate(x=test_images, y=test_labels)

    print('Final TEST performance')
    for metric_value, metric_name in zip(metric_values, model.metrics_names):
        print('{}: {}'.format(metric_name, metric_value))


    return "ok"
